"""Configaro setup module."""

from setuptools import find_packages, setup

from configaro.__metadata__ import release_metadata as configuration

packages = find_packages()

with open('requirements.txt') as infile:
    requirements = [line.strip() for line in infile.readlines()]

configuration.update(dict(
    packages=packages,
    install_requires=requirements,
    zip_safe=True,
    test_suite='tests',
))

setup(**configuration)
