#!/usr/bin/env python3
from setuptools import setup, find_packages


setup(
    name='woodenwaiter',
    version='0.0.2',
    author='zhanghaoran',
    author_email='haoranzeus@gmail.com',
    url='https://github.com/haoranzeus/woodenwaiter',
    description='A producer-customer model based on redis',
    packages=find_packages(exclude=['tests']),
    install_requires=['redis'],
)
