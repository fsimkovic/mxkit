"""Python wrapper module for the MolRep binary"""

__author__ = "Felix Simkovic"
__date__ = "20 Feb 2017"
__version__ = 0.1

from mrkit.cli import AbstractCommandline
from mrkit.cli import Argument
from mrkit.cli import Option
from mrkit.cli import Switch


class MolRepCommandline(AbstractCommandline):
    """Python wrapper for the MolRep [#]_ binary

    Description
    -----------

    .. [#] Zhang Y, Skolnick J. (2004). Scoring function for automated assessment
       of protein structure template quality, Proteins, 57: 702-710.

    Examples
    --------

    1. Run TM-score to compare 'model' and 'native':
    >>> from mrkit.cli import TMscore
    >>> tm_exe = TMscore.TMscoreCommandLine(
    ...     "/usr/bin/TMscore", model="model.pdb", native="native.pdb")
    >>> print(tm_exe)
    /usr/bin/TMscore model.pdb native.pdb

    """
    def __init__(self, cmd='molrep', **kwargs):
        cmd = self.find_exe(cmd)
        self.parameters = [
            Switch(['-h', 'help'],
                   ''),

            Option(['-f', 'hklin'],
                   '',
                   equate=False,
                   filename=True),
            Option(['-m', 'xyzin'],
                   '',
                   equate=False,
                   filename=True),

            Argument(['model'],
                     "Input model structure",
                     filename=True,
                     is_required=True),
            Argument(['native'],
                      "Input native structure",
                      filename=True,
                      is_required=True),
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)
