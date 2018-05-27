.. _configaro_api:

API
===

**configaro** is provided as a single module.

It has a spartan set of three APIs:

- :meth:`configaro.init`
- :meth:`configaro.get`
- :meth:`configaro.put`

It also has several error classes:

- :class:`configaro.ConfigaroError`
- :class:`configaro.ConfigNotFoundError`
- :class:`configaro.ConfigNotValidError`
- :class:`configaro.NotInitializedError`
- :class:`configaro.PropertyNotFoundError`
- :class:`configaro.PropertyNotScalarError`
- :class:`configaro.UpdateNotValidError`

..  note::

    At the moment, the `configaro API documentation <https://configaro.readthedocs.io/en/latest/api.html>`_
    built and hosted by `Read the Docs <https://readthedocs.org>`_ is not being correctly generated.
    When built in the  `Read the Docs build process <https://docs.readthedocs.io/en/latest/builds.html>`_,
    Sphinx is unable to generate the full API docs, as the *automodule* directive is unable to find
    the module, even though the proper directory has been added to ``sys.argv`` in
    ``docs/source/conf.py``.

    To build and view the API docs::

        $ git clone https://github.com/mojochao/configaro.git
        $ cd configaro
        $ pip3 install -e '.[dev]'
        $ python3 setup.py build_sphinx
        $ cd build/sphinx/html
        $ python3 -m http.server
        $ open http://0.0.0.0:8000/

    I will continue to investigate, and hopefully resolve, this soon.

..  automodule:: configaro
    :members:
