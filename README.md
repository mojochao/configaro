configaro configuration library
===============================

What is it?
-----------

`configaro` is a configuration library for Python 3 that's music to your ears.

Why should I care?
------------------

`configaro` has been created with the following design goals in mind:

- provide a system with a simple API that is easy to use and gets out of your way
- provide a system that allows for hierarchical configuration data that supports dot-addressable property access 
- provide a system that allows for configuration defaults and local overrides
- provide a system with complete test coverage
- provide a system with complete documentation

If this sounds appealing to you, keep on reading.

What about Python 2
-------------------

I have zero interest in supporting Python 2 at this point.  If you are still
using Python 2 then move along -- there's nothing to see here.  Fork it if you
like and submit a Pull Request.

Installation
------------

Configaro may be installed from the Python package index:

    $ pip3 install configaro

Configaro may also be installed from source:

    $ git clone https://github.com/mojochao/configaro.git
    $ pip3 install .

If you install from source with `.[dev]` you should be able to run tests:

    $ pytest

Documentation
-------------

Documentation is hosted on [Read The Docs](https://readthedocs.org/projects/configaro/)
and should be consulted for information on integrating ``configaro`` into your project.
