.. _configaro_docs:

=========
configaro
=========

**configaro** is a Python 3.6 configuration library that's music to your ears.

Features
========

**configaro** has been created with the following design goals in mind:

    - provide a single file library with minimal dependencies
    - provide one with a simple, expressive API that is easy to use and gets out of your way
    - provide one that allows for hierarchical config data with dot-addressable access
    - provide one that allows for config data defaults and local overrides

Concepts
========

**configaro** provides a **config object** loaded from a *defaults*
**config module** in the **config package** and an optional *locals*
**config module** in the **config package** or other directory.

A **config package** is the name of a Python package to search for
*defaults* and *locals* **config modules**.

A **config module** is a Python module containing **config data** in a
:class:`dict` module attribute named *config*. Values found in a *locals*
**config module** will override those found in the *defaults* **config module**.

A **config object** is a `dot-addressable dict <https://github.com/Infinidat/munch>`_
containing **config data** loaded from a *defaults* and optional *locals*
**config modules**.  The config object is built by calling the :meth:`configaro.init`
API.  After initialization the config object, or any portion of it, may be
queried with the :meth:`configaro.get` API or modified with the
:meth:`configaro.put` API.

A **config property** is a string identifying a config object or config
config value in a dot-addressable format, such as ``inner.prop``.

A **config value** is a scalar value of some type, typically *None*, *bool*,
*float*, *int* or *str* type, accessed by **config property**.

Usage
=====

Add configaro to your project
-----------------------------

**configaro** must be added to your project before use.

Add the package dependency using `pipenv <https://docs.pipenv.org/>`_::

    $ cd ~/projects/demo_prj
    $ pipenv install configaro

Alternatively, add it to your ``requirements.txt`` file and ``pip3`` install
it into your Python environment::

    $ pip3 install -r requirements.txt

Add defaults config module to your project
------------------------------------------

Add a *defaults* config module to your config package directory::

    # mypkg/config/defaults.py
    config = {
        'inner': {
            'prop': 'some_value'
        }
    }

Import configaro
----------------

All APIs are provided by the **configaro** module::

    import configaro

Initialize the config object
----------------------------

The config object must be initialized before use.  At a minimum, it requires
the name of the config package containing the *defaults* config module
``defaults.py``::

    configaro.init('mypkg.config')

The config data provided by the *defaults* config module may be overridden
with config data provided by a *locals* config module.  This module, if it
exists, is loaded from one of the following locations in precedence order from
highest to lowest:

- locals path
- locals env var
- ``locals.py`` file in config package

The locals path and locals env var can optionally be passed as keyword
arguments::

    configaro.init('mypkg.config', locals_path='/etc/mypkg/locals.py', locals_env_var='MYPKG_LOCALS_PATH')

Once initialized, the config object may be queried with the :meth:`configaro.get`
function and modified with the :meth:`configaro.put` function.

Query the config object
-----------------------

To query the initialized config object, call :meth:`configaro.get` with no
arguments::

    config = configaro.get()

The returned config object provides dot-addressable config data access::

    value = config.inner.prop

You can query any portion of the config object my name.
Scalar config properties can be queried::

    value = configaro.get('inner.prop')

Nested config objects can also be queried::

    inner = configaro.get('inner')
    value = inner.prop

Multiple items can be returned at once by passing multiple positional
arguments::

    inner, another = configaro.get('inner', 'another')
    inner, another = configaro.get('inner another')

Modify the config object
------------------------

To modify the initialized config object, use the :meth:`configaro.put`
function.  To modify the entire config object, provide one dict argument::

    configaro.put({
        'inner': {
            'prop': 'some value'
        },
        'another': 'another_value'
    })

Any portion of of the config object can be similarly modified with a property
name and dict argument::

    configaro.put('inner', {'prop': 'some_value'})

Scalar config data can be modified with an update string::

    configaro.put('inner.prop=some_value')

Multiple items can be modified at once by passing multiple update strings::

    configaro.put('inner.prop=some_value', 'another=another_value')
    configaro.put('inner.prop=some_value another=another_value')

Update string values will be cast to None, bool, int and float values before
updating the config object.

Root config properties can also be modified by passing keyword arguments::

    configaro.put(another='another_value', inner={'prop': 'some_value'})

Caveats
=======

**configaro** uses Python 3.6 features and I have zero interest in supporting
earlier versions.  If you are still using them then move along -- there's
nothing to see here.

..  toctree::
    :maxdepth: 2
    :caption: Contents

    api
    releases

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
