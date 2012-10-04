import os
import subprocess

from blah.repositories import Repository

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
    
    def repo(self, repo_path):
        return Repository(repo_path, self.name)

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
            
    def repo(self, repo_path):
        return Repository(repo_path, self.name)
        
all_systems = [Git(), Hg()]
