import os

import blah.systems
import blah.uri_parser
import blah.errors

def fetch(uri_str, local_path, use_cache=False, systems=None):
    if systems is None:
        systems = blah.systems.all_systems
    
    uri = blah.uri_parser.parse(uri_str)
    
    vcs = _find_vcs(uri, systems)
    if use_cache and getattr(vcs, "supports_caching", False):
        vcs = vcs.use_cache()
    local_repo = _fetch_all_revisions(uri, local_path, vcs)
    revision = _read_revision(vcs, uri)
    local_repo.checkout_revision(revision)

def _find_vcs(uri, systems):
    for vcs in systems:
        if uri.vcs == vcs.name:
            return vcs
            
    raise blah.errors.UnrecognisedSourceControlSystem("Source control system not recognised: " + uri.vcs)

def _fetch_all_revisions(uri, local_path, vcs):
    if os.path.exists(local_path):
        return _update(uri.repo_uri, local_path, vcs)
    else:
        return vcs.clone(uri.repo_uri, local_path)

def _read_revision(vcs, uri):
    if uri.revision is None:
        return vcs.default_branch
    else:
        return uri.revision

def _update(repository_uri, local_path, vcs):
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
            return local_repo
        else:
            raise RuntimeError(
                "Checkout directory is checkout of different URI: " + current_remote_uri +
                "\nExpected: " + repository_uri
            )
    
