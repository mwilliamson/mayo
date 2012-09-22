import os
import subprocess
import sys

def find_command(name):
    return commands[name]

def what_is_this_command():
    repository = find_current_repository()
    if repository is None:
        print "Could not find source control repository"
    else:
        print "{0}+file://{1}".format(repository.type, repository.path)

def find_current_repository():
    directory = os.getcwd()
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

def add_delegated_commands(commands):
    for command_name in ["status", "commit", "add", "diff", "push"]:
        commands[command_name] = delegated_command(command_name)

def delegated_command(command_name):
    def execute_command():
        repository = find_current_repository()
        command = repository.type
        sys.exit(subprocess.call([command] + sys.argv[1:]))
        
    return execute_command

commands = {
    "whatisthis": what_is_this_command,
    "what-is-this": what_is_this_command
}

add_delegated_commands(commands)
