import blah.files

class Repository(object):
    def __init__(self, repo_path, repo_type):
        self.path = repo_path
        self.type = repo_type
        self.working_directory = blah.files.parent(repo_path)
