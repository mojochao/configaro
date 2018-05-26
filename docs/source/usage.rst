.. _configaro_usage:

Usage
=====

Add configaro to your project
-----------------------------

``configaro`` must be added to your project before use.

If using `pipenv <https://docs.pipenv.org/>`_::

    $ cd ~/projects/demo_prj
    $ pipenv install configaro

Alternatively, add the ``configaro`` package to your ``requirements.txt`` file
and ``pip`` install it into your Python 3 environment::

    $ pip install -r requirements.txt

Add defaults config module
--------------------------

``configaro`` loads config modules containing a ``config`` object dict attribute.

Add a ``config`` package to your project.  Assuming the ``demo_prj``
project has a top-level ``demo_pkg`` package, you should create a ``config``
directory underneath it::

    $ mkdir demo_pkg/config

Create a ``defaults.py`` config module in the created directory containing::

    # demo_prj/config/defaults.py
    config = {
        'greeting': 'hello',
        'subject': 'world'
    }

..  note::

    Although this config object is flat, hierarchical configuration is supported.

Initialize the library
----------------------

In your code, initialize the ``configaro`` library with the ``init()``
API and the name of your config package::

    import configaro
    configaro.init('demo_pkg.config')

Query configuration
-------------------

Query the whole configuration with the ``get`` api::

    config = configaro.get()
    print(f'{config.greeting}, {config.subject}!')

Notice that you config properties are dot-addressable.  This is much handier
than using dict-style square-brackets lookups.

You can grab a specific sub-configuration by passing in the name of a
specific property to query::

    greeting = configaro.get('greeting')
    subject = configaro.get('subject')
    print(f'{greeting}, {subject}!')

You can query multiple specific properties at one time::

    greeting, subject = configaro.get('greeting', 'subject')
    print(f'{greeting}, {subject}!')

Configurations may be hierarchical.  Assume a ``myproj/config/defaults.py``
module containing the following::

    config = {
        'greeting': 'hello',
        'subject': {
            'first_name': 'Joe',
            'last_name': 'World'
        }
    }

You can grab the entire subject config with::

    configaro.get('subject')

Or just a scalar leaf-node configuration value with::

    configaro.get('subject.first_name')

Modify configuration
--------------------

Any scalar leaf-node configuration property that exists in the defaults config
module may be updated::

    configaro.put('subject.first_name=Jane')

If you are not using hierarchical configuration data, you can use the keyword
args invocation::

    configaro.put(greeting='Aloha')

This will not work with hierarchical configuration data as the dot character is
not valid in keyword args.  Note that hyphens are also not allowed in keyword args.

Overriding defaults with locals
-------------------------------

The configuration defaults can be overridden with configuration locals.  These
locals can come from one of three sources:

- a locals config module path passed to :meth:`configaro.init`
- a locals config module path specified by environment variable name passed in at :meth:`configaro.init` time
- a locals config module path found in the config package passed in at :meth:`configaro.init` time

Any values found in the locals configuration object will override those found in
the defaults configuration object.

..  note::

    If you use a locals config module in the config package path, ensure that
    you add that path to your ``.gitignore`` file, otherwise it will always be
    present everywhere, effectively becoming a second defaults module.

