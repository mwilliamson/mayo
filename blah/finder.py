import os

from blah.files import parent
from blah.repositories import Repository

def find_repository(directory):
    directory = os.path.abspath(directory)
    while directory is not None:
        files = os.listdir(directory)
        if ".git" in files:
            return Repository(os.path.join(directory, ".git"), "git")
        if ".hg" in files:
            return Repository(os.path.join(directory, ".hg"), "hg")
        
        directory = parent(directory)
        
    return None
