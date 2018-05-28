.. _configaro_api:

API Docs
========

Functions
---------

- :meth:`configaro.init`
- :meth:`configaro.get`
- :meth:`configaro.put`

Errors
------

- :class:`configaro.ConfigError`
- :class:`configaro.ConfigModuleNotFoundError`
- :class:`configaro.ConfigModuleNotValidError`
- :class:`configaro.ConfigObjectNotInitializedError`
- :class:`configaro.ConfigPropertyNotFoundError`
- :class:`configaro.ConfigPropertyNotScalarError`
- :class:`configaro.ConfigUpdateNotValidError`

..  note::

    At the moment, this page is not being correctly generated when built by the
    `Read the Docs build process <https://docs.readthedocs.io/en/latest/builds.html>`_,
    Sphinx is unable to generate the full API docs, as the *automodule* directive
    is unable to find the module, even though the proper directory has been added
    to ``sys.argv`` in ``docs/source/conf.py``.

    To build and view the API docs::

        $ git clone https://github.com/mojochao/configaro.git
        $ cd configaro
        $ pip3 install -e '.[dev]'
        $ python3 setup.py build_sphinx
        $ cd build/sphinx/html && python3 -m http.server
        $ open http://0.0.0.0:8000/

    This issue is being tracked `here <https://github.com/rtfd/readthedocs.org/issues/4154>`_.
    I will continue to investigate, and hopefully resolve, this soon.

..  automodule:: configaro
    :members:
