import subprocess

_dev_null = open('/dev/null', 'w')

def quiet_check_call(*args, **kwargs):
    return _quiet_subprocess_eval(subprocess.check_call, args, kwargs)

def quiet_call(*args, **kwargs):
    return _quiet_subprocess_eval(subprocess.call, args, kwargs)
    
def quiet_check_output(*args, **kwargs):
    return _check_output(*args, stderr=_dev_null, **kwargs)
    
def _quiet_subprocess_eval(func, args, kwargs):
    return func(*args, stdout=_dev_null, stderr=subprocess.STDOUT, **kwargs)

def _check_output(*popenargs, **kwargs):
    r"""Run command with arguments and return its output as a byte string.

Backported from Python 2.7 as it's implemented as pure python on stdlib.
"""
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        error = subprocess.CalledProcessError(retcode, cmd)
        error.output = output
        raise error
    return output
