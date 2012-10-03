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

def write_file(path, contents):
    with open(path, "w") as f:
        return f.write(contents)

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def parent(file_path):
    parent = os.path.dirname(file_path)
    if file_path == parent:
        return None
    else:
        return parent
