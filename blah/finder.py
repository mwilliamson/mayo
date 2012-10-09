import os

from blah.files import parent
from blah import systems

def find_repository(directory):
    directory = os.path.abspath(directory)
    while directory is not None:
        files = os.listdir(directory)
        for system in systems.all_systems:
            if system.directory_name in files:
                return system.local_repo(directory)
        
        directory = parent(directory)
        
    return None
