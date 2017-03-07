# MbKit
Molecular Biology ToolKit

### Installation

    git clone https://github.com/rigdenlab/mbkit.git
    cd mbkit
    ccp4-python setup.py install --prefix $CCP4

This will install the MbKit into your CCP4 installation.

### Development

If you would like to install MbKit in development mode, execute the following:

    git clone https://github.com/rigdenlab/mbkit.git
    cd mbkit
    ccp4-python setup.py develop --prefix $CCP4

This will link this version into the root of your CCP4 installation. Therefore, you do not need to re-install it after every change.

### Testing

    ccp4-python setup.py test

This command will collect all unittests and execute them.

### Contributors

- Jens Thomas
- Ronan Keegan
- Adam Simpkin
- Felix Simkovic
- Daniel Rigden
