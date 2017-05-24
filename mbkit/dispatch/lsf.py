"""Module to store LoadSharingFacility cluster management platform code"""

__author__ = "Felix Simkovic"
__date__ = "08 May 2017"
__version__ = "0.1"

import logging
import os

from mbkit.dispatch.cexectools import cexec

logger = logging.getLogger(__name__)


class LoadSharingFacility(object):
    """Object to handle the Load Sharing Facility (LSF) management platform
    
    Warnings
    --------
    This platform is not yet fully supported. The code in this class might work
    but no guarantees can be given. Please report any bugs to the developers.

    """
    
    @staticmethod
    def bsub(command, array=None, deps=None, directory=None, log=None, name=None, pe_opts=None, priority=None, queue=None, shell=None, time=None, *args, **kwargs):
        """Submit a job to the LSF queue

        Parameters
        ----------
        command : list
           A list with the final command
        array : tuple, optional
           An array specific tuple in format (start, stop, max) [Unused]
        deps : list, optional
           A list of dependency job ids
        directory : str, optional
           A path to a directory to run the job in
        log : str, optional
           The path to a logfile for stdout
        name : str, optional
           The name of the job
        pe_opts : list, optional
           Job-specific keywords [Unused]
        priority : int, optional
           The priority level of the job
        queue : str, optional
           The queue to submit the job to
        shell : str, optional
           The absolute path to the shell to run the job in
        time : int, optional
           The maximum runtime of the job in seconds

        Raises
        ------
        RuntimeError
           Array submission not yet implemented
    
        """
        # Prepare the command
        cmd = ["bsub", "-cwd"]
        if array:
            msg = "Array submission not yet implemented"
            raise RuntimeError(msg)
        if deps:
            cmd += ["-w",  " && ".join(["done(%s)" % dep for dep in map(str, deps)])]
        if log:
            cmd += ["-o", log]
        if name:
            cmd += ["-J", name]
        if priority:
            cmd += ["-sp", str(priority)]
        if queue:
            cmd += ["-q", queue]
        if time:
            cmd += ["-W", str(time)]
        cmd += ["<"] + map(str, command)
        # Submit the job
        stdout = cexec(cmd, directory=directory)
        # Obtain the job id
        jobid = int(stdout.split()[1][1:-1])
        logger.debug("Job %d successfully submitted to the LSF queue", jobid)
        return jobid
   
    @staticmethod
    def bjobs(jobid):
        """Obtain information about a job id
         
        Parameters
        ----------
        jobid : int
           The job id to remove

        Returns
        -------
        dict
           A dictionary with job specific data

        """
        logger.critical("Not yet implemented")
        return {}
    
    @staticmethod
    def bkill(jobid):
        """Remove a job from the LSF queue
        
        Parameters
        ----------
        jobid : int
           The job id to remove

        """
        cexec(["bkill", str(jobid)])
        logger.debug("Removed job %d from the queue", jobid)

    @staticmethod
    def rename_array_logs(array_jobs_f, directory):
        """Rename a set of array logs to match the names of the scripts

        Parameters
        ----------
        array_jobs_f : str
           The path to the 'array.jobs' file
        directory : str
           The directory containing the 'arrayJob_X.log' files

        Raises
        ------
        ValueError
           Number of scripts and logs non-identical

        """
        logger.debug("Array job file provided for renaming logs: %s", array_jobs_f)
        logger.critical("Not yet implemented")




