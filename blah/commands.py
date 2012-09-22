import os

def find_command(name):
    return commands[name]

def what_is_this_command():
    system = what_is_this()
    if system is None:
        print "Unrecognised source control system"
    else:
        print system

def what_is_this():
    directory = os.getcwd()
    while directory is not None:
        files = os.listdir(directory)
        if ".git" in files:
            return "git"
        
        directory = parent(directory)
        
    return None

def parent(file_path):
    parent = os.path.dirname(file_path)
    if file_path == parent:
        return None
    else:
        return parent

commands = {
    "whatisthis": what_is_this_command
}
