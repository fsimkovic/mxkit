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


class AbstractCommandline(AbstractCommandline):
    """Extension to the original :obj:`AbstractCommandline <Bio.Application.AbstractCommandline>`"""

    def __call__(self, *args, **kwargs):
        """Overwrite parent __call__"""
        raise AttributeError("Execution of AbstractCommandline made unavailable")


class Argument(_Argument):
    pass


class ArgumentList(_ArgumentList):
    pass


class Option(_Option):
    pass


class Switch(_Switch):
    pass

