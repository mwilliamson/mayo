import os
import os.path
import hashlib

from blah.util import run

class Git(object):
    name = "git"
    directory_name = ".git"
    default_branch = "origin/master"
    supports_caching = True
    
    def __init__(self, use_cache=False):
        self._use_cache = use_cache
        
    def use_cache(self):
        return Git(use_cache=True)
    
    def clone(self, repository_uri, local_path):
        if self._use_cache:
            cache_dir = self._update_cache(repository_uri)
            _git(["clone", repository_uri, local_path, "--reference", cache_dir])
            _git(["repack", "-a"], cwd=local_path)
            _git(["submodule", "foreach", "git", "repack", "-a"], cwd=local_path)
            
            os.remove(os.path.join(local_path, ".git/objects/info/alternates"))
        else:
            _git(["clone", repository_uri, local_path])
        return GitRepository(local_path)
        
    def local_repo(self, working_directory):
        return GitRepository(working_directory)
        
    def _update_cache(self, repository_uri):
        cache_dir = os.environ.get("BLAH_CACHE_DIR", os.path.expanduser("~/.cache/blah"))
        repo_hash = hashlib.sha1(repository_uri).hexdigest()
        cache_repo = os.path.join(cache_dir, repo_hash)
        
        if os.path.exists(cache_repo):
            _git(["fetch"], cwd=cache_repo)
        else:
            _git(["clone", repository_uri, cache_repo])
            
        return cache_repo

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

def _git(git_command, *args, **kwargs):
    command = ["git"] + git_command
    return run(command, *args, **kwargs)
