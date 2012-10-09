from blah.util import quiet_check_call, quiet_call, quiet_check_output

class GitFetcher(object):
    default_branch = "origin/master"
    
    def update(self, repository_uri, local_path):
        quiet_check_call(self._command("fetch"), cwd=local_path)
            
    def clone(self, repository_uri, local_path):
        quiet_check_call(self._command("clone", repository_uri, local_path))

    def checkout_version(self, local_path, version):
        if quiet_call(self._command("branch", "-r", "--contains", "origin/" + version), cwd=local_path) == 0:
            version = "origin/" + version
        quiet_check_call(self._command("checkout", version), cwd=local_path)

    def current_uri(self, local_path):
        return quiet_check_output(self._command("config", "remote.origin.url"), cwd=local_path).strip()

    def _command(self, command, *args):
        return ["git", command] + list(args)
