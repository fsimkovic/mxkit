"""Storage for chemical information"""

__author__ = "Felix Simkovic & Adam Simpkin"
__date__ = "26 Apr 2017"
__version__ = "0.1"

__all__ = ['atomic_composition', 'periodic_table']


class AtomicComposition(object):

    def __init__(self):
        acids = [
            ('ALA', 'A', {'H': 5, 'C': 3, 'N': 1, 'O': 1}),
            ('CYS', 'C', {'H': 5, 'C': 3, 'N': 1, 'O': 1, 'S': 1}),
            ('ASP', 'D', {'H': 4, 'C': 4, 'N': 1, 'O': 3}),
            ('GLU', 'E', {'H': 6, 'C': 5, 'N': 1, 'O': 3}),
            ('PHE', 'F', {'H': 9, 'C': 9, 'N': 1, 'O': 1}),
            ('GLY', 'G', {'H': 3, 'C': 2, 'N': 1, 'O': 1}),
            ('HIS', 'H', {'H': 8, 'C': 6, 'N': 1, 'O': 1}),
            ('ILE', 'I', {'H': 11, 'C': 6, 'N': 1, 'O': 1}),
            ('LYS', 'K', {'H': 13, 'C': 6, 'N': 2, 'O': 1}),
            ('LEU', 'L', {'H': 11, 'C': 6, 'N': 1, 'O': 1}),
            ('MET', 'M', {'H': 9, 'C': 5, 'N': 1, 'O': 1, 'S': 1}),
            ('ASN', 'N', {'H': 6, 'C': 4, 'N': 2, 'O': 2}),
            ('PRO', 'P', {'H': 7, 'C': 5, 'N': 1, 'O': 1}),
            ('GLN', 'Q', {'H': 8, 'C': 5, 'N': 2, 'O': 2}),
            ('ARG', 'R', {'H': 13, 'C': 6, 'N': 4, 'O': 1}),
            ('SER', 'S', {'H': 5, 'C': 3, 'N': 1, 'O': 2}),
            ('THR', 'T', {'H': 7, 'C': 4, 'N': 1, 'O': 2}),
            ('VAL', 'V', {'H': 9, 'C': 5, 'N': 1, 'O': 1}),
            ('TRP', 'W', {'H': 10, 'C': 11, 'N': 2, 'O': 1}),
            ('TYR', 'Y', {'H': 9, 'C': 9, 'N': 1, 'O': 2}),
        ]
        self._aadict = {}
        for three, one, prop in acids:
            self._aadict[three] = self._aadict[one] = _AminoAcidComposition(**prop)

    def __getitem__(self, k):
        if k.upper() in self._aadict:
            return self._aadict[k.upper()]
        return None


class _AminoAcidComposition(object):

    __slots__ = ['H', 'C', 'N', 'O', 'S']

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__, ", ".join(["{0}={1}".format(k, v) for k, v in self.__dict__.items()])
        )


class PeriodicTable(object):

    def __init__(self):
        atoms = [
            ('Hydrogen', 'H', {'atomic_number': 1, 'atomic_mass': 1.008, 'group': 'Non-metal'}),
            ('Helium', 'He', {'atomic_number': 2, 'atomic_mass': 4.003, 'group': 'Nobel gas'}),
            ('Lithium', 'Li', {'atomic_number': 3, 'atomic_mass': 6.941, 'group': 'Alkali metal'}),
            ('Beryllium', 'Be', {'atomic_number': 4, 'atomic_mass': 9.012, 'group': 'Alkaline earth'}),
            ('Boron', 'B', {'atomic_number': 5, 'atomic_mass': 10.811, 'group': 'Semi-metal'}),
            ('Carbon', 'C', {'atomic_number': 6, 'atomic_mass': 12.011, 'group': 'Non-metal'}),
            ('Nitrogen', 'N', {'atomic_number': 7, 'atomic_mass': 14.007, 'group': 'Non-metal'}),
            ('Oxygen', 'O', {'atomic_number': 8, 'atomic_mass': 15.999, 'group': 'Non-metal'}),
            ('Fluorine', 'F', {'atomic_number': 9, 'atomic_mass': 18.998, 'group': 'Halogen'}),
            ('Neon', 'Ne', {'atomic_number': 10, 'atomic_mass': 20.180, 'group':  'Nobelgas'}),
            ('Sodium', 'Na', {'atomic_number': 11, 'atomic_mass': 22.990, 'group': 'Alkali metal'}),
            ('Magnesium', 'Mg', {'atomic_number': 12, 'atomic_mass': 24.305, 'group': 'Alkaline earth'}),
            ('Aluminium', 'Al', {'atomic_number': 13, 'atomic_mass': 26.982, 'group': 'Basic metal'}),
            ('Silicon', 'Si', {'atomic_number': 14, 'atomic_mass': 28.086, 'group': 'Semi-metal'}),
            ('Phosphorus', 'P', {'atomic_number': 15, 'atomic_mass': 30.974, 'group': 'Non-metal'}),
            ('Sulphur', 'S', {'atomic_number': 16, 'atomic_mass': 32.066, 'group': 'Non-metal'}),
            ('Chlorine', 'Cl', {'atomic_number': 17, 'atomic_mass': 35.453, 'group': 'Halogen'}),
            ('Argon', 'Ar', {'atomic_number': 18, 'atomic_mass': 39.948, 'group': 'Nobel gas'}),
            ('Potassium', 'K', {'atomic_number': 19, 'atomic_mass': 39.098, 'group': 'Alkali metal'}),
            ('Calcium', 'Ca', {'atomic_number': 20, 'atomic_mass': 40.078, 'group': 'Alkaline earth'}),
            ('Scandium', 'Sc', {'atomic_number': 21, 'atomic_mass': 44.956, 'group': 'Transition metal'}),
            ('Titanium', 'Ti', {'atomic_number': 22, 'atomic_mass': 47.880, 'group': 'Transition metal'}),
            ('Vanadium', 'V', {'atomic_number': 23, 'atomic_mass': 50.942, 'group': 'Transition metal'}),
            ('Chromium', 'Cr', {'atomic_number': 24, 'atomic_mass': 51.996, 'group': 'Transition metal'}),
            ('Manganese', 'Mn', {'atomic_number': 25, 'atomic_mass': 54.938, 'group': 'Transition metal'}),
            ('Iron', 'Fe', {'atomic_number': 26, 'atomic_mass': 55.933, 'group': 'Transition metal'}),
            ('Cobalt', 'Co', {'atomic_number': 27, 'atomic_mass': 58.933, 'group': 'Transition metal'}),
            ('Nickle', 'Ni', {'atomic_number': 28, 'atomic_mass': 58.693, 'group': 'Transition metal'}),
            ('Copper', 'Cu', {'atomic_number': 29, 'atomic_mass': 63.546, 'group': 'Transition metal'}),
            ('Zinc', 'Zn', {'atomic_number': 30, 'atomic_mass': 65.390, 'group': 'Transition metal'}),
            ('Gallium', 'Ga', {'atomic_number': 31, 'atomic_mass': 69.732, 'group': 'Basic metal'}),
            ('Germanium', 'Ge', {'atomic_number': 32, 'atomic_mass': 72.610, 'group': 'Semi-metal'}),
            ('Arsenic', 'As', {'atomic_number': 33, 'atomic_mass': 74.922, 'group': 'Semi-metal'}),
            ('Selenium', 'Se', {'atomic_number': 34, 'atomic_mass': 78.972, 'group': 'Non-metal'}),
            ('Bromine', 'Br', {'atomic_number': 35, 'atomic_mass': 79.904, 'group': 'Halogen'}),
            ('Krypton', 'Kr', {'atomic_number': 36, 'atomic_mass': 84.800, 'group': 'Nobel gas'}),
            ('Rubidium', 'Rb', {'atomic_number': 37, 'atomic_mass': 84.468, 'group': 'Alkali metal'}),
            ('Strontium', 'Sr', {'atomic_number': 38, 'atomic_mass': 87.620, 'group': 'Alkaline earth'}),
            ('Yttrium', 'Y', {'atomic_number': 39, 'atomic_mass': 88.906, 'group': 'Transition metal'}),
            ('Zirconium', 'Zr', {'atomic_number': 40, 'atomic_mass': 91.224, 'group': 'Transition metal'}),
            ('Niobium', 'Nb', {'atomic_number': 41, 'atomic_mass': 92.906, 'group': 'Transition metal'}),
            ('Molybdenum', 'Mo', {'atomic_number': 42, 'atomic_mass': 95.950, 'group': 'Transition metal'}),
            ('Technetium', 'Tc', {'atomic_number': 43, 'atomic_mass': 98.907, 'group': 'Transition metal'}),
            ('Ruthenium', 'Ru', {'atomic_number': 44, 'atomic_mass': 101.070, 'group': 'Transition metal'}),
            ('Rhodium', 'Rh', {'atomic_number': 45, 'atomic_mass': 102.906, 'group': 'Transition metal'}),
            ('Palladium', 'Pd', {'atomic_number': 46, 'atomic_mass': 106.420, 'group': 'Transition metal'}),
            ('Silver', 'Ag', {'atomic_number': 47, 'atomic_mass': 107.868, 'group': 'Transition metal'}),
            ('Cadmium', 'Cd', {'atomic_number': 48, 'atomic_mass': 112.411, 'group': 'Transition metal'}),
            ('Indium', 'In', {'atomic_number': 49, 'atomic_mass': 114.818, 'group': 'Basic metal'}),
            ('Tin', 'Sn', {'atomic_number': 50, 'atomic_mass': 118.710, 'group': 'Basic metal'}),
            ('Antimony', 'Sb', {'atomic_number': 51, 'atomic_mass': 121.760, 'group': 'Semi-metal'}),
            ('Tellurium', 'Te', {'atomic_number': 52, 'atomic_mass': 127.600, 'group': 'Semi-metal'}),
            ('Iodine', 'I', {'atomic_number': 53, 'atomic_mass': 126.904, 'group': 'Halogen'}),
            ('Xenon', 'Xe', {'atomic_number': 54, 'atomic_mass': 131.290, 'group': 'Nobel gas'}),
            ('Cesium', 'Cs', {'atomic_number': 55, 'atomic_mass': 132.905, 'group': 'Alkali metal'}),
            ('Barium', 'Ba', {'atomic_number': 56, 'atomic_mass': 137.327, 'group': 'Alkaline earth'}),
            ('Lanthanum', 'La', {'atomic_number': 57, 'atomic_mass': 138.906, 'group': 'Lanthanide'}),
            ('Cerium', 'Ce', {'atomic_number': 58, 'atomic_mass': 140.115, 'group': 'Lanthanide'}),
            ('Praseodymium', 'Pr', {'atomic_number': 59, 'atomic_mass': 140.908, 'group': 'Lanthanide'}),
            ('Neodymium', 'Nd', {'atomic_number': 60, 'atomic_mass': 144.240, 'group': 'Lanthanide'}),
            ('Promethium', 'Pm', {'atomic_number': 61, 'atomic_mass': 144.913, 'group': 'Lanthanide'}),
            ('Samarium', 'Sm', {'atomic_number': 62, 'atomic_mass': 150.360, 'group': 'Lanthanide'}),
            ('Europium', 'Eu', {'atomic_number': 63, 'atomic_mass': 151.966, 'group': 'Lanthanide'}),
            ('Gadolinium', 'Gd', {'atomic_number': 64, 'atomic_mass': 157.250, 'group': 'Lanthanide'}),
            ('Terbium', 'Tb', {'atomic_number': 65, 'atomic_mass': 158.925, 'group': 'Lanthanide'}),
            ('Dysprosium', 'Dy', {'atomic_number': 66, 'atomic_mass': 162.50, 'group': 'Lanthanide'}),
            ('Holmium', 'Ho', {'atomic_number': 67, 'atomic_mass': 164.930, 'group': 'Lanthanide'}),
            ('Erbium', 'Er', {'atomic_number': 68, 'atomic_mass': 167.260, 'group': 'Lanthanide'}),
            ('Thulium', 'Tm', {'atomic_number': 69, 'atomic_mass': 168.934, 'group': 'Lanthanide'}),
            ('Ytterbium', 'Yb', {'atomic_number': 70, 'atomic_mass': 173.04, 'group': 'Lanthanide'}),
            ('Lutetium', 'Lu', {'atomic_number': 71, 'atomic_mass': 174.967, 'group': 'Lanthanide'}),
            ('Hafnium', 'Hf', {'atomic_number': 72, 'atomic_mass': 178.490, 'group': 'Transition metal'}),
            ('Tantalum', 'Ta', {'atomic_number': 73, 'atomic_mass': 180.948, 'group': 'Transition metal'}),
            ('Tungsten', 'W', {'atomic_number': 74, 'atomic_mass': 183.850, 'group': 'Transition metal'}),
            ('Rhenium', 'Re', {'atomic_number': 75, 'atomic_mass': 186.207, 'group': 'Transition metal'}),
            ('Osmium', 'Os', {'atomic_number': 76, 'atomic_mass': 190.230, 'group': 'Transition metal'}),
            ('Iridium', 'Ir', {'atomic_number': 77, 'atomic_mass': 192.220, 'group': 'Transition metal'}),
            ('Platinum', 'Pt', {'atomic_number': 78, 'atomic_mass': 195.08, 'group': 'Transition metal'}),
            ('Gold', 'Au', {'atomic_number': 79, 'atomic_mass': 196.967, 'group': 'Transition metal'}),
            ('Mercury', 'Hg', {'atomic_number': 80, 'atomic_mass': 200.590, 'group': 'Transition metal'}),
            ('Thallium', 'Tl', {'atomic_number': 81, 'atomic_mass': 204.383, 'group': 'Basic metal'}),
            ('Lead', 'Pb', {'atomic_number': 82, 'atomic_mass': 207.200, 'group': 'Basic metal'}),
            ('Bismuth', 'Bi', {'atomic_number': 83, 'atomic_mass': 208.980, 'group': 'Basic metal'}),
            ('Polonium', 'Po', {'atomic_number': 84, 'atomic_mass': 208.982, 'group': 'Semi-metal'}),
            ('Astatine', 'At', {'atomic_number': 85, 'atomic_mass': 209.987, 'group': 'Halogen'}),
            ('Radon', 'Rn', {'atomic_number': 86, 'atomic_mass': 222.018, 'group': 'Nobel gas'}),
            ('Francium', 'Fr', {'atomic_number': 87, 'atomic_mass': 223.020, 'group': 'Alkali metal'}),
            ('Radium', 'Ra', {'atomic_number': 88, 'atomic_mass': 226.025, 'group': 'Alkaline earth'}),
            ('Actinium', 'Ac', {'atomic_number': 89, 'atomic_mass': 227.028, 'group': 'Actinide'}),
            ('Thorium', 'Th', {'atomic_number': 90, 'atomic_mass': 232.038, 'group': 'Actinide'}),
            ('Protactinium', 'Pa', {'atomic_number': 91, 'atomic_mass': 231.036, 'group': 'Actinide'}),
            ('Uranium', 'U', {'atomic_number': 92, 'atomic_mass': 238.029, 'group': 'Actinide'}),
            ('Neptunium', 'Np', {'atomic_number': 93, 'atomic_mass': 237.048, 'group': 'Actinide'}),
            ('Plutonium', 'Pu', {'atomic_number': 94, 'atomic_mass': 244.064, 'group': 'Actinide'}),
            ('Americium', 'Am', {'atomic_number': 95, 'atomic_mass': 243.061, 'group': 'Actinide'}),
            ('Curium', 'Cm', {'atomic_number': 96, 'atomic_mass': 247.070, 'group': 'Actinide'}),
            ('Berkelium', 'Bk', {'atomic_number': 97, 'atomic_mass': 247.070, 'group': 'Actinide'}),
            ('Californium', 'Cf', {'atomic_number': 98, 'atomic_mass': 251.080, 'group': 'Actinide'}),
            ('Einsteinium', 'Es', {'atomic_number': 99, 'atomic_mass': 254.000, 'group': 'Actinide'}),
            ('Fermium', 'Fm', {'atomic_number': 100, 'atomic_mass': 257.095, 'group': 'Actinide'}),
            ('Mendelevium', 'Md', {'atomic_number': 101, 'atomic_mass': 258.100, 'group': 'Actinide'}),
            ('Nobelium', 'No', {'atomic_number': 102, 'atomic_mass': 259.101, 'group': 'Actinide'}),
            ('Lawrencium', 'Lr', {'atomic_number': 103, 'atomic_mass': 262.00, 'group': 'Actinide'}),
            ('Rutherfordium', 'Rf', {'atomic_number': 104, 'atomic_mass': 261.000, 'group': 'Transition metal'}),
            ('Dubnium', 'Db', {'atomic_number': 105, 'atomic_mass': 262.000, 'group': 'Transition metal'}),
            ('Seaborgium', 'Sg', {'atomic_number': 106, 'atomic_mass': 266.000, 'group': 'Transition metal'}),
            ('Bohrium', 'Bh', {'atomic_number': 107, 'atomic_mass': 264.000, 'group': 'Transition metal'}),
            ('Hassium', 'Hs', {'atomic_number': 108, 'atomic_mass': 269.000, 'group': 'Transition metal'}),
            ('Meitnerium', 'Mt', {'atomic_number': 109, 'atomic_mass': 268.000, 'group': 'Transition metal'}),
            ('Darmstadtium', 'Ds', {'atomic_number': 110, 'atomic_mass': 269.000, 'group': 'Transition metal'}),
            ('Roentgenium', 'Rg', {'atomic_number': 111, 'atomic_mass': 272.000, 'group': 'Transition metal'}),
            ('Copernicium', 'Cn', {'atomic_number': 112, 'atomic_mass': 277.000, 'group': 'Transition metal'}),
            ('Ununtrium', 'Uut', {'atomic_number': 113, 'atomic_mass': None, 'group': 'Basic metal'}),
            ('Flerovium', 'Fl', {'atomic_number': 114, 'atomic_mass': 289.000, 'group': 'Basic metal'}),
            ('Ununpentium', 'Uup', {'atomic_number': 115, 'atomic_mass': None, 'group': 'Basic metal'}),
            ('Livermorium', 'Lv', {'atomic_number': 116, 'atomic_mass': 298.000, 'group': 'Basic metal'}),
            ('Ununseptium', 'Uus', {'atomic_number': 117, 'atomic_mass': None, 'group': 'Halogen'}),
            ('Ununoctium', 'Uuo', {'atomic_number': 118, 'atomic_mass': None, 'group': 'Nobel gas'})
        ]

        self._atomdict = {}
        for name, code, prop in atoms:
            self._atomdict[name] = self._atomdict[code] = _AtomComposition(**prop)

    def __getitem__(self, k):
        if k.upper() in self._atomdict:
            return self._atomdict[k.upper()]
        return None


class _AtomComposition(object):

    __slots__ = ['atomic_number', 'atomic_mass', 'group']

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__, ", ".join(["{0}={1}".format(k, v) for k, v in self.__dict__.items()])
        )

# Instantiate some stuff here so we can call it immediately
atomic_composition = AtomicComposition()
periodic_table = PeriodicTable()