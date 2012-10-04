import subprocess

import blah.files

_dev_null = open('/dev/null', 'w')

class Repository(object):
    def __init__(self, repo_path, repo_type):
        self.path = repo_path
        self.type = repo_type
        self.working_directory = blah.files.parent(repo_path)
        
    def execute(self, command):
        command = [self.type] + command
        subprocess.check_call(command, cwd=self.working_directory,
            stdout=_dev_null, stderr=subprocess.STDOUT)
