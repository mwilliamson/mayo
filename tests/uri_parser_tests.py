from nose.tools import istest, assert_equal

from blah.uri_parser import parse

@istest
def vcs_is_none_if_plus_doesnt_occur_in_uri():
    assert_equal(None, parse("http://example.com/repo").vcs)
    
@istest
def vcs_is_string_before_plus():
    assert_equal("git", parse("git+http://example.com/repo").vcs)
    
@istest
def revision_is_none_if_hash_doesnt_occur_in_uri():
    assert_equal(None, parse("http://example.com/repo").revision)
    
@istest
def revision_is_string_after_hash():
    assert_equal("0.1", parse("http://example.com/repo#0.1").revision)
    
@istest
def repo_uri_is_original_uri_if_vcs_and_revision_not_specified():
    assert_equal(
        "http://example.com/repo",
        parse("http://example.com/repo").repo_uri
    )

    
@istest
def additional_pluses_in_uri_are_ignored():
    assert_equal("http://example.com/+repo", parse("git+http://example.com/+repo").repo_uri)
    
@istest
def additional_hashes_in_uri_are_ignored():
    assert_equal("0#1", parse("http://example.com/repo#0#1").revision)
