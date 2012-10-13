from blah.util import quiet_check_call, quiet_check_output

class Hg(object):
    name = "hg"
    directory_name = ".hg"
    default_branch = "default"
    
    def clone(self, repository_uri, local_path):
        quiet_check_call(["hg", "clone", repository_uri, local_path])
        return HgRepository(local_path)
        
    def local_repo(self, working_directory):
        return HgRepository(working_directory)

class HgRepository(object):
    type = Hg.name
    
    def __init__(self, working_directory):
        self.working_directory = working_directory
    
    def update(self):
        quiet_check_call(["hg", "pull"], cwd=self.working_directory)
        
    def checkout_revision(self, revision):
        quiet_check_call(["hg", "update", revision], cwd=self.working_directory)
        
    def remote_repo_uri(self):
        uri = quiet_check_output(["hg", "showconfig", "paths.default"], cwd=self.working_directory).strip()
        # Mercurial strips off "file:///" from the URI
        if _is_local(uri):
            return "file://" + uri
        else:
            return uri
            
    def head_revision(self):
        return quiet_check_output(["hg", "parents", "--template={node}"], cwd=self.working_directory).strip()

def _is_local(uri):
    return "://" not in uri
