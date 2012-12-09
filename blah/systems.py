from blah.git import Git
from blah.hg import Hg
import blah.uri_parser

all_systems = [
    Git(),
    Hg()
]

def is_source_control_uri(uri):
    parsed_uri = blah.uri_parser.parse(uri)
    return parsed_uri.vcs is not None and _is_recognised_prefix(parsed_uri.vcs)

def _is_recognised_prefix(prefix):
    return any(prefix == vcs.name for vcs in all_systems)
