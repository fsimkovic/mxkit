"""Module to store SunGridEngine cluster management platform code"""

__author__ = "Felix Simkovic"
__date__ = "24 May 2017"
__version__ = "0.2"

import logging
import glob
import os
import re
import shutil

from mbkit.apps import SCRIPT_EXT
from mbkit.dispatch.cexectools import cexec

logger = logging.getLogger(__name__)


class SunGridEngine(object):
    """Object to handle the Sun Grid Engine (SGE) management platform"""

    @staticmethod
    def qalter(jobid, priority=None):
        """Alter a job in the SGE queue
        
        Parameters
        ----------
        jobid : int
           The job id to remove
        priority : int, optional
           The priority level of the job

        Notes
        -----
        This function is currently still under development does not provide
        the full range of ``qalter`` flags.

        Todo
        ----
        * Add more functionality
        * Add better debug message to include changed options

        """
        cmd = ["qalter"]
        if priority:
            cmd += ["-p", str(priority)]
        cmd += [str(jobid)]
        cexec(cmd)
        logger.debug("Altered parameters for job %d in the queue", jobid)

    @staticmethod
    def qdel(jobid):
        """Remove a job from the SGE queue
        
        Parameters
        ----------
        jobid : int
           The job id to remove
        
        """
        cexec(["qdel", str(jobid)])
        logger.debug("Removed job %d from the queue", jobid)

    @staticmethod
    def qhold(jobid):
        """Hold a job in the SGE queue
        
        Parameters
        ----------
        jobid : int
           The job id to remove

        """
        cexec(["qhold", str(jobid)])
        logger.debug("Holding back job %d from the queue", jobid)

    @staticmethod
    def qrls(jobid):
        """Release a job from the SGE queue
        
        Parameters
        ----------
        jobid : int
           The job id to remove

        """
        cexec(["qrls", str(jobid)])
        logger.debug("Released job %d from the queue", jobid)

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
        stdout = cexec(["qstat", "-j", str(jobid)], permit_nonzero=True)
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
    def qsub(command, deps=None, directory=None, hold=False, log=None, name=None, pe_opts=None,
             priority=None, queue=None, shell=None, time=None, *args, **kwargs):
        """Submit a job to the SGE queue

        Parameters
        ----------
        command : list
           A list with the final command
        deps : list, optional
           A list of dependency job ids
        directory : str, optional
           A path to a directory to run the job in
        hold : bool, optional
           Submit but __hold__ the job
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
        # See if we need to submit it as array
        if len(command) > 1:
            if directory is None:
                directory = os.getcwd()
            # Write all jobs into an array.jobs file
            array_jobs = os.path.join(directory, 'array.jobs')
            with open(array_jobs, 'w') as f_out:
                f_out.write(os.linesep.join(script))
            # Create the actual executable script
            array_script = os.path.join(directory, "array.script")
            with open(array_script, 'w') as f_out:
                # TODO: use MbKit make_script
                f_out.write(os.linesep.join([
                    "#!/bin/sh", 
                    "script=`sed -n \"${{SGE_TASK_ID}}p\" {0}`".format(array_jobs),
                    "log=\"${script%.*}\".log"
                    "$script > $log 2>&1",
                ]))
            # Overwrite the command
            command = [array_script]
            # Add command-line flags
            cmd += ["-t", "1-{0}".format(len(command)), "-tc", "{0}".format(len(command))]
            # Redirect the log file and reset if provided
            cmd += ["-j", "y", "-o", "/dev/null"]
            log = None
        if deps:
            cmd += ["-hold_jid", "{0}".format(",".join(map(str, deps)))]
        if hold:
            cmd += ["-h"]
        if log:
            cmd += ["-j", "y", "-o", log]
        if name:
            cmd += ["-N", name]
        if pe_opts:
            cmd += ["-pe"] + pe_opts.split()
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
        stdout = cexec(cmd, directory=directory)
        # Obtain the job id
        jobid = int(stdout.split()[2].split(".")[0]) if array else int(stdout.split()[2])
        logger.debug("Job %d successfully submitted to the SGE queue", jobid)
        return jobid
