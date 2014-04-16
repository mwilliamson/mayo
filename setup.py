#!/usr/bin/env python

import os
import sys
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


_install_requires = [
    "spur.local>=0.3.5,<0.4",
]

if sys.version_info[:2] <= (2, 6):
    _install_requires.append("argparse>=1.1,<2.0")

setup(
    name='mayo',
    version='0.2.5',
    description='Thin wrapper around source control systems',
    long_description=read("README"),
    author='Michael Williamson',
    author_email='mike@zwobble.org',
    url='http://github.com/mwilliamson/mayo',
    scripts=["scripts/mayo"],
    packages=['mayo'],
    install_requires=_install_requires,
    keywords="source control vcs scm git mercurial hg",
)
