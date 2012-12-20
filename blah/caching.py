import os


def cache_root():
    xdg_cache_home = os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
    return os.environ.get("BLAH_CACHE_DIR", os.path.join(xdg_cache_home, "blah"))
