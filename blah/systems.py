import os
import subprocess

from blah.repositories import Repository

_dev_null = open('/dev/null', 'w')

class Git(object):
    default_branch = "origin/master"
    
    def update(self, repository_uri, local_path):
        _quiet_check_call(self._command("fetch"), cwd=local_path)
            
    def clone(self, repository_uri, local_path):
        _quiet_check_call(self._command("clone", repository_uri, local_path))

    def checkout_version(self, local_path, version):
        if _quiet_call(self._command("branch", "-r", "--contains", "origin/" + version), cwd=local_path) == 0:
            version = "origin/" + version
        _quiet_check_call(self._command("checkout", version), cwd=local_path)

    def current_uri(self, local_path):
        return _quiet_check_output(self._command("config", "remote.origin.url"), cwd=local_path).strip()

    def _command(self, command, *args):
        return ["git", command] + list(args)

class Hg(object):
    default_branch = "default"
    
    def update(self, repository_uri, local_path):
        _quiet_check_call(["hg", "pull"], cwd=local_path)
        
    def clone(self, repository_uri, local_path):
        _quiet_check_call(["hg", "clone", repository_uri, local_path])
        
    def checkout_version(self, local_path, version):
        _quiet_check_call(["hg", "update", version], cwd=local_path)
        
    def current_uri(self, local_path):
        uri = _quiet_check_output(["hg", "showconfig", "paths.default"], cwd=local_path).strip()
        # Mercurial strips off "file:///" from the URI
        if _is_local(uri):
            return "file://" + uri
        else:
            return uri

class SourceControlSystem(object):
    def __init__(self, name, fetcher):
        self.name = name
        self.vcs_directory = "." + name
        self._fetcher = fetcher
        
    def fetch(self, repository_uri, local_path):
        if "#" in repository_uri:
            repository_uri, version = repository_uri.split("#")
        else:
            version = self._fetcher.default_branch
            
        if os.path.exists(local_path):
            vcs_directory = os.path.join(local_path, self.vcs_directory)
            if not os.path.isdir(local_path):
                raise RuntimeError("Checkout path already exists, and is not directory: " + local_path)
            elif not os.path.isdir(vcs_directory):
                raise RuntimeError("VCS directory doesn't exist: " + vcs_directory)
            else:
                current_uri = self._fetcher.current_uri(local_path)
                if current_uri == repository_uri:
                    self._fetcher.update(repository_uri, local_path)
                else:
                    raise RuntimeError(
                        "Checkout directory is checkout of different URI: " + current_uri +
                        "\nExpected: " + repository_uri
                    )
        else:
            self._fetcher.clone(repository_uri, local_path)
        self._fetcher.checkout_version(local_path, version)
            
    def repo(self, repo_path):
        return Repository(repo_path, self.name)

all_systems = [
    SourceControlSystem("git", Git()),
    SourceControlSystem("hg", Hg())
]

def _quiet_check_call(*args, **kwargs):
    return _quiet_subprocess_eval(subprocess.check_call, args, kwargs)

def _quiet_call(*args, **kwargs):
    return _quiet_subprocess_eval(subprocess.call, args, kwargs)
    
def _quiet_check_output(*args, **kwargs):
    return check_output(*args, stderr=_dev_null, **kwargs)
    
def _quiet_subprocess_eval(func, args, kwargs):
    return func(*args, stdout=_dev_null, stderr=subprocess.STDOUT, **kwargs)

def check_output(*popenargs, **kwargs):
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

def _is_local(uri):
    return "://" not in uri
