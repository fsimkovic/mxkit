"""Python wrapper module for the Maxcluster binary"""

__author__ = "Felix Simkovic"
__date__ = "30 Aug 2016"
__version__ = "0.1"

from mrkit.cli import AbstractCommandline
from mrkit.cli import Option
from mrkit.cli import Switch


class MaxclusterCommandline(AbstractCommandline):
    """Python wrapper module for the Maxcluster [#]_ binary

    Description
    -----------
    MaxCluster [#]_ is a tool for Protein Structure Comparison and Clustering.
    It calculates MaxSub for PDB models / list of models and provides
    clustering routines for lists of models.

    .. [#] Alex Herbert at the Structural Bioinformatics Group, Imperial College, London.

    Examples
    --------
    The first option to use maxcluster is to compare two structures,
    i.e. an experiment and predicted structure:

    >>> from mrkit.cli import Maxcluster
    >>> maxcluster_exe = Maxcluster.MaxclusterCommandline(pdb_experiment="experiment.pdb", pdb_prediction="model.pdb")
    >>> print(maxcluster_exe)
    maxcluster -e experiment.pdb -p model.pdb

    ---
    A second option is to invoke maxcluster using a list of models
    in an all vs all comparisons. Just provide the list file in case
    you wish to run such a comparison:

    >>> from mrkit.cli import Maxcluster
    >>> maxcluster_exe = Maxcluster.MaxclusterCommandline(pdb_list="models.list")
    >>> print(maxcluster_exe)
    maxcluster -l models.list

    ---
    Finally, if you wish to compare a list of models against a single
    experiment structure, you can use the following syntax to do just that:

    >>> from mrkit.cli import Maxcluster
    >>> maxcluster_exe = Maxcluster.MaxclusterCommandline(pdb_list="models.list", pdb_experiment='experiment.pdb')
    >>> print(maxcluster_exe)
    maxcluster -l models.list -e experiment.pdb

    """
    def __init__(self, cmd='maxcluster', **kwargs):
        if not self.options_ok(**kwargs):
            msg = "Unknown combination: Please use one of the following:" \
                  "     -e [file]   PDB experiment" \
                  "     -p [file]   PDB prediction" \
                  " OR" \
                  "     -l [file]   File containing a list of PDB model fragments" \
                  " OR" \
                  "     -e [file]   PDB experiment" \
                  "     -l [file]   File containing a list of PDB model fragments"
            raise RuntimeError(msg)

        self.parameters = [
            Option(['-e', 'pdb_experiment'],
                   'PDB experiment',
                   equate=False,
                   filename=True),
            Option(['-p', 'pdb_prediction'],
                   'PDB prediction',
                   equate=False,
                   filename=True),
            Option(['-l', 'pdb_list'],
                   'File containing a list of PDB model fragments',
                   equate=False,
                   filename=True),

            # OPTIONS
            Option(['-L', 'log_level'],
                   'Log level (default is 4 for single MaxSub, 1 for lists)',
                   equate=False),
            Option(['-d', 'distance_cutoff'],
                   'The distance cut-off for search (default auto-calibrate)',
                   equate=False),
            Option(['-N', 'norm_length'],
                   'The normalisation length for TM score (default is length of experiment)',
                   equate=False),
            Switch(['-rmsd', 'rmsd'],
                   'Perform only RMSD fit'),
            Option(['-i', 'maxsubdom_iterations'],
                   'MaxSubDom iterations (default = 1)',
                   equate=False),
            Switch(['-in', 'sequence_independent'],
                   'Sequence independant mode'),

            # CLUSTERING OPTIONS
            Option(['-C', 'cluster_method'],
                    "Cluster method:"
                    "   0 - No clustering"
                    "   1 - Single linkage"
                    "   2 - Average linkage"
                    "   3 - Maximum linkage"
                    "   4 - Neighbour pairs (min size)"
                    "   5 - Neighbour pairs (absolute size)"
                    "(default = 5)",
                    equate=False),
            Option(['-T', 'init_cluster_threshold'],
                   'Initial clustering threshold (default RMSD = 4; MaxSub = 0.5)',
                   equate=False),
            Option(['-Tm', 'max_cluster_threshold'],
                   'Maximum clustering threshold (default RMSD = 8; MaxSub = 0.8)',
                   equate=False),
            Option(['-a', 'adj_cluster_threshold'],
                   'Clustering threshold adjustment (default RMSD = 0.2; MaxSub = 0.05)',
                   equate=False),
            Option(['-is', 'init_cluster_size'],
                   'Initial cluster size (default = 50)',
                   equate=False),
            Option(['-ms', 'min_cluster_size'],
                   'Minimum cluster size (default = 5)',
                   equate=False),
            Option(['-s', 'score_threshold'],
                   '3D-jury score threshold (default = 0.2)',
                   equate=False),
            Option(['-P', 'pair_threshold'],
                   '3D-jury pair threshold (default = 20)',
                   equate=False)

        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)

    @staticmethod
    def options_ok(**kwargs):
        """Check the parse options for maxcluster combinations"""

        # Middle option
        if 'pdb_list' in kwargs and not ('pdb_experiment' in kwargs or 'pdb_prediction' in kwargs):
            return True

        # Bottom option
        elif 'pdb_experiment' in kwargs and 'pdb_list' in kwargs and 'pdb_prediction' not in kwargs:
            return True

        # Top option
        elif 'pdb_experiment' in kwargs and 'pdb_prediction' in kwargs and 'pdb_list' not in kwargs:
            return True

        return False
