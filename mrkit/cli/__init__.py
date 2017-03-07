"""A command line interface wrapper module

This module contains classes for command line wrappers handling
different command line arguments and constructing entire command
line calls. It also handles the execution of a program and the
appropriate error handling.

"""

from __future__ import print_function

__author__ = "Felix Simkovic & Jens Thomas"
__date__ = "20 Feb 2017"
__version__ = 0.1

from Bio.Application import AbstractCommandline
from Bio.Application import _Argument
from Bio.Application import _ArgumentList
from Bio.Application import _Option
from Bio.Application import _Switch
from Bio.Application import _escape_filename

import os
import subprocess
import tempfile


class AbstractCommandline(AbstractCommandline):
    """Extension to the original :obj:`AbstractCommandline <Bio.Application.AbstractCommandline>`"""

    def __init__(self, cmd, **kwargs):
        """Initialise a new :obj:`AbstractCommandline`"""
        # Check if the executable is available
        cmd = AbstractCommandline.find_exec(cmd)
        super(AbstractCommandline, self).__init__(cmd, **kwargs)

    def __call__(self, *args, **kwargs):
        """Overwrite parent __call__"""
        raise AttributeError("Execution of AbstractCommandline made unavailable")

    def _as_list(self):
        """Return the command line as list"""
        self._validate()
        commandline = [_escape_filename(self.program_name)]
        for parameter in self.parameters:
            if parameter.is_set:
                commandline.extend(parameter._as_list())
        return commandline


    @staticmethod
    def find_exec(program, dirs=None):
        """Find the executable exename.

        Parameters
        ----------
        program : str
           The name or path to an executable
        dirs : list, tuple, optional
           Additional directories to search for the location

        """
        def is_exe(exe):
            return os.path.isfile(exe) and os.access(exe, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            paths = os.environ["PATH"].split(os.pathsep)
            if dirs:
                # Convert in case it's a tuple
                paths += list(dirs)

            for path in paths:
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        msg = "Executable unavailable: {0}".format(program)
        raise ValueError(msg)


class Argument(_Argument):
    def _as_list(self):
        if self.value is None:
            return []
        elif self.is_filename:
            return [_escape_filename(self.value)]
        else:
            return [self.value]


class ArgumentList(_ArgumentList):
    def _as_list(self):
        assert isinstance(self.value, list), \
                "Arguments should be a list"
        assert self.value, "Requires at least one filename"
        if self.is_filename:
            return [_escape_filename(v) for v in self.value]
        else:
            return [self.value]


class Option(_Option):
    def _as_list(self):
        if self.value is None:
            return [self.names[0]]
        if self.is_filename:
            v = _escape_filename(self.value)
        else:
            v = str(self.value)
        if self.equate:
            return ["%s=%s" % (self.names[0], v)]
        else:
            return [self.names[0], v]


class Switch(_Switch):
    def _as_list(self):
        assert not hasattr(self, "value")
        if self.is_set:
            return [self.names[0]]
        else:
            return []


# ========================================================================================================


class Worker(object):
    """Worker responsible for job execution

    """

    @staticmethod
    def run_command(command, logfile=None, directory=None, stdin=None, **kwargs):
        """Execute a command and return the exit code.

        Parameters
        ----------
        command : :obj:`AbstractCommandLine <mrkit.cli.AbstractCommandline>`
           Command to run
        stdin : str, optional
           Stdin for the command
        logfile : str, optional
           The path to the logfile
        directory : str, optional
           The directory to run the job in (cwd assumed)

        Returns
        -------
        returncode : int
           Subprocess exit code

        """
        if not isinstance(command, AbstractCommandline):
            msg = "Input command needs to be AbstractCommandline"
            raise TypeError(msg)

        if not directory:
            directory = os.getcwd()

        if logfile:
            if type(logfile) == file:
                logf = logfile
            else:
                logf = open(os.path.abspath(logfile), "w")
        else:
            logf = tempfile.NamedTemporaryFile(delete=False)

        if stdin != None:
            stdinstr = stdin
            stdin = subprocess.PIPE

        # Windows needs some special treatment
        if os.name == "nt":
            kwargs.update({'bufsize': 0, 'shell': "False"})

        p = subprocess.Popen(command._as_list(), stdin=stdin, stdout=logf,
                             stderr=subprocess.STDOUT, cwd=directory, **kwargs)

        if stdin != None:
            p.stdin.write(stdinstr)
            p.stdin.close()

        p.wait()
        logf.close()

        return p.returncode
