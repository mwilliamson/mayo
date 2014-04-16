from .util import run


class Git(object):
    name = "git"
    directory_name = ".git"
    default_branch = "origin/master"
    
    def clone(self, repository_uri, local_path):
        _git(["clone", repository_uri, local_path])
        return GitRepository(local_path)
        
    def local_repo(self, working_directory):
        return GitRepository(working_directory)


class GitRepository(object):
    type = Git.name
    
    def __init__(self, working_directory):
        self.working_directory = working_directory
    
    def update(self):
        _git(["fetch"], cwd=self.working_directory)

    def checkout_revision(self, revision):
        if _git(["branch", "-r", "--contains", "origin/" + revision], cwd=self.working_directory, allow_error=True).return_code == 0:
            revision = "origin/" + revision
            
        _git(["checkout", revision], cwd=self.working_directory)

    def remote_repo_uri(self):
        return _git(["config", "remote.origin.url"], cwd=self.working_directory).output.strip()
        
    def head_revision(self):
        return _git(["rev-parse", "HEAD"], cwd=self.working_directory).output.strip()

    def find_ignored_files(self):
        result = self._git(["status", "-z", "--ignored"])
        lines = result.output.split(b"\0")
        ignore_prefix = b"!! "
        return [
            line[len(ignore_prefix):].decode("utf8")
            for line in lines
            if line.startswith(ignore_prefix)
        ]
    
    def _git(self, git_command):
        return _git(git_command, cwd=self.working_directory)
        

def _git(git_command, *args, **kwargs):
    command = ["git"] + git_command
    return run(command, *args, **kwargs)
