import os

from blah.repositories import Repository
from blah.git import GitFetcher
from blah.hg import HgFetcher

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
            vcs_directory = os.path.join(local_path, self.vcs_directory)
            if not os.path.isdir(local_path):
                raise RuntimeError("Checkout path already exists, and is not directory: " + local_path)
            elif not os.path.isdir(vcs_directory):
                raise RuntimeError("VCS directory doesn't exist: " + vcs_directory)
            else:
                current_uri = self._fetcher.current_uri(local_path)
                if current_uri == repository_uri:
                    self._fetcher.update(repository_uri, local_path)
                else:
                    raise RuntimeError(
                        "Checkout directory is checkout of different URI: " + current_uri +
                        "\nExpected: " + repository_uri
                    )
        else:
            self._fetcher.clone(repository_uri, local_path)
        self._fetcher.checkout_version(local_path, version)
            
    def repo(self, repo_path):
        return Repository(repo_path, self.name)

all_systems = [
    SourceControlSystem("git", GitFetcher()),
    SourceControlSystem("hg", HgFetcher())
]
