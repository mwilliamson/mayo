# Blah: Library for interacting with source control

The main use of Blah is being able to download repositories from a URI that
specifies what version control system is being used:

```python
import blah

blah.fetch("git+https://github.com/mwilliamson/blah.git", "/tmp/blah")
print open("/tmp/blah/README.md").read()
```

Blah can also be used as a script:

```
blah fetch git+https://github.com/mwilliamson/blah.git /tmp/blah
```

At the moment, git and hg URIs are supported.
