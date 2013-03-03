#!/usr/bin/env python

import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='blah',
    version='0.1.11',
    description='Thin wrapper around source control systems',
    long_description=read("README"),
    author='Michael Williamson',
    url='http://github.com/mwilliamson/blah',
    scripts=["scripts/blah"],
    packages=['blah'],
    install_requires=["argparse==1.2.1", "catchy>=0.1.0,<0.2"],
)
