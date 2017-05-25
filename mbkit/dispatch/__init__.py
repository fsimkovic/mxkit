"""Dispatcher module for easy job submission to local machines or job management systems"""

__author__ = "Felix Simkovic"
__date__ = "24 May 2017"
__version__ = "0.2"

import logging
import os
import time
import warnings

from mbkit.dispatch.local import LocalJobServer
from mbkit.dispatch.lsf import LoadSharingFacility
from mbkit.dispatch.sge import SunGridEngine

# Keep track of which platforms we can handle
KNOWN_PLATFORMS = ["local", "lsf", "sge"]

logger = logging.getLogger(__name__)


class Job(object):
    """Generic :obj:`Job` class to allow for job control
    
    This class provides full access to various job submission
    platforms with a unified interface.
    
    """
    __slots__ = ["_lock", "_log", "_pid", "_qtype", "_script"]
    
    # Submission functions
    _SUB_F = {
        "local": LocalJobServer.jsub,
        "lsf": LoadSharingFacility.bsub,
        "sge": SunGridEngine.qsub,
    }
    # Kill functions
    _KILL_F = {
        "local": LocalJobServer.jdel,
        "lsf": LoadSharingFacility.bkill,
        "sge": SunGridEngine.qdel,
    }
    # Info functions
    _STAT_F = {
        "local": LocalJobServer.jstat,
        "lsf": LoadSharingFacility.bjobs,
        "sge": SunGridEngine.qstat,
    }
    # Hold functions
    _HOLD_F = {
        "sge": SunGridEngine.qhold,
    }
    # Release functions
    _RLS_F = {
        "sge": SunGridEngine.qrls,
    }
    # Alter functions
    _ALT_F = {
        "sge": SunGridEngine.qalter,
    }
    
    def __init__(self, qtype):
        """Instantiate a new :obj:`Job` submission class
        
        Parameters
        ----------
        qtype : str
           The queue type to submit the jobs to [ local | sge ]
        
        Raises
        ------
        ValueError
           Unknown platform
        
        """
        self._lock = False
        self._pid = None
        self._log = []
        self._script = []

        # Check immediately if we have a known platform
        if qtype.lower() in KNOWN_PLATFORMS:
            self._qtype = qtype.lower()
        else:
            raise ValueError("Unknown platform")
        
    def __str__(self):
        return "{0}(pid={1} qtype={2}".format(
            self.__class__.__name__, self.pid, self.qtype    
        )
    
    @property
    def finished(self):
        """Return whether the job has finished"""
        # Empty dictionaries default to False
        return not bool(self.stat())

    @property
    def log(self):
        """Return a list of the log file(s)"""
        return self._log
    
    @property
    def pid(self):
        """Return the process id of this job"""
        return self._pid

    @property
    def qtype(self):
        """Return the platform type we assigned to this job"""
        return self._qtype

    @property
    def script(self):
        """Return a list of the script file(s)"""
        return self._script
    
    def alter(self, priority=None):
        """Alter the job parameters
        
        Parameters
        ----------
        priority : int, optional
           The priority level of the job
        
        """
        alt_func = Job._ALT_F.get(self.qtype, None)
        if self.pid and callable(alt_func):
            return alt_func(self.pid)
        else:
            logger.debug("Function unavailable for specified queue type")
    
    def hold(self):
        """Hold the job"""
        hold_func = Job._HOLD_F.get(self.qtype, None)
        if self.pid and callable(hold_func):
            return hold_func(self.pid)
        else:
            logger.debug("Function unavailable for specified queue type")
    
    def kill(self):
        """Kill the job"""
        if self.pid:
            Job._KILL_F[self.qtype](self.pid)
    
    def release(self):
        """Release the job"""
        rls_func = Job._RLS_F.get(self.qtype, None)
        if self.pid and callable(rls_func):
            return rls_func(self.pid)
        else:
            logger.debug("Function unavailable for specified queue type")
    
    def submit(self, script, *args, **kwargs):
        """Submit a job to the job management platform
    
        Parameters
        ----------
        script : list
           A list of one or more scripts with absolute paths
    
        Raises
        ------
        ValueError
           One or more scripts cannot be found
        ValueError
           One or more scripts are not executable
        ValueError
           Unknown queue type provided
    
        """
        # Only allow one submission per job
        if self._lock:
            logger.debug("This Job instance is locked, for further submissions create a new")
            return
        
        # Define a directory if not already done
        if not('directory' in kwargs and kwargs['directory']):
            kwargs['directory'] = os.getcwd()
    
        # Quick check if all scripts are sound - Also keep copy of logs and scripts
        if isinstance(script, str) and os.path.isfile(script) and os.access(script, os.X_OK):
            self._log = [script.rsplit('.', 1)[0] + '.log']
            self._script = [script]
        elif (isinstance(script, list) or isinstance(script, tuple)) 
             and all(os.path.isfile(fpath) for fpath in script) 
             and all(os.access(fpath, os.X_OK) for fpath in script):
            self._log = [s.rsplit('.', 1)[0] + '.log' for s in script]
            self._script = list(script)
        else:
            raise ValueError("One or more scripts cannot be found or are not executable")
        
        # Get the submission function and submit the job
        self._pid = Job._SUB_F[self.qtype](script, **kwargs)
        # Lock this Job so we cannot submit another
        self._lock = True
    
    def stat(self):
        """Get some data for the job"""
        stat_func = Job._STAT_F.get(self.qtype, None)
        if callable(stat_func):
            return stat_func(self.pid)
        else:
            logger.debug("Function unavailable for specified queue type")
            return {}
        
    def wait(self, check_success=None, interval=30, monitor=None):
        """Wait until all processing has finished
        
        Parameters
        ----------
        check_success : func, optional
           A function handler to be called to check the success status of a job
           !!! The function is required to take a single argument, a log file !!!
        interval : int, optional
           The interval to wait between checking (in seconds) [default: 30]
        monitor : func, optional
           A function handler to be called to update, e.g. GUIs

        """
        do_check_success = bool(check_success and callable(check_success))
        if do_check_success:
            logger.debug("Checking for Job %d success with function %s", self.pid, check_success.__name__) 
        do_monitor = bool(monitor and callable(monitor))

        while not self.finished:
            # Allow for early termination
            if do_check_success:
                for log in self.log:
                    if os.path.isfile(log) and check_success(log):
                        logger.debug("Job %d succeeded, run log: %s", self.pid, log)
                        self.kill()
            # Allow for GUI updating
            if do_monitor:
                monitor()
            # Wait if nothing else
            time.sleep(interval)
        
