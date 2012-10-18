import os
import argparse

import blah.repositories
import blah.fetcher

class WhatIsThisCommand(object):
    def create_parser(self, subparser):
        subparser.add_argument("directory", nargs="?")
    
    def execute(self, args):
        directory = args.directory if args.directory is not None else os.getcwd()
        repository = blah.repositories.find_repository(directory)
        if repository is None:
            print "Could not find source control repository"
        else:
            print "{0}+file://{1}".format(repository.type, repository.working_directory)

what_is_this_command = WhatIsThisCommand()

class FetchCommand(object):
    def create_parser(self, subparser):
        subparser.add_argument("repository_uri", metavar="repository-uri")
        subparser.add_argument("local_path", metavar="local-path")
        subparser.add_argument("--use-cache", default=False, help=argparse.SUPPRESS, action="store_true")
    
    def execute(self, args):
        blah.fetcher.fetch(args.repository_uri, args.local_path, args.use_cache)

commands = {
    "whatisthis": what_is_this_command,
    "what-is-this": what_is_this_command,
    "fetch": FetchCommand()
}
