import os
import subprocess
import sys

import blah.finder

def find_command(name):
    return commands[name]

def what_is_this_command():
    directory = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
    repository = blah.finder.find_repository(directory)
    if repository is None:
        print "Could not find source control repository"
    else:
        print "{0}+file://{1}".format(repository.type, repository.path)

commands = {
    "whatisthis": what_is_this_command,
    "what-is-this": what_is_this_command
}
