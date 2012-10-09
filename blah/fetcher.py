import os

import blah.systems
import blah.uri_parser

def fetch(uri_str, local_path, systems=None):
    if systems is None:
        systems = blah.systems.all_systems
    
    uri = blah.uri_parser.parse(uri_str)
    
    for vcs in systems:
        if uri.vcs == vcs.name:
            return fetch_with_vcs(uri, local_path, vcs)
            
    raise RuntimeError("Source control system not recognised: " + uri.vcs)
        
def fetch_with_vcs(uri, local_path, vcs):
    repository_uri = uri.repo_uri
    
    if os.path.exists(local_path):
        vcs_directory = os.path.join(local_path, vcs.directory_name)
        if not os.path.isdir(local_path):
            raise RuntimeError("Checkout path already exists, and is not directory: " + local_path)
        elif not os.path.isdir(vcs_directory):
            raise RuntimeError("VCS directory doesn't exist: " + vcs_directory)
        else:
            local_repo = vcs.local_repo(local_path)
            current_remote_uri = local_repo.remote_repo_uri()
            if current_remote_uri == repository_uri:
                local_repo.update()
            else:
                raise RuntimeError(
                    "Checkout directory is checkout of different URI: " + current_remote_uri +
                    "\nExpected: " + repository_uri
                )
    else:
        local_repo = vcs.clone(repository_uri, local_path)
        
    if uri.revision is None:
        revision = vcs.default_branch
    else:
        revision = uri.revision
        
    local_repo.checkout_revision(revision)
