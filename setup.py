"""MrKit - Molecular Replacement ToolKit"""

from setuptools import setup, find_packages
from distutils.util import convert_path
import glob

def get_version():
    # Credits to http://stackoverflow.com/a/24517154
    main_ns = {}
    ver_path = convert_path('mrkit/_version.py')
    with open(ver_path) as f_in:
        exec(f_in.read(), main_ns)
    return main_ns['__version__']

# Obtain the current version of ConKit
__version__ = get_version()

# Do the actual setup below
setup(
    name='mrkit',
    description=__doc__.replace("\n", ""),
    long_description=open('README.md').read(),
    version=__version__,
    author='Felix Simkovic, Jens Thomas, Adam Simpkin & Ronan Keegan',
    author_email='felixsimkovic@me.com',
    license='BSD License',
    url='https://github.com/rigdenlab/mrkit',
    download_url='https://github.com/rigdenlab/mrkit/tarball/' + __version__,
    package_dir={'mrkit': 'mrkit'},
    packages=find_packages(exclude="tests"),
    platforms=['Linux', 'Mac OS-X', 'Unix', 'Windows'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    test_suite='nose.collector',
    tests_require=['nose >=1.3.7'],
    include_package_data=True,
    zip_safe=False,
)

