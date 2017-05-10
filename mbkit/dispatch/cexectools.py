"""Module to contain code for the most basic job execution"""

__author__ = "Felix Simkovic"
__date__ = "08 May 2017"
__version__ = "1.0"

import logging
import os
import signal
import subprocess
import sys

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
        kwargs = {"bufsize":0, "shell":"False"} if os.name == "nt" else {}
        p = subprocess.Popen(cmd, cwd=directory, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, **kwargs)
        # We require the str.encode() and str.decode() functions for Python 2.x and 3.x compatibility
        stdout, _ = p.communicate(input=stdin.encode()) if stdin else p.communicate()
        stdout = stdout.decode()
        if p.returncode == 0 or permit_nonzero:
            return stdout.strip()
        else:
            msg = "Execution of '{0}' exited with non-zero return code ({1}): {2}" .format(' '.join(cmd), p.returncode, stdout)
            raise RuntimeError(msg)
    # Allow ctrl-c's
    except KeyboardInterrupt:
        os.kill(p.pid, signal.SIGTERM)
        sys.exit(signal.SIGTERM)
