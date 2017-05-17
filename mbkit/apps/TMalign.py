"""Python wrapper for the TMalign [#]_ binary

Description
-----------
TM-align [#]_ is an algorithm for sequence-order independent protein structure
comparisons. For two protein structures of unknown equivalence, TM-align
first generates optimized residue-to-residue alignment based on structural
similarity using dynamic programming iterations. An optimal superposition
of the two structures, as well as the TM-score value which scales the
structural similarity, will be returned. TM-score has the value in (0,1],
where 1 indicates a perfect match between two structures. Following strict
statistics of structures in the PDB, scores below 0.2 corresponds to
randomly chosen unrelated proteins whereas with a score higher than 0.5
assume generally the same fold in SCOP/CATH.

Examples
--------
>>> from mbkit.apps import TMalign
>>> tm_exe = TMalign.TMalignCommandline(chain1="model1.pdb", chain2="model2.pdb")
>>> print(tm_exe)
TMalign model1.pdb model2.pdb

Citations
---------
.. [#] Zhang Y, Skolnick J (2005). TM-align: A protein structure alignment algorithm
   based on TM-score , Nucleic Acids Research 33, 2302-2309.

"""

__author__ = "Felix Simkovic"
__date__ = "20 Feb 2017"
__version__ = "0.1"

from mbkit.apps import AbstractCommandline
from mbkit.apps import Argument
from mbkit.apps import Option
from mbkit.apps import Switch


class TMalignCommandline(AbstractCommandline):

    def __init__(self, cmd='TMalign', **kwargs):
        self.parameters = [
            Argument(['chain1'],
                     'first PDB structure',
                     filename=True,
                     is_required=True),
            Argument(['chain2'],
                     'second PDB structure',
                     filename=True,
                     is_required=True),

            Option(['-i', 'aln_in'],
                   'an alignment specified in fasta file',
                   equate=False,
                   filename=True),
            Option(['-I', 'aln_out'],
                   'stick the alignment to this file',
                   equate=False,
                   filename=True),

            Option(['-o', 'superposition'],
                   "output the superposition to 'TM.sup', 'TM.sup_all' and 'TM.sup_atm'",
                   equate=False,
                   filename=True),

            Switch(['-a', 'normalized'],
                   'TM-score normalized by the average length of two proteins'),

            Option(['-L', 'assigned_length'],
                   'TM-score normalized by an assigned length (>L_min)',
                   equate=False),
            Option(['-d', 'scale_factor'],
                   'TM-score scaled by an assigned d0',
                   equate=False),

            Option(['-m', 'rotation_matrix'],
                   'output TM-align rotation matrix',
                   equate=False,
                   filename=True),
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)
