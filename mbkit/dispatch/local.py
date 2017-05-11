"""Module to store local job management code"""

__author__ = "Felix Simkovic"
__date__ = "09 May 2017"
__version__ = "0.1"

import logging
import multiprocessing
import os
import time

import mbkit.dispatch.cexectools

logger = logging.getLogger()


class Worker(multiprocessing.Process):
    """Simple manual worker class to execute jobs in the queue"""

    def __init__(self, queue, success_state, check_success=None, directory=None, permit_nonzero=False):
        """Instantiate a new worker

        Parameters
        ----------
        queue : obj
           An instance of a :obj:`Queue <multiprocessing.Queue>`
        success_state : obj
           An instance of a :obl:`Value <multiprocessing.Value>`
        check_success : func, optional
           A callable function to check the success of a job
        directory : str, optional
           The directory to execute the jobs in
        permit_nonzero : bool, optional
           Allow non-zero return codes [default: False]

        """
        super(Worker, self).__init__()
        self.check_success = check_success
        self.directory = directory
        self.permit_nonzero = permit_nonzero
        self.success_state = success_state
        self.queue = queue

    def run(self):
        """Method representing the process's activity"""
        for job in iter(self.queue.get, None):
            if self.success_state.value:
                continue
            stdout = mbkit.dispatch.cexectools.cexec([job], directory=self.directory, permit_nonzero=self.permit_nonzero)
            with open(job.rsplit('.', 1)[0] + '.log', 'w') as f_out:
                f_out.write(stdout)
            if callable(self.check_success):
                if self.check_success(job):
                    self.success_state.value = True
                time.sleep(1)
    

class LocalJobServer(object):
    """A local server to execute jobs via the multiprocessing module
    
    Examples
    --------

    The most basic example of a :obj:`LocalJobServer` is to run scripts across one or
    more processors on a local machine. This can be achieved with the following example.

    >>> from mbkit.apps import make_python_script
    >>> from mbkit.dispatch.local import LocalJobServer
    >>> scripts = [
    ...     make_python_script(["import sys;", "print('hello');", "sys.exit(0);"])
    ...     for _ in range(3)
    ... ]
    >>> LocalJobServer.sub(scripts, nproc=2)

    This will create three Python script files and execute them by calling :func:`sub <LocalJobServer.sub>`. 
    
    Sometimes you might want to submit many jobs where you know that some are going to fail. In this 
    case, you can also use the :obj:`LocalJobServer` and provide the ``permit_nonzero`` keyword argument,
    which will allow non-zero return codes from commands.

    If you you intend to submit jobs, and want to terminate execution prematurely because you are only
    interested in one job succeeding, you can provide a function handle via the ``check_success`` keyword.

    >>> from mbkit.apps import make_python_script
    >>> from mbkit.dispatch.local import LocalJobServer
    >>> def succ_func(j):
    ...     with open(j.rsplit('.', 1)[0] + '.log') as f_in:
    ...         lines = f_in.readlines()
    ...     return any("job 3" in l for l in lines)
    >>> scripts = [
    ...     make_python_script(["import sys;", "print('job {0}');".format(i), "sys.exit(0);"])
    ...     for i in range(5)
    ... ]
    >>> LocalJobServer.sub(scripts, nproc=2, check_success=succ_func)

    In this example, we create and provde the :func:`succ_func` to the :func:`sub <LocalJobServer.sub>` call.
    As jobs are executed, each worker checks if that particular job was successful via :func:`succ_func`,
    and if so the entire execution process will terminate. **Note, only log files for the executed jobs will 
    be created.**

    """

    @staticmethod
    def sub(command, check_success=None, directory=None, nproc=1, permit_nonzero=False, time=None, *args, **kwargs):
        """Submission function for local job submission via ``multiprocessing``
        
        Parameters
        ----------
        command : list
           A list with the final command
        check_success : func, optional
           A callable function to check the success of a job
        directory : str, optional
           The directory to execute the jobs in
        nproc : int, optional
           The number of processors to use
        permit_nonzero : bool, optional
           Allow non-zero return codes [default: False]
        time : int, optional
           The maximum runtime of the job in seconds

        Raises
        ------
        ValueError
           check_success option requires a callable function

        """
        if check_success and not callable(check_success):
            msg = "check_success option requires a callable function/object: {0}".format(check_success)
            raise ValueError(msg)
        
        # Create a new queue
        queue = multiprocessing.Queue()
        success_state = multiprocessing.Value('b', False)
        # Create workers equivalent to the number of jobs
        workers = []
        for _ in range(nproc):
            wp = Worker(queue, success_state, check_success=check_success, directory=directory, permit_nonzero=permit_nonzero)
            wp.start()
            workers.append(wp)
        # Add each command to the queue
        for cmd in command:
            queue.put(cmd)
        # Stop workers from exiting without completion
        for _ in range(nproc):
            queue.put(None) 
        # Start the workers
        for wp in workers:
            wp.join(time)

