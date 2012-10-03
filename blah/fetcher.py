import subprocess
import os

class Git(object):
    def __init__(self):
        self.name = "git"

    def fetch(self, repository_uri, local_path):
        if os.path.exists(local_path):
            # TODO: check that local_path is a valid clone
            subprocess.check_call(["git", "pull"], cwd=local_path)
        else:
            subprocess.check_call(["git", "clone", repository_uri, local_path])
        

class Hg(object):
    def __init__(self):
        self.name = "hg"

    def fetch(self, repository_uri, local_path):
        if os.path.exists(local_path):
            # TODO: check that local_path is a valid clone
            subprocess.check_call(["hg", "pull"], cwd=local_path)
            subprocess.check_call(["hg", "update"], cwd=local_path)
        else:
            subprocess.check_call(["hg", "clone", repository_uri, local_path])

systems = [Git(), Hg()]

def fetch(repository_uri, local_path):
    for system in systems:
        prefix = system.name + "+"
        if repository_uri.startswith(prefix):
            return system.fetch(repository_uri[len(prefix):], local_path)
            
    raise RuntimeError("Source control system not recognised: " + repository_uri)
