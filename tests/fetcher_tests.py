import os
import subprocess
from contextlib import contextmanager

from nose.tools import istest, assert_equal

from blah.fetcher import fetch
from blah.repositories import Repository
from tests.files import mkdir_p, temporary_directory, write_file, read_file

@istest
def can_fetch_git_repository():
    with temporary_directory() as directory:
        target = os.path.join(directory, "clone")
        with temporary_git_repo() as git_repo:
            original_uri = "git+file://" + git_repo.path
            fetch(original_uri, target)
            assert_equal("Run it.", read_file(os.path.join(target, "README")))
        
@contextmanager
def temporary_git_repo():
    with temporary_directory() as path:
        subprocess.check_call(["git", "init"], cwd=path)
        write_file(os.path.join(path, "README"), "Run it.")
        subprocess.check_call(["git", "add", "README"], cwd=path)
        subprocess.check_call(["git", "commit", "-mAdding README"], cwd=path)
        yield Repository(path, "git")
