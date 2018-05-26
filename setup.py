"""Configaro setup module."""

from setuptools import setup

from docs.source.conf import release_metadata

with open('README.md') as infile:
    long_description = infile.read()

with open('requirements.txt') as infile:
    requirements = [line.strip() for line in infile.readlines()]

release_metadata.update(dict(
    py_modules=['configaro'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    zip_safe=True,
    test_suite='tests',
))

if __name__ == '__main__':
    setup(**release_metadata)
