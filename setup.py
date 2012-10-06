#!/usr/bin/env python

import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='blah',
    version='0.1.2',
    description='Thin wrapper around source control systems',
    long_description=read("README.md"),
    author='Michael Williamson',
    url='http://github.com/mwilliamson/blah',
    scripts=["scripts/blah"],
    packages=['blah'],
)
