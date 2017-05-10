"""Molecular Biology ToolKit Utility Module"""

import os
import tempfile


def tmp_fname(directory=None, prefix='tmp', suffix=""):
    """Return a filename for a temporary file

    Parameters
    ----------
    directory : str, optional
       Path to a directory to write the files to.
    prefix : str, optional
       A prefix to the temporary filename
    suffix : str, optional
       A suffix to the temporary filename

    """
    return tempfile.mkstemp(dir=directory, prefix=prefix, suffix=suffix)[0]

