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

    1. Run Molrep to do basic molecular replacement (RF + TF):
    >>> from mbkit.cli import Molrep
    >>> molrep_exe = Molrep.MolrepCommandLine(
    ...     "/usr/bin/molrep", hklin="data.mtz", xyzin="model.pdb")
    >>> print(molrep_exe)
    /usr/bin/molrep -f data.mtz -m model.pdb

    2. Run Molrep to do basic molecular replacement (RF + TF) with fixed model:
    >>> from mbkit.cli import Molrep
    >>> molrep_exe = Molrep.MolrepCommandLine(
    ...     "/usr/bin/molrep", hklin="data.mtz", xyzin="model.pdb", fixed_xyzin="model2.pdb")
    >>> print(molrep_exe)
    /usr/bin/molrep -f data.mtz -m model.pdb -mx model2.pdb

    3. Run Molrep to do basic MR (RF + TF) with input sequence and redirect output and scratch files:
    >>> from mbkit.cli import Molrep
    >>> molrep_exe = Molrep.MolrepCommandLine(
    ...     "/usr/bin/molrep", hklin="data.mtz", xyzin="model.pdb", seqin="sequence.fasta", outDir="out/", outScr="scr/")
    >>> print(molrep_exe)
    /usr/bin/molrep -f data.mtz -m model.pdb -s sequence.fasta -po out/ -ps scr/



 #     Self rotation funtion
 # molrep -f file.mtz
 #
 #     multi-copy search, one model
 # molrep -f file.mtz -m model.pdb -m2 model.pdb
 #
 #     multi-copy search, two models
 # molrep -f file.mtz -m model1.pdb -m2 model2.pdb
 #
 #     Fitting two atomic models
 # molrep -m model1.pdb -mx model2.pdb
 #
 #     Rigid body refinement
 # molrep -f file.mtz  -mx model.pdb
 #
 #     Using keywords from file
 # molrep -f fobs.mtz -m model.pdb -k file_keywords
 #
 #     Using keywords interactivly: fitting a model to EM map
 # molrep -f em.map  -m model.pdb -i <CR>
 # nmon 4 <CR>
 # <CR>
 #



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
            Option(['-k', 'keyin'],
                   '',
                   equate=False,
                   filename=True),
            Option(['-po', 'outDir'],
                   '',
                   equate=False,
                   dirname=True),
            Option(['-ps', 'outScr'],
                   '',
                   equate=False,
                   dirname=True),

            #Argument(['model'],
            #         "Input model structure",
            #         filename=True,
            #         is_required=True),
            #Argument(['native'],
            #          "Input native structure",
            #          filename=True,
            #          is_required=True),
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)
