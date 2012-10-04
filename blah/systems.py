import os
import subprocess

from blah.repositories import Repository

class Git(object):
    default_branch = "origin/master"
    
    def update(self, repository_uri, local_path, version):
        subprocess.check_call(["git", "fetch"], cwd=local_path)
        if subprocess.call(["git", "branch", "-r", "--contains", "origin/" + version]) == 0:
            version = "origin/" + version
            
        subprocess.check_call(["git", "checkout", version], cwd=local_path)
            
    def clone(self, repository_uri, local_path, version):
        subprocess.check_call(["git", "clone", repository_uri, local_path])

class Hg(object):
    default_branch = "default"
    
    def update(self, repository_uri, local_path, version):
        subprocess.check_call(["hg", "pull"], cwd=local_path)
        subprocess.check_call(["hg", "update", version], cwd=local_path)
        
    def clone(self, repository_uri, local_path, version):
        subprocess.check_call(["hg", "clone", repository_uri, local_path])

class SourceControlSystem(object):
    def __init__(self, name, fetcher):
        self.name = name
        self.vcs_directory = "." + name
        self._fetcher = fetcher
        
    def fetch(self, repository_uri, local_path):
        if "#" in repository_uri:
            repository_uri, version = repository_uri.split("#")
        else:
            version = self._fetcher.default_branch
            
        if os.path.exists(local_path):
            # TODO: check that local_path is a valid clone
            self._fetcher.update(repository_uri, local_path, version)
        else:
            self._fetcher.clone(repository_uri, local_path, version)
            
    def repo(self, repo_path):
        return Repository(repo_path, self.name)

all_systems = [
    SourceControlSystem("git", Git()),
    SourceControlSystem("hg", Hg())
]
