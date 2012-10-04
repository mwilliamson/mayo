import os
import subprocess
from contextlib import contextmanager

from nose.tools import istest, assert_equal, assert_raises

from blah.fetcher import fetch
from blah.repositories import Repository
from tests.files import mkdir_p, temporary_directory, write_file, read_file

@istest
def can_fetch_git_repository_into_new_directory():
    with temporary_directory() as directory:
        target = os.path.join(directory, "clone")
        with temporary_git_repo() as git_repo:
            original_uri = "git+file://" + git_repo.working_directory
            fetch(original_uri, target)
            assert_equal("Run it.", read_file(os.path.join(target, "README")))
        
@istest
def can_update_git_repository_to_latest_version():
    with temporary_directory() as directory:
        target = os.path.join(directory, "clone")
        with temporary_git_repo() as git_repo:
            original_uri = "git+file://" + git_repo.working_directory
            fetch(original_uri, target)
            assert_equal("Run it.", read_file(os.path.join(target, "README")))
            
            add_commit_to_git_repo(git_repo)
            fetch(original_uri, target)
            assert_equal("Run away!", read_file(os.path.join(target, "README")))
        
@istest
def can_update_git_repository_to_specific_commit_using_hash_before_commit_name():
    with temporary_directory() as directory:
        target = os.path.join(directory, "clone")
        with temporary_git_repo() as git_repo:
            original_uri = "git+file://" + git_repo.working_directory
            add_commit_to_git_repo(git_repo)
            fetch(original_uri, target)
            assert_equal("Run away!", read_file(os.path.join(target, "README")))
            
            fetch(original_uri + "#master^", target)
            assert_equal("Run it.", read_file(os.path.join(target, "README")))

@istest
def can_fetch_hg_repository_into_new_directory():
    with temporary_directory() as directory:
        target = os.path.join(directory, "clone")
        with temporary_hg_repo() as hg_repo:
            original_uri = "hg+file://" + hg_repo.working_directory
            fetch(original_uri, target)
            assert_equal("Run it.", read_file(os.path.join(target, "README")))
@istest
def can_update_hg_repository_to_latest_version():
    with temporary_directory() as directory:
        target = os.path.join(directory, "clone")
        with temporary_hg_repo() as hg_repo:
            original_uri = "hg+file://" + hg_repo.working_directory
            fetch(original_uri, target)
            assert_equal("Run it.", read_file(os.path.join(target, "README")))
            
            add_commit_to_hg_repo(hg_repo)
            fetch(original_uri, target)
            assert_equal("Run away!", read_file(os.path.join(target, "README")))
@istest
def can_update_hg_repository_to_specific_commit_using_hash_before_commit_name():
    with temporary_directory() as directory:
        target = os.path.join(directory, "clone")
        with temporary_hg_repo() as hg_repo:
            original_uri = "hg+file://" + hg_repo.working_directory
            add_commit_to_hg_repo(hg_repo)
            fetch(original_uri, target)
            assert_equal("Run away!", read_file(os.path.join(target, "README")))
            
            fetch(original_uri + "#0", target)
            assert_equal("Run it.", read_file(os.path.join(target, "README")))
            
@istest
def exception_is_thrown_if_repository_uri_is_not_recognised():
    with temporary_directory() as directory:
        target = os.path.join(directory, "clone")
        original_uri = "asf+file:///tmp"
        assert_raises(RuntimeError, lambda: fetch(original_uri, target))
        
@contextmanager
def temporary_git_repo():
    with temporary_directory() as path:
        repository = Repository(os.path.join(path, ".git"), "git")
        repository.execute(["init"])
        write_file(os.path.join(path, "README"), "Run it.")
        repository.execute(["add", "README"])
        repository.execute(["commit", "-mAdding README"])
        yield repository

def add_commit_to_git_repo(repo):
    write_file(os.path.join(repo.working_directory, "README"), "Run away!")
    repo.execute(["add", "README"])
    repo.execute(["commit", "-mUpdating README"])
        
@contextmanager
def temporary_hg_repo():
    with temporary_directory() as path:
        repository = Repository(os.path.join(path, ".hg"), "hg")
        repository.execute(["init"])
        write_file(os.path.join(path, "README"), "Run it.")
        repository.execute(["add", "README"])
        repository.execute(["commit", "-mAdding README"])
        yield repository

def add_commit_to_hg_repo(repo):
    write_file(os.path.join(repo.working_directory, "README"), "Run away!")
    repo.execute(["add", "README"])
    repo.execute(["commit", "-mUpdating README"])
