"""Molecular Biology ToolKit Utility Module"""

import tempfile


def tmp_fname(delete=False, directory=None, prefix='tmp', suffix=""):
    """Return a filename for a temporary file

    Parameters
    ----------
    delete : bool, optional
       Delete the file, thus return name only [default: True]
    directory : str, optional
       Path to a directory to write the files to.
    prefix : str, optional
       A prefix to the temporary filename
    suffix : str, optional
       A suffix to the temporary filename

    """
    tmpf = tempfile.NamedTemporaryFile(delete=False, dir=directory, prefix=prefix, suffix=suffix)
    tmpf.close()
    return tmpf.name

