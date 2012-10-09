import os

from blah.util import quiet_check_call, quiet_check_output
import blah.files

class Hg(object):
    default_branch = "default"
    vcs_directory = ".hg"
    
    def clone(self, repository_uri, local_path):
        quiet_check_call(["hg", "clone", repository_uri, local_path])
        return HgRepository(os.path.join(local_path, self.vcs_directory))
        
    def local_repo(self, local_path):
        return HgRepository(local_path)

class HgRepository(object):
    def __init__(self, local_path):
        self._working_directory = blah.files.parent(local_path)
    
    def update(self, repository_uri):
        quiet_check_call(["hg", "pull"], cwd=self._working_directory)
        
    def checkout_version(self, version):
        quiet_check_call(["hg", "update", version], cwd=self._working_directory)
        
    def current_uri(self):
        uri = quiet_check_output(["hg", "showconfig", "paths.default"], cwd=self._working_directory).strip()
        # Mercurial strips off "file:///" from the URI
        if _is_local(uri):
            return "file://" + uri
        else:
            return uri

def _is_local(uri):
    return "://" not in uri
