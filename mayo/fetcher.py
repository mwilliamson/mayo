import os
import shutil
import hashlib

import catchy

import mayo.systems
import mayo.uri_parser
import mayo.errors


def archive(uri_str, local_path):
    uri_hash = _sha1(uri_str)
    uri = mayo.uri_parser.parse(uri_str)
    
    vcs, local_repo = _fetch(uri_str, local_path)
    shutil.rmtree(os.path.join(local_path, vcs.directory_name))

def _sha1(value):
    return hashlib.sha1(value).hexdigest()

# Define fetch as distinct from _fetch to stop return value leaking
def fetch(*args, **kwargs):
    _fetch(*args, **kwargs)

def _fetch(uri_str, local_path, use_cache=False, systems=None):
    if systems is None:
        systems = mayo.systems.all_systems
    
    uri = mayo.uri_parser.parse(uri_str)
    
    vcs = _find_vcs(uri, systems)
    if use_cache and getattr(vcs, "supports_caching", False):
        vcs = vcs.use_cache()
    local_repo = _fetch_all_revisions(uri, local_path, vcs)
    revision = _read_revision(vcs, uri)
    local_repo.checkout_revision(revision)
    return vcs, local_repo

def _find_vcs(uri, systems):
    for vcs in systems:
        if uri.vcs == vcs.name:
            return vcs
            
    message = "Source control system not recognised: {0}".format(uri.vcs)
    raise mayo.errors.UnrecognisedSourceControlSystem(message)

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
        message = "Checkout path already exists, and is not directory: {0}".format(local_path)
        raise mayo.errors.MayoUserError(message)
    elif not os.path.isdir(vcs_directory):
        message = "{0} already exists and is not a {1} repository".format(local_path, vcs.name)
        raise mayo.errors.MayoUserError(message)
    else:
        local_repo = vcs.local_repo(local_path)
        current_remote_uri = local_repo.remote_repo_uri()
        if current_remote_uri == repository_uri:
            local_repo.update()
            return local_repo
        else:
            message = "{0} is existing checkout of different repository: {1}" \
                .format(local_path, current_remote_uri)
            raise mayo.errors.MayoUserError(message)
    
