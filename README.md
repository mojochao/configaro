configaro
=========

[![Build Status](https://travis-ci.org/mojochao/configaro.svg?branch=master)](https://travis-ci.org/mojochao/configaro)

[![Documentation Status](https://readthedocs.org/projects/configaro/badge/?version=latest)](http://configaro.readthedocs.io/?badge=latest)

What is it?
-----------

**configaro** is a Python 3.6 configuration library that's music to your ears.

Why should I care?
------------------

**configaro** has been created with the following design goals in mind:

- provide a single file library with minimal dependencies
- provide one with a simple, expressive API that is easy to use and gets out of your way
- provide one that allows for hierarchical config data with dot-addressable access
- provide one that allows for defaults and locals config modules

If this sounds appealing to you, take a look:

    import configaro as cfg

    # Initialize the library with the name of the package containing your defaults.py config module
    cfg.init('mypkg.config')

    # Get the entire config object
    config = cfg.get()
    print(config)  # prints "{'greeting': 'Hello', 'subject': 'World'}"

    # Config object provide attribute access style in addition to dict access style.
    print('f{config.greeting}, {config.subject}!')  # prints "Hello, World!"

    # Config objects may be updated quite flexibly as well.
    cfg.put(greeting='Goodbye', subject='Folks'}
    cfg.put({'greeting': 'Goodbye', 'subject': 'Folks'})
    cfg.put('greeting=Goodbye subject=Folks')

What about earlier Python?
==========================

**configaro** uses Python 3.6 features and I have zero interest in supporting
earlier versions.  If you are still using them then move along -- there's
nothing to see here.

Installation
------------

**configaro** may be installed from the Python package index:

    $ pip3 install configaro

It may also be installed from source:

    $ git clone https://github.com/mojochao/configaro.git
    $ pip3 install .

If you install from source with `.[dev]` you should be able to run tests:

    $ tox

Documentation
-------------

`configaro` documentation is hosted on [Read The Docs](https://configaro.readthedocs.io/en/latest/)
and should be consulted for information on integrating it into your project.
