"""Python wrapper module for the Spicker binary"""

__author__ = "Felix Simkovic"
__date__ = "28 Aug 2016"
__version__ = "0.1"

from mrkit.cli import AbstractCommandline
from mrkit.cli import Argument
from mrkit.cli import ArgumentList


class SpickerCommandline(AbstractCommandline):
    """Python wrapper module for the Spicker [#]_ binary

    SPICKER [#]_ is a clustering algorithm to identify the near-native
    models from a pool of protein structure decoys.

    .. [#] Zhang Y, Skolnick J (2004). SPICKER: A Clustering Approach to
           Identify Near-Native Protein Folds. J Comp Chem 25, 865-871.

    Examples
    --------

    >>> from mrkit.cli import Spicker
    >>> spicker_exe = Spicker.SpickerCommandline(rmsinp='rmsinp', seqdat='seqdat', train='tra.in', reptra=['rep1.tra1'])
    >>> print(spicker_exe)
    spicker rmsinp seq.dat tra.in rep1.tra1

    """
    def __init__(self, cmd='spicker', **kwargs):
        self.parameters = [
            Argument(['rmsinp'],
                     'length of protein & piece for RMSD calculation'),
            Argument(['seqdat'],
                     'sequence file, for output of PDB models',
                     filename=True),
            Argument(['train'],
                     "list of trajectory names used for clustering"
                     "In the first line of 'tra.in', there are 3 parameters:"
                     " par1: number of decoy files"
                     " par2: 1, default cutoff, best for clustering decoys from "
                     "          template-based modeling;"
                     "      -1, cutoff based on variation, best for clustering"
                     "          decoys from ab initio modeling."
                     "      -2, cluster based on TM scores"
                     " par3: 1, select closc from all decoys; "
                     "      -1, closc from clustered decoys (slighly faster)"
                     "From second lines are file names which contain coordinates"
                     "of 3D structure decoys. All these files are mandatory. See"
                     "attached 'rep1.tra1' etc for the format of decoys.",
                     filename=True),
            ArgumentList(['reptra'],
                         "decoy files     which should have the "
                         "same name as those listed in 'tra.in'. In the first line, "
                         "the first number is the length of the decoy; the second "
                         "number is the energy of the decoy (if you donot know the "
                         "energy you can put any number there); the third and fourth "
                         "numbers are not necessary and useless. "
                         "Starting from the second line, the coordinates (x,y,z) of "
                         "C-alpha atoms are listed.",
                         filename=True),
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)
