import locale

import spur.local


shell = spur.local.LocalShell()


def quiet_check_call(command, cwd=None):
    return run(command, cwd=cwd).return_code

def quiet_call(command, cwd=None):
    return run(command, cwd=cwd, allow_error=True).return_code
    
def quiet_check_output(command, cwd):
    return run(command, cwd=cwd).output
    

def run(*args, **kwargs):
    decode = kwargs.pop("decode", True)
    result = shell.run(*args, **kwargs)
    if decode:
        result.output = _decode(result.output)
        result.stderr_output = _decode(result.stderr_output)
    return result


NoSuchCommandError = spur.local.NoSuchCommandError


def _decode(raw_bytes):
    return raw_bytes.decode(locale.getdefaultlocale()[1])
