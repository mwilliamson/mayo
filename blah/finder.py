import os

from blah.files import parent
from blah.repositories import Repository
from blah import systems

def find_repository(directory):
    directory = os.path.abspath(directory)
    while directory is not None:
        files = os.listdir(directory)
        for system in systems.all_systems:
            if system.vcs_directory in files:
                return Repository(os.path.join(directory, system.vcs_directory), system.name)
        
        directory = parent(directory)
        
    return None
