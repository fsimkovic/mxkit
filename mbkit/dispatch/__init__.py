"""Dispatcher module for easy job submission to local machines or job management systems"""

__author__ = "Felix Simkovic"
__date__ = "24 May 2017"
__version__ = "0.2"

import os
import time
import warnings

from mbkit.dispatch.local import LocalJobServer
from mbkit.dispatch.lsf import LoadSharingFacility
from mbkit.dispatch.sge import SunGridEngine

# Keep track of which platforms we can handle
KNOWN_PLATFORMS = ["local", "lsf", "sge"]


class Job(object):
    """Generic :obj:`Job` class to allow for job control
    
    This class provides full access to various job submission
    platforms with a unified interface.
    
    """
    
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
    
    __slots__ = ["_lock", "_pid", "_qtype"]
    
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
    def pid(self):
        """Return the process id of this job"""
        return self._pid

    @property
    def qtype(self):
        """Return the platform type we assigned to this job"""
        return self._qtype
    
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
        
        # Define a directory is not already done
        if not('directory' in kwargs and kwargs['directory']):
            kwargs['directory'] = os.getcwd()
    
        # Quick check if all scripts are sound
        if not all(os.path.isfile(fpath) for fpath in script):
            raise ValueError("One or more scripts cannot be found")
        elif not all(os.access(fpath, os.X_OK) for fpath in script):
            raise ValueError("One or more scripts are not executable")
        
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
        
    def wait(self):
        """Wait until all processing has finished"""
        while not self.finished:
            time.sleep(5)
