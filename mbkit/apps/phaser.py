"""Python wrapper for the Phaser [#]_ binary

Description
-----------
Phaser [#]_ is a program for phasing macromolecular crystal structures with maximum likelihood methods. 
It has been developed by Randy Read's group at the Cambridge Institute for Medical Research (CIMR) in the 
University of Cambridge and is available through the Phenix (http://www.phenix-online.org/) and 
CCP4 (http://www.ccp4.ac.uk/) software suites.

Examples
--------
1. Run Phaser (note: The command line is constant and the stdin options control how Phaser is run):

>>> from mbkit.apps import phaser
>>> phaser_exe = phaser.PhaserCommandline("/usr/bin/phaser")
>>> print(phaser_exe)
/usr/bin/phaser

Citations
---------
.. [#] A.J.McCoy, R.W.Grosse-Kunstleve, P.D.Adams, M.D.Winn, L.C.Storoni, & R.J.Read, Phaser crystallographic software.,
   J. Appl. Cryst. (2007). 40, 658-674.
"""

__author__ = "Adam Simpkin"
__date__ = "26 May 2017"
__version__ = "0.1"

from mbkit.apps import AbstractCommandline
from mbkit.apps import Argument
from mbkit.apps import Option
from mbkit.apps import Switch

class PhaserCommandline(AbstractCommandline):

    def __init__(self, cmd='phaser', **kwargs):
        self.parameters = [
            Switch(['-h', 'help'],
                   ''),
            Switch(['-i', 'interactive'],
                   '')
            ]

        AbstractCommandline.__init__(self, cmd, **kwargs)