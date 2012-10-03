import subprocess
import os

def fetch(repository_uri, local_path):
    if repository_uri.startswith("git+"):
        fetch_git_repository(repository_uri[len("git+"):], local_path)
    else:
        raise RuntimeError("Source control system not recognised: " + repository_uri)

def fetch_git_repository(repository_uri, local_path):
    if os.path.exists(local_path):
        # TODO: check that local_path is a valid clone
        subprocess.check_call(["git", "pull"], cwd=local_path)
    else:
        subprocess.check_call(["git", "clone", repository_uri, local_path])
