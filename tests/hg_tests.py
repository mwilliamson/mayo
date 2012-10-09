import os
import subprocess
from contextlib import contextmanager

from nose.tools import assert_not_equal, istest

from blah.hg import Hg
import blah.files
from blah.files import mkdir_p, temporary_directory, write_file, read_file

@istest
def can_get_current_revision_of_hg_repository():
    with temporary_hg_repo() as hg_repo:
        first_revision = hg_repo.head_revision()
        
        add_commit_to_repo(hg_repo)
        second_revision = hg_repo.head_revision()
        
        assert_not_equal(first_revision, second_revision)

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
