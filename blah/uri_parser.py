def parse(uri):
    if "+" in uri:
        vcs, versioned_repo_uri = uri.split("+", 1)
    else:
        vcs = None
        versioned_repo_uri = uri
        
    if "#" in versioned_repo_uri:
        repo_uri, revision = versioned_repo_uri.split("#", 1)
    else:
        revision = None
        repo_uri = versioned_repo_uri
        
    return ParsedUri(vcs, repo_uri, revision)

class ParsedUri(object):
    def __init__(self, vcs, repo_uri, revision):
        self.vcs = vcs
        self.repo_uri = repo_uri
        self.revision = revision
