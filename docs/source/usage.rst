.. _configaro_usage:

Usage
=====

..  toctree::
    :maxdepth: 2
    :caption: Contents

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

