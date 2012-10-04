import os
import subprocess

from blah.repositories import Repository

_dev_null = open('/dev/null', 'w')

class Git(object):
    default_branch = "origin/master"
    
    def update(self, repository_uri, local_path):
        _quiet_check_call(self._command("fetch"), cwd=local_path)
            
    def clone(self, repository_uri, local_path):
        _quiet_check_call(self._command("clone", repository_uri, local_path))

    def checkout_version(self, local_path, version):
        if _quiet_call(self._command("branch", "-r", "--contains", "origin/" + version), cwd=local_path) == 0:
            version = "origin/" + version
        _quiet_check_call(self._command("checkout", version), cwd=local_path)

    def _command(self, command, *args):
        return ["git", command] + list(args)

class Hg(object):
    default_branch = "default"
    
    def update(self, repository_uri, local_path):
        _quiet_check_call(["hg", "pull"], cwd=local_path)
        
    def clone(self, repository_uri, local_path):
        _quiet_check_call(["hg", "clone", repository_uri, local_path])
        
    def checkout_version(self, local_path, version):
        _quiet_check_call(["hg", "update", version], cwd=local_path)

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
            self._fetcher.update(repository_uri, local_path)
        else:
            self._fetcher.clone(repository_uri, local_path)
        self._fetcher.checkout_version(local_path, version)
            
    def repo(self, repo_path):
        return Repository(repo_path, self.name)

all_systems = [
    SourceControlSystem("git", Git()),
    SourceControlSystem("hg", Hg())
]

def _quiet_check_call(*args, **kwargs):
    return _quiet_subprocess_eval(subprocess.check_call, args, kwargs)

def _quiet_call(*args, **kwargs):
    return _quiet_subprocess_eval(subprocess.call, args, kwargs)
    
def _quiet_subprocess_eval(func, args, kwargs):
    return func(*args, stdout=_dev_null, stderr=subprocess.STDOUT, **kwargs)
