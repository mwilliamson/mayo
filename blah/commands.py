import os
import subprocess
import sys

import blah.repositories
import blah.fetcher

def find_command(name):
    return commands[name]

def what_is_this_command():
    directory = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
    repository = blah.repositories.find_repository(directory)
    if repository is None:
        print "Could not find source control repository"
    else:
        print "{0}+file://{1}".format(repository.type, repository.working_directory)

def fetch_command():
    repository_uri = sys.argv[2]
    local_path = sys.argv[3]
    blah.fetcher.fetch(repository_uri, local_path)

commands = {
    "whatisthis": what_is_this_command,
    "what-is-this": what_is_this_command,
    "fetch": fetch_command
}
