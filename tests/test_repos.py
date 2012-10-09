import os
import subprocess
from contextlib import contextmanager

from blah.git import Git
from blah.hg import Hg
from blah.files import temporary_directory, write_file
        
@contextmanager
def temporary_git_repo():
    with temporary_directory() as path:
        repository = Git().local_repo(path)
        execute(repository, ["init"])
        write_file(os.path.join(path, "README"), "Run it.")
        execute(repository, ["add", "README"])
        execute(repository, ["commit", "-mAdding README"])
        yield repository

@contextmanager
def temporary_hg_repo():
    with temporary_directory() as path:
        repository = Hg().local_repo(path)
        execute(repository, ["init"])
        write_file(os.path.join(path, "README"), "Run it.")
        execute(repository, ["add", "README"])
        execute(repository, ["commit", "-mAdding README"])
        yield repository

def add_commit_to_repo(repo):
    write_file(os.path.join(repo.working_directory, "README"), "Run away!")
    execute(repo, ["add", "README"])
    execute(repo, ["commit", "-mUpdating README"])

_dev_null = open('/dev/null', 'w')

def execute(repo, command):
    command = [repo.type] + command
    subprocess.check_call(command, cwd=repo.working_directory,
        stdout=_dev_null, stderr=subprocess.STDOUT)

