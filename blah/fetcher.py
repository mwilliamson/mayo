from blah import systems

def fetch(repository_uri, local_path):
    for system in systems.all_systems:
        prefix = system.name + "+"
        if repository_uri.startswith(prefix):
            return system.fetch(repository_uri[len(prefix):], local_path)
            
    raise RuntimeError("Source control system not recognised: " + repository_uri)
