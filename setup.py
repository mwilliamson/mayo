#!/usr/bin/env python

import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='mayo',
    version='0.2.2',
    description='Thin wrapper around source control systems',
    long_description=read("README"),
    author='Michael Williamson',
    author_email='mike@zwobble.org',
    url='http://github.com/mwilliamson/mayo',
    scripts=["scripts/mayo"],
    packages=['mayo'],
    install_requires=["argparse==1.2.1", "catchy>=0.2,<0.3"],
    keywords="source control vcs scm git mercurial hg",
)
