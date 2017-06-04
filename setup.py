"""Molecular Biology ToolKit"""

from distutils.util import convert_path
from setuptools import setup

import os
import sys

# ==============================================================
# Functions, functions, functions ...
# ==============================================================

def dependencies():
    modules, links = [], []
    for line in open('requirements.txt', 'r'):
        if line.startswith("#"):
            continue
        elif line.startswith("http"):
            links.append(line.strip())
        else:
            modules.append(line.strip())
    return modules, links


def readme():
    with open('README.rst', 'r') as f_in:
        return f_in.read()


def version():
    # Credits to http://stackoverflow.com/a/24517154
    main_ns = {}
    ver_path = convert_path('mbkit/version.py')
    with open(ver_path) as f_in:
        exec(f_in.read(), main_ns)
    return main_ns['__version__']

# ==============================================================
# Determine the Python executable
# ==============================================================
PYTHON_EXE = None
for arg in sys.argv:
    if arg[0:20] == "--script-python-path" and len(arg) == 20:
        option, value = arg, sys.argv[sys.argv.index(arg) + 1]
        PYTHON_EXE = value
    elif arg[0:20] == "--script-python-path" and arg[20] == "=":
        option, value = arg[:20], arg[21:]
        PYTHON_EXE = value

if not PYTHON_EXE:
    PYTHON_EXE = sys.executable


# ==============================================================
# Define all the relevant options
# ==============================================================
AUTHOR = "Felix Simkovic"
AUTHOR_EMAIL = "felixsimkovic@me.com"
DESCRIPTION = __doc__.replace("\n", "")
DEPENDENCIES, DEPENDENCY_LINKS = dependencies()
LICENSE = "BSD License"
LONG_DESCRIPTION = readme()
PACKAGE_DIR = "mbkit"
PACKAGE_NAME = "mbkit"
PLATFORMS = ['POSIX', 'Mac OS', 'Windows', 'Unix']
URL = "http://mbkit.rtfd.org"
VERSION = version()

PACKAGES = [
    'mbkit', 
    'mbkit/apps',
]

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
]

TEST_REQUIREMENTS = [
    "nose >=1.3.7",
] + ["unittest2 >=1.1.0" if sys.version_info < (2, 7) else ""]

# Do the actual setup below
setup(
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    name=PACKAGE_NAME,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    license=LICENSE,
    version=VERSION,
    url=URL,
    packages=PACKAGES,
    package_dir={PACKAGE_NAME: PACKAGE_DIR},
    install_requires=DEPENDENCIES,
    dependency_links=DEPENDENCY_LINKS,
    platforms=PLATFORMS,
    classifiers=CLASSIFIERS,
    test_suite='nose.collector',
    tests_require=TEST_REQUIREMENTS,
    include_package_data=True,
    zip_safe=False,
)

