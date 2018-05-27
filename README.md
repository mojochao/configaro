configaro configuration library
===============================

What is it?
-----------

`configaro` is a configuration library for Python 3 that's music to your ears.

Why should I care?
------------------

`configaro` has been created with the following design goals in mind:

- provide a single file library with minimal dependencies
- provide one with a simple, expressive API that is easy to use and gets out of your way
- provide one that allows for hierarchical config data supporting dot-addressable access 
- provide one that allows for defaults and locals config modules
- provide one with complete test coverage
- provide one with complete documentation

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


What about Python 2?
--------------------

I have zero interest in supporting Python 2 at this point.  If you are still
using Python 2 then move along -- there's nothing to see here.  Fork it if you
like and submit a pull request.

Installation
------------

`configaro` may be installed from the Python package index:

    $ pip3 install configaro

`configaro` may also be installed from source:

    $ git clone https://github.com/mojochao/configaro.git
    $ pip3 install .

If you install from source with `.[dev]` you should be able to run tests:

    $ pytest

Documentation
-------------

`configaro` documentation is hosted on [Read The Docs](https://configaro.readthedocs.io/en/latest/)
and should be consulted for information on integrating it into your project.
