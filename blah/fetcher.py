import blah.systems

def fetch(repository_uri, local_path, systems=None):
    if systems is None:
        systems = blah.systems.all_systems
        
    for system in systems:
        prefix = system.name + "+"
        if repository_uri.startswith(prefix):
            return system.fetch(repository_uri[len(prefix):], local_path)
            
    raise RuntimeError("Source control system not recognised: " + repository_uri)
        
