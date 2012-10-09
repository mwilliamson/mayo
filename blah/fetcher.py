import blah.systems
import blah.uri_parser

def fetch(uri_str, local_path, systems=None):
    if systems is None:
        systems = blah.systems.all_systems
    
    uri = blah.uri_parser.parse(uri_str)
    
    for system in systems:
        if uri.vcs == system.name:
            return system.fetch(uri, local_path)
            
    raise RuntimeError("Source control system not recognised: " + uri.vcs)
        
