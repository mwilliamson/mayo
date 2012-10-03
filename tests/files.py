import os
import errno
import shutil
from contextlib import contextmanager
import tempfile

def mkdir_p(path):
    """ 'mkdir -p' in Python """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
            
@contextmanager
def temporary_directory():
    directory = tempfile.mkdtemp()
    yield directory
    shutil.rmtree(directory)
