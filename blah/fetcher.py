import subprocess

def fetch(repository_uri, local_path):
    if repository_uri.startswith("git+"):
        fetch_git_repository(repository_uri[len("git+"):], local_path)

def fetch_git_repository(repository_uri, local_path):
    subprocess.check_call(["git", "clone", repository_uri, local_path])
