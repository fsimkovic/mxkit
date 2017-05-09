"""Module to store local job management code"""

__author__ = "Felix Simkovic"
__date__ = "09 May 2017"
__version__ = "0.1"

import logging
import multiprocessing
import os
import time

import cexectools

logger = logging.getLogger(__name__)


class _Worker(multiprocessing.Process):
    """Simple manual worker class to execute jobs in the queue"""

    def __init__(self, queue, check_success=None, directory=None, permit_nonzero=False):
        """Instantiate a new worker

        Parameters
        ----------
        queue : obj
           An instance of a :obj:`Queue <multiprocessing.Queue>`
        check_success : func, optional
           A callable function to check the success of a job
        directory : str, optional
           The directory to execute the jobs in
        permit_nonzero : bool, optional
           Allow non-zero return codes [default: False]

        """
        super(_Worker, self).__init__()
        self.check_success = check_success
        self.directory = directory
        self.permit_nonzero = permit_nonzero
        self.queue = queue

    def run(self):
        """Method representing the process's activity"""
        for job in iter(self.queue.get, None):
            if job is not None:
                logger.debug("Worker %s running job %s", multiprocessing.current_process().name, job)
                stdout = cexectools.cexec([job], directory=self.directory, permit_nonzero=self.permit_nonzero)
                with open(job.rsplit('.', 1)[0] + '.log', 'w') as f_out:
                    f_out.write(stdout)
                logger.debug("Worker %s running job %s finished", multiprocessing.current_process().name, job)
                if callable(self.check_success) and self.check_success(job):
                    logger.debug("Job %s succeeded on worker %s", job, multiprocessing.current_process().name)
                    break
            if self.queue.empty():
                break
        while not self.queue.empty():
            _job = self.queue.get()
            if _job is not None:
                logger.debug("Removing job %s from the queue", _job)


class LocalJobServer(object):
    """A local server to execute jobs via the multiprocessing module"""

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
        # Create workers equivalent to the number of jobs
        processes = []
        for _ in range(nproc):
            p = _Worker(queue, check_success=check_success, directory=directory, permit_nonzero=permit_nonzero)
            p.start()
            processes.append(p)
        # Add each command to the queue
        for cmd in command:
            queue.put(cmd, timeout=time)
        # Stop workers from exiting without completion
        for _ in range(nproc):
            queue.put(None) 
        for p in processes:
            p.join()

