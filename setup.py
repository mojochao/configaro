"""Configaro setup module."""
import json

from setuptools import setup

with open('README.md') as infile:
    long_description = infile.read()

with open('release.json') as infile:
    release_metadata = json.load(infile)

with open('requirements.txt') as infile:
    requirements = [line.strip() for line in infile.readlines()]

release_metadata.update(dict(
    py_modules=['configaro'],
    install_requires=requirements,
    zip_safe=True,
    test_suite='tests',
))

if __name__ == '__main__':
    setup(**release_metadata)
