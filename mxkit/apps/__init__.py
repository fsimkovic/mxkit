"""A command line interface wrapper module

This module contains classes for command line wrappers handling
different command line arguments and constructing entire command
line calls. It also handles the execution of a program and the
appropriate error handling.

"""

from __future__ import print_function

__author__ = "Felix Simkovic"
__date__ = "20 Feb 2017"
__version__ = "0.1"

import os
import sys

from Bio.Application import AbstractCommandline
from Bio.Application import _Argument
from Bio.Application import _ArgumentList
from Bio.Application import _Option
from Bio.Application import _Switch
from Bio.Application import _escape_filename


class AbstractCommandline(AbstractCommandline):
    """Extension to the original :obj:`AbstractCommandline <Bio.Application.AbstractCommandline>`"""

    def __init__(self, cmd, **kwargs):
        """Initialise a new :obj:`AbstractCommandline`"""
        cmd = AbstractCommandline.find_exec(cmd)
        super(AbstractCommandline, self).__init__(cmd, **kwargs)

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

