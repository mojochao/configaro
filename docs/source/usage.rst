.. _configaro_usage:

Usage
=====

Understand configaro
--------------------

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

Add configaro to your project
-----------------------------

**configaro** must be added to your project before use.

Add the package dependency using `pipenv <https://docs.pipenv.org/>`_::

    $ cd ~/projects/demo_prj
    $ pipenv install configaro

Alternatively, add it to your ``requirements.txt`` file and ``pip3`` install
it into your Python environment::

    $ pip3 install -r requirements.txt

Add defaults config module
--------------------------

If a ``demo_prj`` project contains a ``demo_pkg`` package, create a
``demo_prj/demo_pkg/config`` config package directory::

    $ mkdir demo_pkg/config

Create a ``demo_pkgr/config/defaults.py`` config module in that directory::

    $ cat >> demo_pkg/config/defaults.py << EOF
    config = {
        'greeting': 'hello',
        'subject': {
            'first_name': 'Joe',
            'last_name': 'World'
        }
    }
    EOF

Initialize the library
----------------------

In your code, initialize the **configaro** library with the :meth:`configaro.init`
API and the name of your config package::

    import configaro
    configaro.init('demo_pkg.config')

Query configuration
-------------------

Query the config object with the :meth:`configaro.get` API::

    config = configaro.get()
    print(f'{config.greeting}, {config.subject}!')

..  note::

    Config properties are dot-addressable.  This is more convenient
    than using dict-style ``data['prop']`` access, however that works as well.

You can grab a specific sub-configuration by passing in the name of a
specific property to query::

    greeting = configaro.get('greeting')
    subject = configaro.get('subject')
    print(f'{greeting}, {subject}!')

You can query multiple specific properties at one time::

    greeting, subject = configaro.get('greeting', 'subject')
    print(f'{greeting}, {subject}!')

You can grab the entire subject config data by its property name::

    configaro.get('subject')

You can grab a nested config value with its dot-addressed property name::

    configaro.get('subject.first_name')

Modify configuration
--------------------

Modify the config object with the :meth:`configaro.put` api::

    configaro.put('subject.first_name=Jane')

If you are not modifying hierarchical config data, you can use the keyword
args invocation::

    configaro.put(greeting='Aloha')

..  note::

    This will not work with hierarchical config data as the *dot*, or ``.``,
    character is not valid in keyword args as key names must be valid Python
    names.

    The *hyphen*, or ``-``, character is similarly not allowed in keyword args.
    Save yourself some pain and use the *underscore*, or ``_``, character instead.

Add locals config module
------------------------

The config data found in the *defaults* config module can be overridden with
config data found in the *locals* config module.  The *locals* config module
can be loaded from one of three sources, in precedence order from highest to
lowest:

- a locals config module path passed to :meth:`configaro.init` API
- a locals config module path specified by environment variable name passed to :meth:`configaro.init` API
- a locals config module path found in the config package passed to :meth:`configaro.init` API

If no *locals* config module is found, the config object will contain only
the *defaults* config module's config data.

..  warning::

    If you use a ``locals.py`` config module in the config package directory,
    ensure that you add its file path to your ``.gitignore`` file, otherwise
    it will always be found, effectively becoming a second *defaults* config
    module.

