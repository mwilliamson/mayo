import os

from blah.util import quiet_check_call, quiet_call, quiet_check_output
import blah.files

class Git(object):
    name = "git"
    directory_name = ".git"
    default_branch = "origin/master"
    
    def clone(self, repository_uri, local_path):
        quiet_check_call(_command("clone", repository_uri, local_path))
        return GitRepository(local_path)
        
    def local_repo(self, working_directory):
        return GitRepository(working_directory)

class GitRepository(object):
    type = Git.name
    
    def __init__(self, working_directory):
        self.working_directory = working_directory
    
    def update(self):
        quiet_check_call(_command("fetch"), cwd=self.working_directory)

    def checkout_revision(self, revision):
        if quiet_call(_command("branch", "-r", "--contains", "origin/" + revision), cwd=self.working_directory) == 0:
            revision = "origin/" + revision
            
        quiet_check_call(_command("checkout", revision), cwd=self.working_directory)

    def remote_repo_uri(self):
        return quiet_check_output(_command("config", "remote.origin.url"), cwd=self.working_directory).strip()
        
    def head_revision(self):
        return quiet_check_output(_command("rev-parse", "HEAD"), cwd=self.working_directory).strip()

def _command(command, *args):
    return ["git", command] + list(args)
