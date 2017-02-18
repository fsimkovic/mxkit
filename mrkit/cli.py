"""A command line interface wrapper module

This module contains classes for command line wrappers handling
different command line arguments and constructing entire command
line calls. It also handles the execution of a program and the
appropriate error handling.

"""

from __future__ import print_function

__author__ = "Felix Simkovic"
__date__ = "01 Nov 2016"
__version__ = 0.1

import re


# What do we expose to the outside?
__all__ = [
    'Argument',
    'ArgumentList',
    'Option',
    'OptionList',
    'Switch',
]


# Define some regular expressions here
SPACE_QUOTE = re.compile(r'^\s*(".*")\s*$')


class _GenericArgument(object):
    """
    A generic command line argument object

    Description
    -----------
    This class contains a generic bunch of properties and functions
    applicable to all types of command line arguments.

    """

    def __init__(self):
        """A generic command line argument object"""
        self.is_set = False

    @property
    def names(self):
        """The names associated with the command line argument"""
        return self.__names

    @names.setter
    def names(self, names):
        """Define the names associated with the command line argument

        Parameters
        ----------
        names : list, tuple

        """
        self.__names = names
    
    @property
    def description(self):
        """The description associated with the command line argument"""
        return self.__description
    
    @description.setter
    def description(self, description):
        """Define the associated with the command line argument

        Parameters
        ----------
        description : str

        """
        self.__description = description

    @property
    def equate(self):
        """The representation status of the command line argument"""
        return self.__equate

    @equate.setter
    def equate(self, equate):
        """Define if the key and value need to be separated
        by an `=` symbol

        Parameters
        ----------
        equate : bool

        """
        self.__equate = equate

    @property
    def is_filename(self):
        """The filename status of the command line argument"""
        return self.__is_filename
    
    @is_filename.setter
    def is_filename(self, is_filename):
        """Define if the argument is a filename

        Parameters
        ----------
        is_filename : bool

        """
        self.__is_filename = is_filename
    
    @property
    def is_set(self):
        """The definition status of the command line argument"""
        return self.__is_set

    @is_set.setter
    def is_set(self, is_set):
        """Define if the argument is set

        Parameters
        ----------
        is_set : bool

        """
        self.__is_set = is_set

    @property
    def is_required(self):
        """The requirement status of the command line argument"""
        return self.__is_required

    @is_required.setter
    def is_required(self, is_required):
        """Define if the argument is required

        Parameters
        ----------
        is_required : bool

        """
        self.__is_required = is_required

    @staticmethod
    def _escape_spaces(filename):
        """Escape all white space in a filename

        Parameters
        ----------
        filename : str

        Returns
        -------
        filename : str

        """
        if " " not in str(filename):
            return str(filename)
        elif SPACE_QUOTE.match(str(filename)):
            return SPACE_QUOTE.match(str(filename)).group(1)
        else:
            return '"{value}"'.format(value=filename)


class Argument(_GenericArgument):
    """A simple command line argument

    Description
    -----------
    This class provides the structure to define a command line
    argument, which will be represented in the style of ``value``.

    Attributes
    ----------
    names : list, typle
       A list of names to define the argument
    description : str
       A description string for the command line argument
    is_filename : bool, optional
       The definition of ``value`` being a filename [default: False]
    is_required : bool, optional
       The definition of the command line argument being required [default: False]
    value : str, int, float
       The ``value`` associated with the command line argument

    Examples
    --------
    >>> argument = Argument(['-fasta', 'fasta'], 'This is the FASTA file',
    ...                     is_filename=True, is_required=True)
    >>> argument.value = '<PATH-TO-FASTA-FILE>'
    >>> print(argument)
    <PATH-TO-FASTA-FILE>

    """
    
    def __init__(self, names, description, is_filename=False, is_required=False):
        """Initialize a new :obj:`Argument` class

        Parameters
        ----------
        names : list, typle
           A list of names - first needs to be command line ``-flag``
        description : str
           A description string for the command line argument
        is_filename : bool, optional
           The definition of ``value`` being a filename [default: False]
        is_required : bool, optional
           The definition of the command line argument being required [default: False]

        """
        super(Argument, self).__init__()
        self.names = names
        self.description = description
        self.is_filename = is_filename
        self.is_required = is_required
        self.value = None

    def __str__(self):
        """The :obj:`str` representation of the :obj:`Argument`"""
        if self.is_set and self.value is not None:
            return '{0} '.format(self.value)
        else:
            return ''   
 
    @property
    def value(self):
        """The associated value of :obj:`Argument`"""
        if self.is_filename:
            return self._escape_spaces(self.__value)
        else:
            return self.__value
    
    @value.setter
    def value(self, value):
        """Define the associated value of :obj:`Argument`

        Parameters
        ----------
        value : str, int, float

        """
        if not value:
            self.__value = None
        elif not (isinstance(value, str) or isinstance(value, int) or isinstance(value, float)):
            raise TypeError('Provide one of str, int, float')
        self.__value = value


class ArgumentList(Argument):
    """A simple command line argument list

    Description
    -----------
    This class provides the structure to define a command line
    argument list, which will be represented in the style of ``<value1, value2, ... valueN>``.

    Attributes
    ----------
    names : list, typle
       A list of names to define the argument list
    description : str
       A description string for the command line argument list
    is_filename : bool, optional
       The definition of ``value`` being a filename [default: False]
    is_required : bool, optional
       The definition of the command line argument lsit being required [default: False]
    value : str, int, float
       The ``value`` associated with the command line argument list

    Examples
    --------
    >>> argument_list = ArgumentList(['-fasta', 'fasta'], 'This is the FASTA file',
    ...                              is_filename=True, is_required=True)
    >>> argument_list.value = ['<PATH-TO-FASTA-FILE1>', '<PATH-TO-FASTA-FILE2>', '<PATH-TO-FASTA-FILE3>']
    >>> print(argument_list)
    <PATH-TO-FASTA-FILE1> <PATH-TO-FASTA-FILE2> <PATH-TO-FASTA-FILE3>

    """
    def __init__(self, *args, **kwargs):
        """Initialize a new :obj:`Argument` class

        Parameters
        ----------
        names : list, typle
           A list of names - first needs to be command line ``-flag``
        description : str
           A description string for the command line argument
        is_filename : bool, optional
           The definition of ``value`` being a filename [default: False]
        is_required : bool, optional
           The definition of the command line argument being required [default: False]

        """
        super(ArgumentList, self).__init__(*args, **kwargs)

    def __str__(self):
        """The :obj:`str` representation of the :obj:`ArgumentList`"""
        if self.is_set and self.value is not None:
            return '{0} '.format(' '.join(self.value))
        else:
            return '' 

    @property
    def value(self):
        """The associated value of :obj:`ArgumentList`"""
        if self.is_filename:
            return list(self._escape_spaces(v) for v in self.__value)
        else:
            return self.__value
   
    @value.setter
    def value(self, value):
        """Define the associated value of :obj:`ArgumentList`

        Parameters
        ----------
        value : list, tuple

        """
        if value is None:
            self.__value = []
        elif not (isinstance(value, list) or isinstance(value, tuple)):
            raise TypeError('Provide one of list, tuple')
        self.__value = value


class Option(_GenericArgument):
    """A simple command line option

    Description
    -----------
    This class provides the structure to define a command line
    option, which will be represented in the style of `-flag value`.

    Attributes
    ----------
    names : list, typle
       A list of names - first needs to be command line ``-flag``
    description : str
       A description string for the command line option
    equate : bool, optional
       The definition of ``-flag`` and ``value``
       being separated by a ``=`` symbol [default: False]
    is_filename : bool, optional
       The definition of ``value`` being filenames [default: False]
    is_required : bool, optional
       The definition of the command line option being required [default: False]
    value : str, int, float
       The ``value`` associated with ``-flag``

    Examples
    --------
    >>> option = Option(['-fasta', 'fasta'], 'This is the FASTA file',
    ...                 is_filename=True, is_required=True)
    >>> option.value = ['<PATH-TO-FASTA-FILE>']
    >>> print(option)
    -fasta <PATH-TO-FASTA-FILE>

    >>> option = Option(['-fasta', 'fasta'], 'This is the FASTA file',
    ...                 equate=True, is_filename=True, is_required=True)
    >>> option.value = ['<PATH-TO-FASTA-FILE>']
    >>> print(option)
    -fasta=<PATH-TO-FASTA-FILE>

    """

    def __init__(self, names, description, equate=False, is_filename=False, is_required=False):
        """Initialize a new :obj:`Option` class

        Parameters
        ----------
        names : list, typle
           A list of names - first needs to be command line ``-flag``
        description : str
           A description string for the command line argument
        equate : bool, optional
           The definition of ``-flag`` and ``value``
           being separated by a ``=`` symbol [default: False]
        is_filename : bool, optional
           The definition of ``value`` being a filename [default: False]
        is_required : bool, optional
           The definition of the command line argument being required [default: False]

        """
        super(Option, self).__init__()
        self.names = names
        self.description = description
        self.equate = equate
        self.is_filename = is_filename
        self.is_required = is_required
        self.value = None

    def __str__(self):
        """The :obj:`str` representation of the :obj:`Option`"""
        if self.is_set and self.value is not None:
            sep = '=' if self.equate else ' '
            return '{flag}{sep}{arg} '.format(flag=self.names[0], arg=self.value, sep=sep)
        else:
            return ''
 
    @property
    def value(self):
        """The associated value of :obj:`Option`"""
        if self.is_filename:
            return self._escape_spaces(self.__value)
        else:
            return self.__value
    
    @value.setter
    def value(self, value):
        """Define the associated value of :obj:`Argument`

        Parameters
        ----------
        value : str, int, float

        """
        if not value:
            self.__value = None
        elif not (isinstance(value, str) or isinstance(value, int) or isinstance(value, float)):
            raise TypeError('Provide one of str, int, float')
        self.__value = value


class OptionList(Option):
    """A simple command line option list

    Description
    -----------
    This class provides the structure to define a command line
    option list, which will be represented in the style of `-flag <value1, value2, ... valueN>`.

    Attributes
    ----------
    names : list, typle
       A list of names - first needs to be command line ``-flag``
    description : str
       A description string for the command line option list
    equate : bool, optional
       The definition of ``-flag`` and ``<value1, value2, ... valueN>``
       being separated by a ``=`` & ``,`` symbol [default: False]
    is_filename : bool, optional
       The definition of ``<value1, value2, ... valueN>`` being filenames [default: False]
    is_required : bool, optional
       The definition of the command line option being required [default: False]
    value : str, int, float
       The ``<value1, value2, ... valueN>`` associated with ``-flag``

    Examples
    --------
    >>> option_list = OptionList(['-fasta', 'fasta'], 'This is the FASTA file',
    ...                          is_filename=True, is_required=True)
    >>> option_list.value = ['<PATH-TO-FASTA-FILE1>', '<PATH-TO-FASTA-FILE2>', '<PATH-TO-FASTA-FILE3>']
    >>> print(option_list)
    -fasta <PATH-TO-FASTA-FILE1> <PATH-TO-FASTA-FILE2> <PATH-TO-FASTA-FILE3>

    >>> option_list = OptionList(['-fasta', 'fasta'], 'This is the FASTA file',
    ...                          equate=True, is_filename=True, is_required=True)
    >>> option_list.value = ['<PATH-TO-FASTA-FILE1>', '<PATH-TO-FASTA-FILE2>', '<PATH-TO-FASTA-FILE3>']
    >>> print(option_list)
    -fasta=<PATH-TO-FASTA-FILE1>,<PATH-TO-FASTA-FILE2>,<PATH-TO-FASTA-FILE3>

    """
    def __init__(self, *args, **kwargs):
        """Initialize a new :obj:`Option` class

        Parameters
        ----------
        names : list, typle
           A list of names - first needs to be command line ``-flag``
        description : str
           A description string for the command line argument
        equate : bool, optional
           The definition of ``-flag`` and ``value``
           being separated by a ``=`` symbol [default: False]
        is_filename : bool, optional
           The definition of ``value`` being a filename [default: False]
        is_required : bool, optional
           The definition of the command line argument being required [default: False]

        """
        super(OptionList, self).__init__(*args, **kwargs)

    def __str__(self):
        """The :obj:`str` representation of the :obj:`OptionList`"""
        if self.is_set and self.value is not None:
            sep1 = ',' if self.equate else ' '
            sep2 = '=' if self.equate else ' '
            return '{flag}{sep}{arg} '.format(flag=self.names[0], arg=sep1.join(self.value), sep=sep2)
        else:
            return ''

    @property
    def value(self):
        """The associated value of :obj:`OptionList`"""
        if self.is_filename:
            return list(self._escape_spaces(v) for v in self.__value)
        else: 
            return self.__value
   
    @value.setter
    def value(self, value):
        """Define the associated value of :obj:`OptionList`

        Parameters
        ----------
        value : list, tuple

        """
        if value is None:
            self.__value = []
        elif not (isinstance(value, list) or isinstance(value, tuple)):
            raise TypeError('Provide one of list, tuple')
        self.__value = value


class Switch(_GenericArgument):
    """A simple command line switch

    Description
    -----------
    This class provides the structure to define a command line
    switch, which will be represented in the style of `-flag`.

    Attributes
    ----------
    names : list, typle
       A list of names - first needs to be command line ``-flag``
    description : str
       A description string for the command line option

    Examples
    --------
    >>> switch = Switch(['-nohoms', 'nohoms'], 'Exclude homologs')
    >>> switch.value = True
    >>> print(switch)
    -nohoms

    """
    def __init__(self, names, description):
        """Initialize a new :obj:`Switch` class

        Parameters
        ----------
        names : list, typle
           A list of names - first needs to be command line ``-flag``
        description : str
           A description string for the command line argument

        """
        super(Switch, self).__init__()
        self.names = names
        self.description = description

    def __str__(self):
        """The :obj:`str` representation of the :obj:`Switch`"""
        assert not hasattr(self, 'value')
        if self.is_set:
            return '{0} '.format(self.names[0])
        else:
            return ''

