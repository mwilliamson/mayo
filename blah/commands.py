import os
import subprocess
import sys

def find_command(name):
    return commands[name]

def what_is_this_command():
    directory = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
    repository = find_repository(directory)
    if repository is None:
        print "Could not find source control repository"
    else:
        print "{0}+file://{1}".format(repository.type, repository.path)

def find_repository(directory):
    directory = os.path.abspath(directory)
    while directory is not None:
        files = os.listdir(directory)
        if ".git" in files:
            return Repository(os.path.join(directory, ".git"), "git")
        
        directory = parent(directory)
        
    return None

class Repository(object):
    def __init__(self, repo_path, repo_type):
        self.path = repo_path
        self.type = repo_type

def parent(file_path):
    parent = os.path.dirname(file_path)
    if file_path == parent:
        return None
    else:
        return parent

commands = {
    "whatisthis": what_is_this_command,
    "what-is-this": what_is_this_command
}
