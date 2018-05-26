.. _configaro_api:

API
===

``configaro`` is provided as a single module.

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

..  automodule:: configaro
    :members:
