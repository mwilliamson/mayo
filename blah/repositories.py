import os

from blah import systems
from blah.files import parent

def repository_at(working_directory):
    directory = os.path.abspath(working_directory)
    files = os.listdir(directory)
    for system in systems.all_systems:
        if system.directory_name in files:
            return system.local_repo(directory)
        
    return None
    
def find_repository(directory):
    directory = os.path.abspath(directory)
    while directory is not None:
        repository = repository_at(directory)
        if repository is not None:
            return repository
        directory = parent(directory)
        
    return None
