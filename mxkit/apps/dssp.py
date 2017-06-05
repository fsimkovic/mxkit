"""Python wrapper module for the DSSP [#]_ binary

Examples
--------
>>> from mxkit.apps import dssp
>>> dssp_exe = dssp.DsspCommandline(
...     "/usr/bin/dssp", input="model.pdb", output="model.dssp"
... )
>>> print(dssp_exe)
/usr/bin/dssp -i model.pdb -o model.dssp

Citations
---------
.. [#] Kabsch W, Sander C (1983). Dictionary of protein secondary structure: pattern
   recognition of hydrogen-bonded and geometrical features. Biopolymers 22, 2577-2637.

"""

__author__ = "Felix Simkovic"
__date__ = "17 May 2017"
__version__ = "0.1"

from mxkit.apps import AbstractCommandline
from mxkit.apps import Argument
from mxkit.apps import Option
from mxkit.apps import Switch


class DsspCommandline(AbstractCommandline):

    def __init__(self, cmd='dssp', **kwargs):
        self.parameters = [
            Switch(['-v', 'verbose'],
                   'Verbose output'),
            Option(['-i', 'input'],
                    "Input structure",
                    equate=False,
                    filename=True,
                    is_required=True),
            Option(['-o', 'output'],
                    "Output DSSP file",
                    equate=False,
                    filename=True,
                    is_required=True),
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)
