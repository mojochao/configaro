# configaro configuration package

## What is it?


`configaro` is a Python 3 configuration package that's music to your ears.

## Why should I care?

`configaro` has been created with the following design goals in mind:

- provide a system with a simple API that is easy to use and gets out of your way
- provide a system that allows for hierarchical configuration data
- provide a system that provides configuration in a dot-addressable, attribute-access manner
- provide a system that allows for configuration defaults and local overrides
- provide a system with complete test coverage
- provide a system with complete documentation coverage

If this sounds appealing to you, keep on reading.

## Installation

Configaro may be installed from the Python package index:

    $ pip install configaro

Configaro may also be installed from source:

    $ git clone https://github.com/mojochao/configaro.git
    $ cd configaro
    $ python3 -m venv ./venv
    $ source ./venv/bin/activate
    (venv) $ pip install '.[all]'

If you install from source with `.[all]` you should be able to run tests:

    (venv) $ pytest

## Documentation

Documentation is hosted on readthedocs.

TBD
