import os

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

def parent(file_path):
    parent = os.path.dirname(file_path)
    if file_path == parent:
        return None
    else:
        return parent
