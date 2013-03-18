from nose.tools import istest, assert_true, assert_false

import mayo.systems

@istest
def uri_is_recognised_if_it_has_known_source_control_prefix():
    _assert_is_source_control_uri("git+file:///tmp/blah")
    _assert_is_source_control_uri("git+https://github.com/mwilliamson/blah.git")

@istest
def uri_is_not_recognised_if_it_has_no_prefix():
    _assert_is_not_source_control_uri("file:///tmp/blah")
    
@istest
def uri_is_not_recognised_if_prefix_is_not_known():
    _assert_is_not_source_control_uri("local+file:///tmp/blah")
    
def _assert_is_source_control_uri(uri):
    assert_true(mayo.systems.is_source_control_uri(uri))
    
def _assert_is_not_source_control_uri(uri):
    assert_false(mayo.systems.is_source_control_uri(uri))
