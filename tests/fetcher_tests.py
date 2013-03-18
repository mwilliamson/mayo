import os
import functools
import contextlib

from nose.tools import istest, assert_equal, assert_false

from mayo.fetcher import fetch, archive
from mayo.files import mkdir_p, temporary_directory, write_file, read_file
from mayo import UnrecognisedSourceControlSystem
from mayo.errors import MayoUserError
from mayo.systems import all_systems

from test_repos import temporary_hg_repo, temporary_git_repo, add_commit_to_repo, tag_git_repo
import test_repos


def test(func):
    @functools.wraps(func)
    def run_test(*args, **kwargs):
        with temporary_xdg_cache_dir():
            return func(*args, **kwargs)
    return istest(run_test)


def vcs_agnostic_test(func=None, params=(), **kwargs):
    def wrap(func):
        @functools.wraps(func)
        def run_test():
            for vcs in map(VcsUnderTest, all_systems):
                test_params = [kwargs["{0}_params".format(vcs.name)][param_name] for param_name in params]
                with temporary_empty_dir() as temp_dir:
                    yield tuple([test(func), vcs, temp_dir] + test_params)
        return istest(run_test)
        
    if func is not None and len(kwargs) == 0:
        return wrap(func)
    else:
        return wrap


class VcsUnderTest(object):
    def __init__(self, vcs):
        self.vcs = vcs
        
    @property
    def name(self):
        return self.vcs.name
        
    @property
    def directory_name(self):
        return self.vcs.directory_name
    
    def temporary_repo(self):
        return test_repos.temporary_repo(self.name)
        
    def __repr__(self):
        return self.name

#~ @test
def repository_is_used_if_uri_has_prefix():
    git = mock_vcs("git")
    hg = mock_vcs("hg")
    git_uri = "http://www.example.com/project.git"
    
    fetch("git+" + git_uri, "/tmp/project", systems=[hg, git])
    
    git.fetch.assert_called_once_with(mock.ANY, "/tmp/project")
    uri_arg = git.fetch.call_args[0][0]
    assert_equal("git", uri_arg.vcs)
    assert_equal(git_uri, uri_arg.repo_uri)
    assert_equal(None, uri_arg.revision)
    
def mock_vcs(name):
    vcs = mock.Mock()
    vcs.name = name
    return vcs

@test
def error_is_raised_if_repository_uri_is_not_recognised():
    with temporary_empty_dir() as target:
        original_uri = "asf+file:///tmp"
        assert_raises_message(
            UnrecognisedSourceControlSystem,
            "Source control system not recognised: asf",
            lambda: fetch(original_uri, target)
        )

@vcs_agnostic_test
def can_fetch_repository_into_new_directory(vcs, target):
    with vcs.temporary_repo() as repo:
        original_uri = "{0}+file://{1}".format(vcs.name, repo.working_directory)
        fetch(original_uri, target)
        assert_equal("Run it.", read_file(os.path.join(target, "README")))
        
@vcs_agnostic_test
def can_update_repository_to_latest_version(vcs, target):
    with vcs.temporary_repo() as repo:
        original_uri = "{0}+file://{1}".format(vcs.name, repo.working_directory)
        fetch(original_uri, target)
        assert_equal("Run it.", read_file(os.path.join(target, "README")))
        
        add_commit_to_repo(repo)
        fetch(original_uri, target)
        assert_equal("Run away!", read_file(os.path.join(target, "README")))
        
@vcs_agnostic_test(
    params=("commit", ),
    git_params={"commit": "master^"},
    hg_params={"commit": "0"}
)
def can_update_repository_to_specific_commit_using_hash_before_commit_name(vcs, target, commit):
    with vcs.temporary_repo() as repo:
        original_uri = "{0}+file://{1}".format(vcs.name, repo.working_directory)
        add_commit_to_repo(repo)
        fetch(original_uri, target)
        assert_equal("Run away!", read_file(os.path.join(target, "README")))
        
        fetch("{0}#{1}".format(original_uri, commit), target)
        assert_equal("Run it.", read_file(os.path.join(target, "README")))
            
@vcs_agnostic_test(
    params=("commit", ),
    git_params={"commit": "master^"},
    hg_params={"commit": "0"}
)
def can_clone_repository_to_specific_commit_using_hash_before_commit_name(vcs, target, commit):
    with vcs.temporary_repo() as repo:
        original_uri = "{0}+file://{1}".format(vcs.name, repo.working_directory)
        add_commit_to_repo(repo)
        fetch("{0}#{1}".format(original_uri, commit), target)
        assert_equal("Run it.", read_file(os.path.join(target, "README")))
        

@vcs_agnostic_test
def can_fetch_repo_without_vcs_files(vcs, target):
    with vcs.temporary_repo() as repo:
        original_uri = "{0}+file://{1}".format(vcs.name, repo.working_directory)
        archive(original_uri, target)
        assert_equal("Run it.", read_file(os.path.join(target, "README")))
        assert_false(os.path.exists(os.path.join(target, vcs.directory_name)))
        
@test
def origin_is_prefixed_to_git_commit_if_necessary():
    with temporary_empty_dir() as target:
        with temporary_git_repo() as git_repo:
            original_uri = "git+file://" + git_repo.working_directory
            # master == origin/master
            fetch(original_uri, target)
            assert_equal("Run it.", read_file(os.path.join(target, "README")))
            
            add_commit_to_repo(git_repo)
            # If we checkout master rather than origin/master, we don't change revision
            fetch(original_uri + "#master", target)
            assert_equal("Run away!", read_file(os.path.join(target, "README")))
            
@test
def can_use_cache_when_cloning_git_repository():
    with temporary_empty_dir() as target:
        with temporary_git_repo() as git_repo:
            original_uri = "git+file://" + git_repo.working_directory
            add_commit_to_repo(git_repo)
            fetch(original_uri + "#master^", target, use_cache=True)
            assert_equal("Run it.", read_file(os.path.join(target, "README")))


@test
def error_is_raised_if_target_is_file():
    with temporary_empty_dir() as target:
        write_file(target, "Nope")
        with temporary_git_repo() as git_repo:
            original_uri = "git+file://" + git_repo.working_directory
            assert_raises_message(
                MayoUserError,
                "Checkout path already exists, and is not directory: {0}".format(target),
                lambda: fetch(original_uri, target)
            )
            
@test
def git_fetch_raises_error_if_target_is_not_git_repository():
    with temporary_directory() as target:
        with temporary_git_repo() as git_repo:
            original_uri = "git+file://" + git_repo.working_directory
            assert_raises_message(
                MayoUserError,
                "{0} already exists and is not a git repository".format(target),
                lambda: fetch(original_uri, target)
            )
            
@test
def git_fetch_raises_error_if_target_is_checkout_of_different_repository():
    with temporary_empty_dir() as target:
        with temporary_git_repo() as first_repo:
            with temporary_git_repo() as second_repo:
                fetch("git+file://" + first_repo.working_directory, target)
                assert_raises_message(
                    MayoUserError,
                    "{0} is existing checkout of different repository: file://{1}"
                        .format(target, first_repo.working_directory),
                    lambda: fetch("git+file://" + second_repo.working_directory, target)
                )

@test
def hg_fetch_raises_error_if_target_is_checkout_of_different_repository():
    with temporary_empty_dir() as target:
        with temporary_hg_repo() as first_repo:
            with temporary_hg_repo() as second_repo:
                fetch("hg+file://" + first_repo.working_directory, target)
                assert_raises_message(
                    MayoUserError,
                    "{0} is existing checkout of different repository: file://{1}"
                        .format(target, first_repo.working_directory),
                    lambda: fetch("hg+file://" + second_repo.working_directory, target)
                )

def assert_raises_message(expected_error_type, expected_message, func):
    try:
        func()
        assert False
    except expected_error_type as error:
        assert_equal(expected_message, error.message)


@contextlib.contextmanager
def temporary_xdg_cache_dir():
    key = "XDG_CACHE_HOME"
    with temporary_directory() as cache_dir:
        with updated_env({key: cache_dir}):
            yield

@contextlib.contextmanager
def updated_env(env_updates):
    original_env = {}
    for key, updated_value in env_updates.iteritems():
        original_env[key] = os.environ.get(key)
    os.environ[key] = updated_value

    try:
        yield
    finally:
        for key, original_value in original_env.iteritems():
            if original_value is None:
                del os.environ[key]
            else:
                os.environ[key] = original_value


@contextlib.contextmanager
def temporary_empty_dir():
    with temporary_directory() as directory:
        yield os.path.join(directory, "sub")
