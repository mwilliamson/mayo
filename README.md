# Mayo: Download source control URIs

The main use of Mayo is being able to download repositories from a URI that
specifies what version control system (VCS) is being used:

```python
import mayo

mayo.fetch("git+https://github.com/mwilliamson/mayo.git", "/tmp/mayo")
print open("/tmp/mayo/README.md").read()
```

Mayo can also be used as a script:

```
mayo fetch git+https://github.com/mwilliamson/mayo.git /tmp/mayo
```

Specific commits can be selected by appending a hash to the URI, followed by
the name of the commit:

```python
mayo.fetch("git+https://github.com/mwilliamson/mayo.git#74d69b4", "/tmp/mayo")
```

At the moment, git and hg URIs are supported.
