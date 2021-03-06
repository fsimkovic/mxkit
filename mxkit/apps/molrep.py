"""Python wrapper for the Molrep [#]_ binary

Description
-----------
Molrep [#]_ is an automated molecular replacement (MR) program for attempting to 
position a known structure in the unit cell of a target structure to attempt to give 
a first estimate of phases for the unknown target. Apart from the basic MR function it
has several additional features that can be used to assist the MR process. Molrep is 
part of the CCP4 software suite. CCP4 is needed for running this wrapper. It can be 
downloaded from www.ccp4.ac.uk.

Examples
--------
1. Run Molrep to do basic molecular replacement (RF + TF):

>>> from mxkit.apps import molrep
>>> molrep_exe = molrep.MolrepCommandline(
...     "/usr/bin/molrep", hklin="data.mtz", xyzin="model.pdb")
>>> print(molrep_exe)
/usr/bin/molrep -f data.mtz -m model.pdb

2. Run Molrep to do basic molecular replacement (RF + TF) with fixed model:

>>> from mxkit.apps import molrep
>>> molrep_exe = molrep.MolrepCommandline(
...     "/usr/bin/molrep", hklin="data.mtz", xyzin="model.pdb", fixed_xyzin="model2.pdb")
>>> print(molrep_exe)
/usr/bin/molrep -f data.mtz -m model.pdb -mx model2.pdb

3. Run Molrep to do basic MR (RF + TF) with input sequence and redirect output and scratch files:

>>> from mxkit.apps import molrep
>>> molrep_exe = molrep.MolrepCommandline(
...     "/usr/bin/molrep", hklin="data.mtz", xyzin="model.pdb", seqin="sequence.fasta", outDir="out/", outScr="scr/")
>>> print(molrep_exe)
/usr/bin/molrep -f data.mtz -m model.pdb -s sequence.fasta -po out/ -ps scr/

4. Run Molrep to do self rotation function:

>>> from mxkit.apps import molrep
>>> molrep_exe = molrep.MolrepCommandline(
...     "/usr/bin/molrep", hklin="data.mtz")
>>> print(molrep_exe)
/usr/bin/molrep -f data.mtz

5. Run Molrep to do multicopy search using one model:

>>> from mxkit.apps import molrep
>>> molrep_exe = molrep.MolrepCommandline(
...     "/usr/bin/molrep", hklin="data.mtz", xyzin="model.pdb", xyzin2="model.pdb")
>>> print(molrep_exe)
/usr/bin/molrep -f data.mtz -m model.pdb -m2 model.pdb

6. Run Molrep to do multicopy search using two models:

>>> from mxkit.apps import molrep
>>> molrep_exe = molrep.MolrepCommandline(
...     "/usr/bin/molrep", hklin="data.mtz", xyzin="model.pdb", xyzin2="model2.pdb")
>>> print(molrep_exe)
/usr/bin/molrep -f data.mtz -m model.pdb -m2 model2.pdb

7. Run Molrep to fit two atomic models:

>>> from mxkit.apps import molrep
>>> molrep_exe = molrep.MolrepCommandline(
...     "/usr/bin/molrep", xyzin="model.pdb", fixed_xyzin="model2.pdb")
>>> print(molrep_exe)
/usr/bin/molrep -m model.pdb -mx model2.pdb

8. Run Molrep to rigid body refinement:

>>> from mxkit.apps import molrep
>>> molrep_exe = molrep.MolrepCommandline(
...     "/usr/bin/molrep", hklin="data.mtz", fixed_xyzin="model2.pdb")
>>> print(molrep_exe)
/usr/bin/molrep -f data.mtz -mx model.pdb

9. Run Molrep to do basic MR (RF + TF) with keyword file input:

>>> from mxkit.apps import molrep
>>> molrep_exe = molrep.MolrepCommandline(
...     "/usr/bin/molrep", hklin="data.mtz", xyzin="model.pdb", keyin="keywords.txt")
>>> print(molrep_exe)
/usr/bin/molrep -f data.mtz -m model.pdb -k keywords.txt

10. Run Molrep to fit model to EM map:

>>> from mxkit.apps import molrep
>>> molrep_exe = molrep.MolrepCommandline(
...     "/usr/bin/molrep", hklin="em.map", xyzin="model.pdb")
>>> print(molrep_exe)
/usr/bin/molrep -f em.map -m model.pdb 

11. Run Molrep to do basic molecular replacement (RF + TF) with input through stdin:

>>> from mxkit.apps import molrep
>>> molrep_exe = molrep.MolrepCommandline(
...     "/usr/bin/molrep", interactive=True, hklin="data.mtz", xyzin="model.pdb")
>>> print(molrep_exe)
/usr/bin/molrep -f data.mtz -m model.pdb -i

Citations
---------
.. [#] A.Vagin, A.Teplyakov, MOLREP: an automated program for molecular replacement.,
   J. Appl. Cryst. (1997) 30, 1022-1025.

"""

__author__ = "Felix Simkovic & Ronan Keegan"
__date__ = "07 Mar 2017"
__version__ = "0.1"

from mxkit.apps import AbstractCommandline
from mxkit.apps import Argument
from mxkit.apps import Option
from mxkit.apps import Switch


class MolrepCommandline(AbstractCommandline):

    def __init__(self, cmd='molrep', **kwargs):
        self.parameters = [
            Switch(['-h', 'help'],
                   ''),
            Switch(['-i', 'interactive'],
                   ''),

            Option(['-f', 'hklin'],
                   '',
                   equate=False,
                   filename=True),
            Option(['-m', 'xyzin'],
                   '',
                   equate=False,
                   filename=True),
            Option(['-m2', 'xyzin2'],
                   '',
                   equate=False,
                   filename=True),
            Option(['-mx', 'fixed_xyzin'],
                   '',
                   equate=False,
                   filename=True),
            Option(['-s', 'seqin'],
                   '',
                   equate=False,
                   filename=True),
            Option(['-s2', 'seqin2'],
                   '',
                   equate=False,
                   filename=True),
            Option(['-k', 'keyin'],
                   '',
                   equate=False,
                   filename=True),
            Option(['-po', 'out_dir'],
                   '',
                   equate=False),
            Option(['-ps', 'out_scr'],
                   '',
                   equate=False),
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)
