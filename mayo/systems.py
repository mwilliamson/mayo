from .git import Git
from .hg import Hg
from .uri_parser import parse as parse_uri

all_systems = [
    Git(),
    Hg()
]

def is_source_control_uri(uri):
    parsed_uri = parse_uri(uri)
    return parsed_uri.vcs is not None and _is_recognised_prefix(parsed_uri.vcs)

def _is_recognised_prefix(prefix):
    return any(prefix == vcs.name for vcs in all_systems)
