from nose.tools import istest, assert_equal

import blah.util

@istest
def running_non_existent_command_raises_specific_no_such_command_exception():
    try:
        blah.util.run(["i-am-not-a-command"])
        # Expected exception
        assert False
    except blah.util.NoSuchCommandError as error:
        assert_equal("No such command: i-am-not-a-command", error.message)
        assert_equal("i-am-not-a-command", error.command)
