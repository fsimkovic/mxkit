"""Python wrapper for the TMscore [#]_ binary

Description
-----------
TM-score [#]_ is a metric for measuring the structural similarity of two protein models.
It is designed to solve two major problems in the traditional metrics such as
root-mean-square deviation (RMSD): (1) TM-score measures the global fold similarity
and is less sensitive to the local structural variations; (2) magnitude of TM-score
for random structure pairs is length-independent. TM-score has the value in (0,1],
where 1 indicates a perfect match between two structures. Following strict statistics
of structures in the PDB, scores below 0.17 corresponds to randomly chosen unrelated
proteins whereas with a score higher than 0.5 assume generally the same fold in SCOP/CATH.

Examples
--------
1. Run TM-score to compare 'model' and 'native':

>>> from mbkit.apps import TMscore
>>> tm_exe = TMscore.TMscoreCommandline(
...     "/usr/bin/TMscore", model="model.pdb", native="native.pdb")
>>> print(tm_exe)
/usr/bin/TMscore model.pdb native.pdb

2. Run TM-score to compare two complex structures with multiple chains

>>> from mbkit.apps import TMscore
>>> tm_exe = TMscore.TMscoreCommandline(
...     "/usr/bin/TMscore", complex=True, model="model.pdb", native="native.pdb")
>>> print(tm_exe)
/usr/bin/TMscore -c model.pdb native.pdb

3. TM-score normalized with an assigned scale d0 e.g. 5 A

>>> from mbkit.apps import TMscore
>>> tm_exe = TMscore.TMscoreCommandline(
...     "/usr/bin/TMscore", norm_scale=5, model="model.pdb", native="native.pdb")
>>> print(tm_exe)
/usr/bin/TMscore model native -d 5

4. TM-score normalized by a specific length, e.g. 120 AA

>>> from mbkit.apps import TMscore
>>> tm_exe = TMscore.TMscoreCommandline(
...     "/usr/bin/TMscore", norm_length=5, model="model.pdb", native="native.pdb")
>>> print(tm_exe)
/usr/bin/TMscore model native -l 120

Citations
---------
.. [#] Zhang Y, Skolnick J. (2004). Scoring function for automated assessment
   of protein structure template quality, Proteins, 57: 702-710.

"""

__author__ = "Felix Simkovic"
__date__ = "20 Feb 2017"
__version__ = "0.1"

from mbkit.apps import AbstractCommandline
from mbkit.apps import Argument
from mbkit.apps import Option
from mbkit.apps import Switch


class TMscoreCommandline(AbstractCommandline):

    def __init__(self, cmd='TMscore', **kwargs):
        self.parameters = [
            Switch(['-c', 'complex'],
                   'Run TM-score to compare two complex structures with multiple chains'),
            Option(['-d', 'norm_scale'],
                   'TM-score normalized with an assigned scale d0',
                    equate=False),
            Option(['-l', 'norm_length'],
                   'TM-score normalized by a specific length',
                   equate=False),

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
