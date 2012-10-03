import os

from nose.tools import istest, assert_equal

from blah.finder import find_repository
from tests.files import mkdir_p, temporary_directory

@istest
def none_is_returned_if_there_is_no_repository():
    with temporary_directory() as directory:
        assert_equal(None, find_repository(directory))
        
@istest
def git_repository_is_returned_if_path_is_root_of_git_repository():
    with temporary_directory() as directory:
        mkdir_p(os.path.join(directory, ".git"))
        repository = find_repository(directory)
        assert_equal("git", repository.type)
        
@istest
def hg_repository_is_returned_if_path_is_root_of_hg_repository():
    with temporary_directory() as directory:
        mkdir_p(os.path.join(directory, ".hg"))
        repository = find_repository(directory)
        assert_equal("hg", repository.type)
        
@istest
def repository_path_of_git_repository_is_hidden_git_directory():
    with temporary_directory() as directory:
        repository_path = os.path.join(directory, ".git")
        mkdir_p(repository_path)
        repository = find_repository(directory)
        assert_equal(repository_path, repository.path)
        
@istest
def ancestors_are_searched_for_repositories():
    with temporary_directory() as directory:
        repository_path = os.path.join(directory, ".git")
        search_path = os.path.join(directory, "one/two/three")
        mkdir_p(repository_path)
        mkdir_p(search_path)
        repository = find_repository(search_path)
        assert_equal(repository_path, repository.path)
