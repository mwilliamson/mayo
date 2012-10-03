#!/usr/bin/env python

from distutils.core import setup

setup(
    name='blah',
    version='0.1',
    description='Thin wrapper around source control systems',
    author='Michael Williamson',
    url='http://github.com/mwilliamson/blah',
    scripts=["scripts/blah"],
    packages=['blah'],
)
