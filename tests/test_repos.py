import os
from contextlib import contextmanager

from mayo.git import Git
from mayo.hg import Hg
from mayo.files import temporary_directory, write_file
from mayo.util import run

def create_repo(vcs_name, path):
    return {
        "git": create_git_repo,
        "hg": create_hg_repo
    }.get(vcs_name, create_unrecognised_repo)(path)

def create_unrecognised_repo(path):
    raise RuntimeError("Unrecognised VCS")

def create_git_repo(path):
    repository = Git().local_repo(path)
    execute(repository, ["init"])
    write_file(os.path.join(path, "README"), "Run it.")
    execute(repository, ["add", "README"])
    execute(repository, ["commit", "-mAdding README"])
    return repository

def create_hg_repo(path):    
    repository = Hg().local_repo(path)
    execute(repository, ["init"])
    write_file(os.path.join(path, "README"), "Run it.")
    execute(repository, ["add", "README"])
    execute(repository, ["commit", "-mAdding README"])
    return repository

@contextmanager
def temporary_repo(vcs):
    with temporary_directory() as path:
        yield create_repo(vcs, path)

@contextmanager
def temporary_git_repo():
    with temporary_directory() as path:
        yield create_git_repo(path)

@contextmanager
def temporary_hg_repo():
    with temporary_directory() as path:
        yield create_hg_repo(path)

def add_commit_to_repo(repo):
    write_file(os.path.join(repo.working_directory, "README"), "Run away!")
    execute(repo, ["add", "README"])
    execute(repo, ["commit", "-mUpdating README"])

def execute(repo, command):
    command = [repo.type] + command
    run(command, cwd=repo.working_directory)

