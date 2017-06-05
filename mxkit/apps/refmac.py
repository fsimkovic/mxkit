"""Python wrapper for the Refmac [#]_ binary

Description
-----------
Refmac [#]_ is a program designed for the REFinement of MACromolecular structures. Refmac is part of the CCP4
software suite. CCP4 is needed for running this wrapper. It can be downloaded from www.ccp4.ac.uk.

Examples
--------
1. Run Refmac (note: The command line is constant and the stdin options control how Refmac is run):

>>> from mxkit.apps import refmac
>>> refmac_exe = refmac.RefmacCommandline(
...     "/usr/bin/refmac5", hklin="data.mtz", hklout="name.mtz", xyzin="data.pdb", xyzout="name.pdb")
>>> print(refmac_exe)
/usr/bin/refmac5 HKLIN data.mtz HKLOUT name.mtz XYZIN data.pdb XYZOUT name.pdb

Citations
---------
.. [#] A.A.Vagin and E.J.Dodson, Refinement of Macromolecular Structures by the Maximum-Likelihood method.,
   Acta Cryst. D53, 240-255.

"""

__author__ = "Adam Simpkin"
__date__ = "15 Mar 2017"
__version__ = "0.1"

from mxkit.apps import AbstractCommandline
from mxkit.apps import Argument
from mxkit.apps import Option
from mxkit.apps import Switch


class RefmacCommandline(AbstractCommandline):

    def __init__(self, cmd='refmac5', **kwargs):
        self.parameters = [
            Switch(['-h', 'help'],
                   ''),
            Switch(['-i', 'interactive'],
                   ''),

            Option(['HKLIN', 'hklin'],
                   '',
                   equate=False,
                   filename=True),
            Option(['HKLOUT', 'hklout'],
                   '',
                   equate=False,
                   filename=True),
            Option(['XYZIN', 'xyzin'],
                   '',
                   equate=False,
                   filename=True),
            Option(['XYZOUT', 'xyzout'],
                   '',
                   equate=False,
                   filename=True),
            ]

        AbstractCommandline.__init__(self, cmd, **kwargs)
