import errno
import tempfile
import subprocess
import os
import shutil

from nose.tools import assert_equal, assert_not_equal, istest

from .test_repos import temporary_git_repo, add_commit_to_repo
import mayo


@istest
def head_revision_of_git_repository_changes_after_commit():
    with temporary_git_repo() as git_repo:
        first_revision = git_repo.head_revision()
        
        add_commit_to_repo(git_repo)
        second_revision = git_repo.head_revision()
        
        assert_not_equal(first_revision, second_revision)


@istest
def files_ignored_by_git_are_ignored_by_copy():
    temp_dir = tempfile.mkdtemp()
    try:
        _create_git_repo(
            path=temp_dir,
            filenames=["a", "b/a"],
            gitignore="/a"
        )
        repo = mayo.repository_at(temp_dir)
        assert_equal(["a"], repo.find_ignored_files())
    finally:
        shutil.rmtree(temp_dir)

def _create_files(parent_path, filenames):
    for filename in filenames:
        path = os.path.join(parent_path, filename)
        _mkdir_p(os.path.dirname(path))
        with open(path, "w") as target:
            target.write("")

def _create_git_repo(path, filenames, gitignore):
    _create_files(path, filenames)
    with open(os.path.join(path, ".gitignore"), "w") as gitignore_file:
        gitignore_file.write(gitignore)
    subprocess.check_call(["git", "init"], cwd=path)

def _list_destination_files():
    return list(files.all_filenames(self._destination_dir))


def _mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
