import os

from blah.repositories import Repository
from blah.git import Git
from blah.hg import Hg

class SourceControlSystem(object):
    def __init__(self, name, vcs):
        self.name = name
        self.vcs_directory = "." + name
        self._vcs = vcs
        
    def fetch(self, uri, local_path):
        repository_uri = uri.repo_uri
        
        if os.path.exists(local_path):
            vcs_directory = os.path.join(local_path, self.vcs_directory)
            if not os.path.isdir(local_path):
                raise RuntimeError("Checkout path already exists, and is not directory: " + local_path)
            elif not os.path.isdir(vcs_directory):
                raise RuntimeError("VCS directory doesn't exist: " + vcs_directory)
            else:
                local_repo = self._vcs.local_repo(vcs_directory)
                current_uri = local_repo.current_uri()
                if current_uri == repository_uri:
                    local_repo.update(repository_uri)
                else:
                    raise RuntimeError(
                        "Checkout directory is checkout of different URI: " + current_uri +
                        "\nExpected: " + repository_uri
                    )
        else:
            local_repo = self._vcs.clone(repository_uri, local_path)
            
        if uri.revision is None:
            revision = self._vcs.default_branch
        else:
            revision = uri.revision
            
        local_repo.checkout_revision(revision)
            
    def repo(self, repo_path):
        return Repository(repo_path, self.name)

all_systems = [
    SourceControlSystem("git", Git()),
    SourceControlSystem("hg", Hg())
]
