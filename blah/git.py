import os

from blah.util import quiet_check_call, quiet_call, quiet_check_output
import blah.files

class Git(object):
    default_branch = "origin/master"
    vcs_directory = ".git"
    
    def clone(self, repository_uri, local_path):
        quiet_check_call(_command("clone", repository_uri, local_path))
        return GitRepository(os.path.join(local_path, self.vcs_directory))
        
    def local_repo(self, local_path):
        return GitRepository(local_path)

class GitRepository(object):
    def __init__(self, local_path):
        self._working_directory = blah.files.parent(local_path)
    
    def update(self, repository_uri):
        quiet_check_call(_command("fetch"), cwd=self._working_directory)

    def checkout_version(self, version):
        if quiet_call(_command("branch", "-r", "--contains", "origin/" + version), cwd=self._working_directory) == 0:
            version = "origin/" + version
            
        quiet_check_call(_command("checkout", version), cwd=self._working_directory)

    def current_uri(self):
        return quiet_check_output(_command("config", "remote.origin.url"), cwd=self._working_directory).strip()

def _command(command, *args):
    return ["git", command] + list(args)
