# MrKit
Molecular Replacement ToolKit

### Installation

    git clone https://github.com/rigdenlab/mrkit.git
    cd mrkit
    ccp4-python setup.py install --prefix $CCP4

This will install the MrKit into your CCP4 installation.

### Development

If you would like to install MrKit in development mode, execute the following:

    git clone https://github.com/rigdenlab/mrkit.git
    cd mrkit
    ccp4-python setup.py develop --prefix $CCP4

This will link this version into the root of your CCP4 installation. Therefore, you do not need to re-install it after every change.

### Testing

    python setup.py test

This command will collect all unittests and execute them.

### Contributors

- Jens Thomas
- Ronan Keegan
- Adam Simpkin
- Felix Simkovic
- Daniel Rigden
