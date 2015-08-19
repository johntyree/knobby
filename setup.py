#!/usr/bin/env python
# coding: utf8

from setuptools import setup

setup(
    name='knobby',
    version='0.0.1',
    packages=['knobby'],
    author='John Tyree',
    author_email='johntyree@gmail.com',
    license='GPL3+',
    url='http://github.com/johntyree/knobby',
    description="Interface for the Griffin PowerMate",
    keywords="PowerMate wheel usb",
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['knobby = knobby.handlers.fart:main'],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: "
        "GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Utilities",  # FIXME
    ],
)
