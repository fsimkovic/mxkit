"""Python wrapper module for the Molrep binary"""

__author__ = "Felix Simkovic & Ronan Keegan"
__date__ = "07 Mar 2017"
__version__ = 0.1

from mbkit.cli import AbstractCommandline
from mbkit.cli import Argument
from mbkit.cli import Option
from mbkit.cli import Switch


class MolrepCommandline(AbstractCommandline):
    """Python wrapper for the Molrep [#]_ binary

    Description
    -----------

    .. [#] A.Vagin, A.Teplyakov, MOLREP: an automated program for molecular replacement.,
       J. Appl. Cryst. (1997) 30, 1022-1025.

    Examples
    --------

    1. Run Molrep to do basic molecular replacement:
    >>> from mbkit.cli import Molrep
    >>> molrep_exe = Molrep.MolrepCommandLine(
    ...     "/usr/bin/molrep", hklin="data.mtz", xyzin="model.pdb")
    >>> print(molrep_exe)
    /usr/bin/molrep -f data.mtz -m model.pdb

    """
    def __init__(self, cmd='molrep', **kwargs):
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
