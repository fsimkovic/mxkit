"""Module to contain code for the most basic job execution"""

__author__ = "Felix Simkovic"
__date__ = "08 May 2017"
__version__ = "1.0"

import logging
import os
import signal
import subprocess
import sys

from mbkit.util import tmp_fname

logger = logging.getLogger(__name__)


def cexec(cmd, directory=None, stdin=None, permit_nonzero=False):
    """Execute a command

    Parameters
    ----------
    cmd : list
       The command to call
    directory : str, optional
       The directory to execute the job in
    stdin : str, optional
       Additional keywords provided to the command
    permit_nonzero : bool, optional
       Allow non-zero return codes [default: False]
    
    Returns
    -------
    str
       The processes standard out

    Raises
    ------
    RuntimeError
       Execution exited with non-zero return code

    """
    try:
        logger.debug("Executing '%s'", " ".join(cmd))
        kwargs = {"bufsize": 0, "shell": "False"} if os.name == "nt" else {}
        p = subprocess.Popen(cmd, cwd=directory, stdin=subprocess.PIPE, stderr=subprocess.STDOUT,
                             stdout=subprocess.PIPE, **kwargs)
        # We require the str.encode() and str.decode() functions for Python 2.x and 3.x compatibility
        stdout, _ = p.communicate(input=stdin.encode()) if stdin else p.communicate()
        stdout = stdout.decode()
        if p.returncode == 0:
            return stdout.strip()
        elif permit_nonzero:
            logger.debug("Ignoring non-zero returncode %d for '%s'", p.returncode, " ".join(cmd))
            return stdout.strip()
        else:
            msg = "Execution of '{0}' exited with non-zero return code ({1}): {2}" .format(' '.join(cmd),
                                                                                           p.returncode, stdout)
            raise RuntimeError(msg)
    # Allow ctrl-c's
    except KeyboardInterrupt:
        os.kill(p.pid, signal.SIGTERM)
        sys.exit(signal.SIGTERM)


def prep_array_scripts(scripts, directory, task_env):
    """Prepare multiple jobs to be an array

    Parameters
    ----------
    scripts : list
       The scripts to be run as part of the array
    directory : str
       The directory to create the files in
    task_env : str
       The task environment variable

    """
    # Write all jobs into an array.jobs file
    array_jobs = tmp_fname(directory=directory, prefix="array_", suffix='.jobs')
    with open(array_jobs, 'w') as f_out:
        f_out.write(os.linesep.join(scripts) + os.linesep)
    # Create the actual executable script
    array_script = array_jobs.replace(".jobs", ".script")
    with open(array_script, "w") as f_out:
        # Construct the content for the file
        content = "#!/bin/sh{linesep}"
        content += "script=`sed -n \"${{{task_env}}}p\" {array_jobs}`{linesep}"
        content += "$script{linesep}"
        content = content.format(array_jobs=array_jobs, linesep=os.linesep,
                                 task_env=task_env)
        f_out.write(content)
    return array_script, array_jobs
