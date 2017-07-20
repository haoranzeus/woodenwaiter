#!/usr/bin/env python3
from setuptools import setup, find_packages

readme = open('README.rst').read()

setup(
    name='woodenwaiter',
    version='0.0.3',
    author='zhanghaoran',
    author_email='zhanghaoran@cmhi.chinamobile.com',
    description='A producer-customer model based on redis',
    long_description=readme,
    packages=find_packages(exclude=['tests']),
    install_requires=['redis'],
)
