#!/usr/bin/env python3
from setuptools import setup, find_packages


setup(
    name='woodenwaiter',
    version='0.0.1',
    packages=find_packages(exclude=['tests']),
    install_requires=['redis'],
)
