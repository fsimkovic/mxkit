"""Module to store cluster management platform specific code"""

__author__ = "Felix Simkovic"
__date__ = "08 May 2017"
__version__ = "0.1"

import logging
import os
import re

import cexectools

logger = logging.getLogger(__name__)


class _Platform(object):
    """Parent class for all management platforms"""
    pass


class LoadSharingFacility(_Platform):
    """Object ot handle the Load Sharing Facility (LSF) management platform
    
    Warnings
    --------
    This platform is not yet fully supported. The code in this class might work
    but no guarantees can be given. Please report any bugs to the developers.

    """

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

        """
        # Prepare the command
        cmd = ["bsub", "-cwd"]
        #if array:
        #    cmd += ["-t", array]
        if deps:
            cmd += ["-w",  " && ".join(["done(%s)" % dep for dep in map(str, deps)])]
        if log:
            cmd += ["-o", log]
        if name:
            cmd += ["-J", name]
        # if pe_opts:
        #     cmd += ["-pe"] + pe_opt.split()
        if priority:
            cmd += ["-sp", str(priority)]
        if queue:
            cmd += ["-q", queue]
        if time:
            cmd += ["-W", str(time)]
        cmd += ["<"] + map(str, command)
        # Submit the job
        stdout = cexectools.cexec(cmd, directory=directory)
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
        cmd = ["bjobs", "-j", str(jobid)]
        stdout = cexectools.cexec(cmd, permit_nonzero=True)
        data = {}
        # line_split = re.compile(':\s+')
        # for line in stdout.split(os.linesep):
        #     line = line.strip()
        #     if 'jobs do not exist' in line:
        #         return data
        #     if not line or "=" * 30 in line:
        #         continue
        #     else:
        #         kv = line_split.split(line, 1)
        #         if len(kv) == 2:
        #             data[kv[0]] = kv[1]
        return data
    
    @staticmethod
    def bkill(jobid):
        """Remove a job from the LSF queue
        
        Parameters
        ----------
        jobid : int
           The job id to remove

        """
        cmd = ["bkill", str(jobid)]
        _ = cexectools.cexec(cmd)
        logger.debug("Removed job %d from the queue", jobid)


class SunGridEngine(_Platform):
    """Object to handle the Sun Grid Engine (SGE) management platform"""
    
    @staticmethod
    def qsub(command, array=None, deps=None, directory=None, log=None, name=None, pe_opts=None, priority=None, queue=None, shell=None, time=None, *args, **kwargs):
        """Submit a job to the SGE queue

        Parameters
        ----------
        command : list
           A list with the final command
        array : tuple, optional
           An array specific tuple in format (start, stop, max)
        deps : list, optional
           A list of dependency job ids
        directory : str, optional
           A path to a directory to run the job in
        log : str, optional
           The path to a logfile for stdout
        name : str, optional
           The name of the job
        pe_opts : list, optional
           Job-specific keywords
        priority : int, optional
           The priority level of the job
        queue : str, optional
           The queue to submit the job to
        shell : str, optional
           The absolute path to the shell to run the job in
        time : int, optional
           The maximum runtime of the job in seconds

        """
        # Prepare the command with default options
        cmd = ["qsub", "-cwd", "-V", "-w", "e"]
        if array:
            cmd += ["-t", "{0}-{1}".format(*array[:2]), "-tc", str(array[2])]
        if deps:
            cmd += ["-hold_jid",  "{0}".format(",".join(map(str, deps)))]
        if log:
            # '-j y' required to pipe stderr to stdout
            cmd += ["-j", "y", "-o", log]
        if name:
            cmd += ["-N", name]
        if pe_opts:
            cmd += ["-pe"] + pe_opt.split()
        if priority:
            cmd += ["-p", str(priority)]
        if queue:
            cmd += ["-q", queue]
        if shell:
            cmd += ["-S", shell]
        if time:
            cmd += ["-l", "h_rt={0}".format(time)]
        cmd += map(str, command)
        # Submit the job
        stdout = cexectools.cexec(cmd, directory=directory)
        # Obtain the job id
        jobid = int(stdout.split()[2].split(".")[0]) if array else int(stdout.split()[2])
        logger.debug("Job %d successfully submitted to the SGE queue", jobid)
        return jobid
    
    @staticmethod
    def qstat(jobid):
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
        cmd = ["qstat", "-j", str(jobid)]
        stdout = cexectools.cexec(cmd, permit_nonzero=True)
        data = {}
        line_split = re.compile(':\s+')
        for line in stdout.split(os.linesep):
            line = line.strip()
            if 'jobs do not exist' in line:
                return data
            if not line or "=" * 30 in line:
                continue
            else:
                kv = line_split.split(line, 1)
                if len(kv) == 2:
                    data[kv[0]] = kv[1]
        return data
    
    @staticmethod
    def qdel(jobid):
        """Remove a job from the SGE queue
        
        Parameters
        ----------
        jobid : int
           The job id to remove

        """
        cmd = ["qdel", str(jobid)]
        _ = cexectools.cexec(cmd)
        logger.debug("Removed job %d from the queue", jobid)

