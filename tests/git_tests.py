from nose.tools import assert_not_equal, istest

from test_repos import temporary_git_repo, add_commit_to_repo

@istest
def head_revision_of_git_repository_changes_after_commit():
    with temporary_git_repo() as git_repo:
        first_revision = git_repo.head_revision()
        
        add_commit_to_repo(git_repo)
        second_revision = git_repo.head_revision()
        
        assert_not_equal(first_revision, second_revision)
