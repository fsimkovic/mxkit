"""Python wrapper module for the Refmac binary"""

__author__ = "Adam Simpkin"
__date__ = "15 Mar 2017"
__version__ = 0.1

from mbkit.cli import AbstractCommandline
from mbkit.cli import Argument
from mbkit.cli import Option
from mbkit.cli import Switch

class RefmacCommandline(AbstractCommandline):
    """Python wrapper for the Refmac [#]_ binary

    Description
    -----------
    Refmac [#]_ is a program designed for the REFinement of MACromolecular structures. Refmac is part of the CCP4
    software suite. CCP4 is needed for running this wrapper. It can be downloaded from www.ccp4.ac.uk.

    .. [#] A.A.Vagin and E.J.Dodson, Refinement of Macromolecular Structures by the Maximum-Likelihood method.,
       Acta Cryst. D53, 240-255.

    Examples
    --------
    1. Restrained refinement with overall B-factor refinement. Method is sparse matrix method.
    >>> from mbkit.cli import Refmac

    2. Unrestrained refinement by maximum likelihood method
    >>> from mbkit.cli import Refmac

    3. Idealization. Method of minimization is conjugate gradient method.
    >>> from mbkit.cli import Refmac

    4. Restrained refinement with partial contribution from hydrogens.
    >>> from mbkit.cli import Refmac

    5. Restrained refinement with maximum likelihood method etc. 3 angstrom data requires fixing of protein and
    Babinet's BULK B value. In these cases it is better to use TLS refinement before individual atomic refinement.
    >>> from mbkit.cli import Refmac

    6a. Example of rigid body refinement in refmac. Ordinary case with several domains.
    >>> from mbkit.cli import Refmac

    6b. Same problem but now using experimental phases.
    >>> from mbkit.cli import Refmac

    7. Example of using experimental phase information. Very bad model (RMS error 2 angstroms)
    >>> from mbkit.cli import Refmac

    8. Example of refinement of individual anisotropic B values. Hydrogens must be included. They will be used for
    geometry gradient and second derivatives and structure factor calculatation. But they do not contribute to X-ray
    gradients and second derivatives.
    >>> from mbkit.cli import Refmac

    9. Example of TLS refinement prior to individual isotropic B value and positional parameters.
    >>> from mbkit.cli import Refmac
    """

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

        self.stdin = [
            # Principal X-ray keywords
            Argument(['LABIN'],
                     "Column labels from hklin",
                     filename=False,
                     is_required=True),
            Argument(['NCYC'],
                     "Number of refinement cycles",
                     filename=False,
                     is_required=False),
            Argument(['REFI'],
                     "Type of refinement",
                     filename=False,
                     is_required=False),
            Argument(['SCAL'],
                     "Scaling of calculated and observed structure factors",
                     filename=False,
                     is_required=False),
            Argument(['SOLVENT'],
                     "Solvent content",
                     filename=False,
                     is_required=False),
            Argument(['WEIG'],
                     "Weighting of the x-ray and geometric parts",
                     filename=False,
                     is_required=False),

            # General X-ray keywords
            Argument(['BINS'],
                     "Number of resolution bins",
                     filename=False,
                     is_required=False),
            Argument(['RANGE'],
                     "Number of resolution bins",
                     filename=False,
                     is_required=False),
            Argument(['BLIM'],
                     "Limits of allowed B value range",
                     filename=False,
                     is_required=False),
            Argument(['CELL'],
                     "Cell parameters",
                     filename=False,
                     is_required=False),
            Argument(['DAMP'],
                     "Factors to scale down shifts at every cycle",
                     filename=False,
                     is_required=False),
            Argument(['END'],
                     "End of keywords",
                     filename=False,
                     is_required=False),
            Argument(['GO'],
                     "End of keywords",
                     filename=False,
                     is_required=False),
            Argument(['LABO'],
                     "Output MTZ labels",
                     filename=False,
                     is_required=False),
            Argument(['MODE'],
                     "Refinement mode",
                     filename=False,
                     is_required=False),
            Argument(['MONI'],
                     "Levels of monitoried statistics",
                     filename=False,
                     is_required=False),
            Argument(['PHASE'],
                     "Parameters for the phased refinement",
                     filename=False,
                     is_required=False),
            Argument(['RIGI'],
                     "Parameters for the rigid body refinement",
                     filename=False,
                     is_required=False),
            Argument(['SCPA'],
                     "For scaling of the external partial structure factors",
                     filename=False,
                     is_required=False),
            Argument(['SHAN'],
                     "Shannon factor to controp grid spacings",
                     filename=False,
                     is_required=False),
            Argument(['SYMM'],
                     "Symmetry",
                     filename=False,
                     is_required=False),
            Argument(['TLSC'],
                     "Number of TLC cycles",
                     filename=False,
                     is_required=False),

            # Restraints keywords
            Argument(['ANGL'],
                     "Restrains on bond angles",
                     filename=False,
                     is_required=False),
            Argument(['BFAC'],
                     "Restrains on B values",
                     filename=False,
                     is_required=False),
            Argument(['TEMP'],
                     "restrains on B values",
                     filename=False,
                     is_required=False),
            Argument(['CHIR'],
                     "Restraints on chiral volumes",
                     filename=False,
                     is_required=False),
            Argument(['DIST'],
                     "Restraints on bond distances",
                     filename=False,
                     is_required=False),
            Argument(['HOLD'],
                     "Restrains against excessive shifts",
                     filename=False,
                     is_required=False),
            Argument(['MAKE'],
                     "Controls making restraints and checking coordinates against dictionary",
                     filename=False,
                     is_required=False),
            Argument(['NCSR'],
                     "Restrains on non-crystallographic symmetry",
                     filename=False,
                     is_required=False),
            Argument(['NONX'],
                     "Restrains on non-crystallographic symmetry",
                     filename=False,
                     is_required=False),
            Argument(['PLAN'],
                     "Restraints on planarity",
                     filename=False,
                     is_required=False),
            Argument(['RBON'],
                     "Rigid bond restraints on the anisotropic B values of bonded atoms",
                     filename=False,
                     is_required=False),
            Argument(['SPHE'],
                     "Sphericity restraints on the anisotropic B values",
                     filename=False,
                     is_required=False),
            Argument(['TORS'],
                     "Restraints on the torsion angles",
                     filename=False,
                     is_required=False),
            Argument(['VDWR'],
                     "Restraints on VDW repulsions",
                     filename=False,
                     is_required=False),
            Argument(['VAND'],
                     "Restraints on VDW repulsions",
                     filename=False,
                     is_required=False),

            # Harvesting keywords
            Argument(['PNAME'],
                     "Project name",
                     filename=False,
                     is_required=False),
            Argument(['DNAME'],
                     "Dataset name",
                     filename=False,
                     is_required=False),
            Argument(['PRIVATE'],
                     "Set the directory permisions to 700, read/write/execute privileges for user only",
                     filename=False,
                     is_required=False),
            Argument(['USECWD'],
                     "Write the deposit file to current working directory",
                     filename=False,
                     is_required=False),
            Argument(['RSIZE'],
                     "Maxium width of a row in the deposit file",
                     filename=False,
                     is_required=False),
            Argument(['NOHARVEST'],
                     "Do not write out a deposit file",
                     filename=False,
                     is_required=False),

            # Additional keywords
            Argument(['twin'],
                     "Twin refinement",
                     filename=False,
                     is_required=False),
            Argument(['mapc'],
                     "Map calculation",
                     filename=False,
                     is_required=False),
            Argument(['anom'],
                     "Map coefficients",
                     filename=False,
                     is_required=False),
            Argument(['exte dist'],
                     "external restraints",
                     filename=False,
                     is_required=False),
            Argument(['@'],
                     "file containing external restraints",
                     filename=True,
                     is_required=False),
            Argument(['libcheck'],
                     "",
                     filename=True,
                     is_required=False),
        ]

        AbstractCommandline.__init__(self, cmd, **kwargs)