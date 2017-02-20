"""A command line interface wrapper module

This module contains classes for command line wrappers handling
different command line arguments and constructing entire command
line calls. It also handles the execution of a program and the
appropriate error handling.

"""

__author__ = "Felix Simkovic"
__date__ = "20 Feb 2017"
__version__ = 0.1


from Bio.Application import AbstractCommandline
from Bio.Application import _Argument
from Bio.Application import _ArgumentList
from Bio.Application import _Option
from Bio.Application import _Switch

import os


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
    pass


class ArgumentList(_ArgumentList):
    pass


class Option(_Option):
    pass


class Switch(_Switch):
    pass

