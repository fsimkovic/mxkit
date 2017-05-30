"""Module to store LoadSharingFacility cluster management platform code"""

__author__ = "Felix Simkovic"
__date__ = "30 May 2017"
__version__ = "0.1"

import logging
import os

from mbkit.dispatch.cexectools import cexec
from mbkit.util import tmp_fname

logger = logging.getLogger(__name__)


class LoadSharingFacility(object):
    """Object to handle the Load Sharing Facility (LSF) management platform"""

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
        
        Todo
        ----
        * Extract the correct information
    
        """
        stdout = cexec(["bjobs", "-l", str(jobid)])
        if "Done successfully" in stdout:
            return {}
        else:
            return {'pid': jobid, 'status': "Running"}

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
    def bmod(jobid, priority=None):
        """Alter a job in the LSF queue

        Parameters
        ----------
        jobid : int
           The job id to remove
        priority : int, optional
           The priority level of the job

        Notes
        -----
        This function is currently still under development does not provide
        the full range of ``bmod`` flags.

        Todo
        ----
        * Add better debug message to include changed options

        """
        cmd = ["bmod"]
        if priority:
            cmd += ["-sp", str(priority)]
        cmd += [str(jobid)]
        cexec(cmd)
        logger.debug("Altered parameters for job %d in the queue", jobid)

    @staticmethod
    def bresume(jobid):
        """Release a job from the LSF queue

        Parameters
        ----------
        jobid : int
           The job id to remove

        """
        cexec(["bresume", str(jobid)])
        logger.debug("Released job %d from the queue", jobid)

    @staticmethod
    def bstop(jobid):
        """Hold a job in the LSF queue

        Parameters
        ----------
        jobid : int
           The job id to remove

        """
        cexec(["bstop", str(jobid)])
        logger.debug("Holding back job %d from the queue", jobid)

    @staticmethod
    def bsub(command, deps=None, directory=None, log=None, name=None, priority=None, queue=None,
             time=None, threads=None, *args, **kwargs):
        """Submit a job to the LSF queue

        Parameters
        ----------
        command : list
           A list with the final command
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
        if len(command) > 1:
            if directory is None:
                directory = os.getcwd()
            array_script, array_jobs = LoadSharingFacility._prep_array(command, directory)
            # Add command-line flags
            name = name if name else "mbkit"
            cmd += ["-J", "{0}[1-{1}]%{1}".format(name, len(command))]
            # Overwrite some defaults
            command = [array_script]
            log = os.devnull
        if deps:
            cmd += ["-w", " && ".join(["done(%s)" % dep for dep in map(str, deps)])]
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
        if threads:
            cmd += ["-R", '"span[ptile={0}]"'.format(threads)]
        cmd += ["<"] + map(str, command)
        # Submit the job
        stdout = cexec(cmd, directory=directory)
        # Obtain the job id
        jobid = int(stdout.split()[1][1:-1])
        logger.debug("Job %d successfully submitted to the LSF queue", jobid)
        return jobid

    @staticmethod
    def _prep_array(commands, directory):
        """Prepare multiple jobs to be an array"""
        # Write all jobs into an array.jobs file
        array_jobs = tmp_fname(directory=directory, prefix="array_", suffix='.jobs')
        with open(array_jobs, 'w') as f_out:
            f_out.write(os.linesep.join(commands) + os.linesep)
        # Create the actual executable script
        array_script = array_jobs.replace(".jobs", ".script")
        with open(array_script, "w") as f_out:
            content = "#!/bin/sh\n"
            content += "script=`sed -n \"${{SGE_TASK_ID}}p\" {0}`\n".format(array_jobs)
            content += "log=\"${script%.*}\".log\n"
            content += "$script > $log 2>&1\n"
            f_out.write(content)
        return array_script, array_jobs
