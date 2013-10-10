import locale

import spur.local


shell = spur.local.LocalShell()


_dev_null = open('/dev/null', 'w')

def quiet_check_call(command, cwd=None):
    return run(command, cwd=cwd).return_code

def quiet_call(command, cwd=None):
    return run(command, cwd=cwd, allow_error=True).return_code
    
def quiet_check_output(command, cwd):
    return run(command, cwd=cwd).output
    

run = shell.run


NoSuchCommandError = spur.local.NoSuchCommandError
