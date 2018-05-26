"""Configaro setup module."""

from setuptools import find_packages, setup

with open('README.md') as infile:
    long_description = infile.read()

with open('requirements.txt') as infile:
    requirements = [line.strip() for line in infile.readlines()]

release_metadata = {
    'name': 'configaro',
    'description': "A configuration library that's music to your ears.",
    'version': '0.9.4',
    'url': 'https://github.com/mojochao/configaro',
    'author': 'Allen Gooch',
    'author_email': 'allen.gooch@gmail.com',
    'maintainer': 'Allen Gooch',
    'maintainer_email': 'allen.gooch@gmail.com',
    'license': 'MIT',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License'
    ],
    'keywords': [
        'configuration',
        'utility'
    ]
}

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
