import os
import shutil
import hashlib

import blah.systems
import blah.uri_parser
import blah.errors
import blah.caching

def archive(uri_str, local_path):
    uri_hash = _sha1(uri_str)
    cache_dir = os.path.join(blah.caching.cache_root(), "archive", uri_hash)
    if not os.path.exists(os.path.dirname(cache_dir)):
        os.makedirs(os.path.dirname(cache_dir))
    if not os.path.exists(cache_dir):
        vcs = _fetch(uri_str, cache_dir)
        shutil.rmtree(os.path.join(cache_dir, vcs.directory_name))
    
    shutil.copytree(cache_dir, local_path)

def _sha1(value):
    return hashlib.sha1(value).hexdigest()

# Define fetch as distinct from _fetch to stop return value leaking
def fetch(*args, **kwargs):
    _fetch(*args, **kwargs)

def _fetch(uri_str, local_path, use_cache=False, systems=None):
    if systems is None:
        systems = blah.systems.all_systems
    
    uri = blah.uri_parser.parse(uri_str)
    
    vcs = _find_vcs(uri, systems)
    if use_cache and getattr(vcs, "supports_caching", False):
        vcs = vcs.use_cache()
    local_repo = _fetch_all_revisions(uri, local_path, vcs)
    revision = _read_revision(vcs, uri)
    local_repo.checkout_revision(revision)
    return vcs

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
        raise blah.errors.BlahUserError("Checkout path already exists, and is not directory: " + local_path)
    elif not os.path.isdir(vcs_directory):
        message = "{0} already exists and is not a git repository".format(local_path)
        raise blah.errors.BlahUserError(message)
    else:
        local_repo = vcs.local_repo(local_path)
        current_remote_uri = local_repo.remote_repo_uri()
        if current_remote_uri == repository_uri:
            local_repo.update()
            return local_repo
        else:
            message = "{0} is existing checkout of different repository: {1}" \
                .format(local_path, current_remote_uri)
            raise blah.errors.BlahUserError(message)
    
