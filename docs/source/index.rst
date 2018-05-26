.. _configaro_docs:

=======================
configaro documentation
=======================

..  toctree::
    :maxdepth: 2
    :caption: Contents:

.. _configaro_what:

What is it?
===========

``configaro`` is a Python configuration library that's music to your ears..

.. _configaro_design_goals:

Why should I care?
==================

``configaro`` has been created with the following design goals in mind:

- provide a system with a simple API that is easy to use and gets out of your way
- provide a system that allows for hierarchical configuration data that supports dot-addressable property access
- provide a system that allows for configuration defaults and local overrides
- provide a system with complete test coverage
- provide a system with complete documentation coverage

If this sounds appealing to you, keep on reading.

What about Python 2?
====================

I have zero interest in supporting Python 2 at this point.  If you are still
using Python 2 then move along -- there's nothing to see here.  Fork this repo
if you like and submit a pull request.

How do I use it?
================

Add configaro to your project
-----------------------------

First add the ``configaro`` package to your ``requirements.txt`` file and
install it into your Python 3 environment::

    $ cd ~/projects/my_project
    $ echo configaro >> requirements.txt
    $ pip3 install -r requirements.txt

Add configuration defaults
--------------------------

Next, add a ``config`` package to your project.  Assuming a project has a
top-level ``myproj`` package, you should create a ``config`` directory
underneath it::

    $ mkdir myproj/config

A ``defaults.py`` config module must be created in the directory just
created::

    $ cat << EOF > myproj/config/defaults.py
    config = {
        'greeting': 'hello',
        'subject': 'world'
    }
    EOF
    $

Initialize the package
----------------------

In your code, initialize the ``configaro`` package with the ``initialize``
API and the name of your config package::

    import configaro
    configaro.initialize('myproj.config')

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
            'first_name': 'Mr.',
            'last_name': 'World'
        }
    }

You can grab the entire subject config with::

    configaro.get('subject')

Or just a scalar leaf-node configuration value with::

    configaro.get('subject.first-name')

Modify configuration
--------------------

Any scalar leaf-node configuration property that exists in the defaults config
module may be updated::

    configaro.put('subject.first_name="Mrs."')

If you are not using hierarchical configuration data, you can use the keyword
args invocation::

    configaro.put(greeting='aloha')

This will not work with hierarchical configuration data as the dot character is
not valid in keyword args.  Note that hyphens are also not allowed in keyword args.

Overriding defaults with locals
-------------------------------

The configuration defaults can be overridden with configuration locals.  These
locals can come from one of three sources.

- a locals config file passed in at ``initialize()`` time
- a locals config file specified by environment variable passed in at ``initialize()`` time
- a locals config file found in the config package passed in at ``initialize()`` time

Any values found in the locals configuration object will override those found in
the defaults configuration object.

.. _configaro_api:

API Reference
=============

``configaro`` has a spartan set of three APIs and a handful of error classes.

configaro.__init__
==================

.. automodule:: configaro.__init__
   :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
