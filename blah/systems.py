import os
import subprocess

class Git(object):
    def __init__(self):
        self.name = "git"
        self.vcs_directory = ".git"

    def fetch(self, repository_uri, local_path):
        if os.path.exists(local_path):
            # TODO: check that local_path is a valid clone
            subprocess.check_call(["git", "pull"], cwd=local_path)
        else:
            subprocess.check_call(["git", "clone", repository_uri, local_path])
        

class Hg(object):
    def __init__(self):
        self.name = "hg"
        self.vcs_directory = ".hg"

    def fetch(self, repository_uri, local_path):
        if os.path.exists(local_path):
            # TODO: check that local_path is a valid clone
            subprocess.check_call(["hg", "pull"], cwd=local_path)
            subprocess.check_call(["hg", "update"], cwd=local_path)
        else:
            subprocess.check_call(["hg", "clone", repository_uri, local_path])

all_systems = [Git(), Hg()]
