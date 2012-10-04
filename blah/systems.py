import os
import subprocess

from blah.repositories import Repository

class Git(object):
    def update(self, repository_uri, local_path):
        subprocess.check_call(["git", "pull"], cwd=local_path)
            
    def clone(self, repository_uri, local_path):
        subprocess.check_call(["git", "clone", repository_uri, local_path])

class Hg(object):
    def update(self, repository_uri, local_path):
        subprocess.check_call(["hg", "pull"], cwd=local_path)
        subprocess.check_call(["hg", "update"], cwd=local_path)
        
    def clone(self, repository_uri, local_path):
        subprocess.check_call(["hg", "clone", repository_uri, local_path])

class SourceControlSystem(object):
    def __init__(self, name, fetcher):
        self.name = name
        self.vcs_directory = "." + name
        self._fetcher = fetcher
        
    def fetch(self, repository_uri, local_path):
        if os.path.exists(local_path):
            # TODO: check that local_path is a valid clone
            self._fetcher.update(repository_uri, local_path)
        else:
            self._fetcher.clone(repository_uri, local_path)
            
    def repo(self, repo_path):
        return Repository(repo_path, self.name)

all_systems = [
    SourceControlSystem("git", Git()),
    SourceControlSystem("hg", Hg())
]
