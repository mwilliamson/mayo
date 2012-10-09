from blah.util import quiet_check_call, quiet_check_output

class HgFetcher(object):
    default_branch = "default"
    
    def update(self, repository_uri, local_path):
        quiet_check_call(["hg", "pull"], cwd=local_path)
        
    def clone(self, repository_uri, local_path):
        quiet_check_call(["hg", "clone", repository_uri, local_path])
        
    def checkout_version(self, local_path, version):
        quiet_check_call(["hg", "update", version], cwd=local_path)
        
    def current_uri(self, local_path):
        uri = quiet_check_output(["hg", "showconfig", "paths.default"], cwd=local_path).strip()
        # Mercurial strips off "file:///" from the URI
        if _is_local(uri):
            return "file://" + uri
        else:
            return uri

def _is_local(uri):
    return "://" not in uri
