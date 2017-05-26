"""Molecular Biology ToolKit Utility Module"""

import os
import tempfile


def tmp_dir(directory=None, prefix='tmp', suffix=""):
    """Return a filename for a temporary directory 

    Parameters
    ----------
    directory : str, optional
       Path to a directory to write the files to.
    prefix : str, optional
       A prefix to the temporary filename
    suffix : str, optional
       A suffix to the temporary filename

    """
    return tempfile.mkdtemp(dir=directory, prefix=prefix, suffix=suffix)


def tmp_fname(delete=False, directory=None, prefix='tmp', stem=None, suffix=""):
    """Return a filename for a temporary file

    The naming convention of scripts will be ``prefix`` + ``stem`` + ``suffix``.

    Parameters
    ----------
    delete : bool, optional
       Delete the file, thus return name only [default: True]
    directory : str, optional
       Path to a directory to write the files to
    prefix : str, optional
       A prefix to the temporary filename
    stem : str, optional
       The steam part of the script name
    suffix : str, optional
       A suffix to the temporary filename

    """
    if directory is None:
        directory = tempfile.gettempdir()
    if stem is None:
        tmpf = tempfile.NamedTemporaryFile(delete=False, dir=directory, prefix=prefix, suffix=suffix)
        tmpf.close()
        return tmpf.name
    else:
        tmpf = os.path.join(directory, prefix + stem + suffix)
        if not delete:
            open(tmpf, 'w').close()
        return tmpf
