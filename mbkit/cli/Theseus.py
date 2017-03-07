"""Python wrapper module for the Theseus binary"""

__author__ = "Felix Simkovic"
__date__ = "28 Aug 2016"
__version__ = 0.1

from mbkit.cli import AbstractCommandline
from mbkit.cli import ArgumentList
from mbkit.cli import Option
from mbkit.cli import Switch


class TheseusCommandline(AbstractCommandline):
    """Python wrapper module for the Theseus [#]_ [#]_ binary

    THESEUS: Maximum likelihood multiple superpositioning

    .. [#] Theobald DL, Steindel PA (2012). Optimal simultaneous superpositioning of
           multiple structures with missing data. Bioinformatics 28(15), 1972-1979.

    .. [#] Theobald DL, Wuttke DS (2008). Accurate structural correlations from maximum
           likelihood superpositions. PLOS Computational Biology 4(2), e43.

    Examples
    --------

    >>> from mbkit.cli import Theseus
    >>> theseus_exe = Theseus.TheseusCommandline(pdb_files="model1.pdb model2.pdb model3.pdb")
    >>> print(theseus_exe)
    theseus model1.pdb model2.pdb model3.pdb

    """
    def __init__(self, cmd='theseus', **kwargs):

        if 'pdb_files' in kwargs and (isinstance(kwargs['pdb_files'], list) or isinstance(kwargs['pdb_files'], tuple)):
            kwargs['pdb_files'] = " ".join(kwargs['pdb_files'])

        self.parameters = [
            Option(['-a', 'atoms'],
                   "atoms to include in superposition"
                   "    0 = alpha carbons and phosphorous atoms"
                   "    1 = backbone"
                   "    2 = all"
                   "    3 = alpha and beta carbons"
                   "    4 = all heavy atoms (all but hydrogens)"
                   "         or"
                   "    a colon-delimited string specifying the atom-types PDB-style"
                   "e.g., -a ' CA  : N'"
                   "selects the alpha carbons and backone nitrogens",
                   equate=False),
            Switch(['-f', 'first_model'],
                   "only read the first model of a multi-model PDB file"),
            Option(['-i', 'niteration'],
                   "maximum iterations {200}",
                   equate=False),
            Switch(['-l', 'least_square'],
                   "superimpose with conventional least squares method"),
            Option(['-s', 'residues_incl'],
                   "residues to select (e.g. -s15-45:50-55) {all}",
                   equate=False),
            Option(['-S', 'residues_excl'],
                   "residues to exclude (e.g. -S15-45:50-55) {none}",
                   equate=False),
            Switch(['-v' 'ml_variance_weighting'],
                   "use ML variance weighting (no correlations)"),

            # Input/output options
            Switch(['--amber', 'amber'],
                   "for reading AMBER8 formatted PDB files"),
            Option(['-A', 'alignment'],
                   "sequence alignment file to use as a guide (CLUSTAL or A2M format)",
                   equate=False,
                   filename=True),
            Switch(['-F', 'print_fasta'],
                   "print FASTA files of the sequences in PDB files and quit"),
            Switch(['-I', 'no_superposition'],
                   "just calculate statistics for input file (don't superposition)"),
            Option(['-M', 'sequence_map'],
                   "file that maps sequences in the alignment file to PDB files",
                   equate=False,
                   filename=True),
            Option(['-r', 'root_name'],
                   'root name for output files {theseus}',
                   equare=False),
            
            # Principal components analysis
            Switch(['-C', 'covariance_matrix'],
                   "use covariance matrix for PCA (correlation matrix is default)"),
            Option(['-P', 'principal_components'],
                   "# of principal components to calculate {0}",
                   equate=False),
            
            # Morphometrics
            Switch(['-d', 'scale_factors'],
                   "calculate scale factors (for morphometrics)"),
            Switch(['-q', 'rohlf_files'],
                   "read and write Rohlf TPS morphometric landmark files"),
                   
            
            ArgumentList(['pdb_files'],
                         'Input pdb files',
                         filename=True,
                         is_required=True),
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)

