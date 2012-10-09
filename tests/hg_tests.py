from nose.tools import assert_not_equal, istest

from test_repos import temporary_hg_repo, add_commit_to_repo

@istest
def head_revision_of_hg_repository_changes_after_commit():
    with temporary_hg_repo() as hg_repo:
        first_revision = hg_repo.head_revision()
        
        add_commit_to_repo(hg_repo)
        second_revision = hg_repo.head_revision()
        
        assert_not_equal(first_revision, second_revision)
