from nose.tools import istest, assert_equal

import blah.util

@istest
def running_non_existent_command_raises_specific_no_such_command_exception():
    try:
        blah.util.run(["bin/i-am-not-a-command"])
        # Expected exception
        assert False
    except blah.util.NoSuchCommandError as error:
        assert_equal("No such command: bin/i-am-not-a-command", error.message)
        assert_equal("bin/i-am-not-a-command", error.command)

@istest
def running_command_that_uses_path_env_variable_asks_if_command_is_installed():
    try:
        blah.util.run(["not-git"])
        # Expected exception
        assert False
    except blah.util.NoSuchCommandError as error:
        assert_equal("Command not found: not-git. Check that not-git is installed and on $PATH", error.message)
        assert_equal("not-git", error.command)
