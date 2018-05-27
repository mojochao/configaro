.. _configaro_releases:

=======
Changes
=======

..  toctree::
    :maxdepth: 2
    :caption: Contents:

.. _configaro_release_0_9_10:

0.9.10
======

Changes
-------

- sphinx documentation improvements

.. _configaro_release_0_9_9:

0.9.9
=====

Changes
-------

- refactored error class names to match documentation
- added sphinx doc builds to tox tests
- added fab automation of dist build and upload to PyPI

.. _configaro_release_0_9_8:

0.9.8
=====

Changes
-------

- documented readthedocs API documentation fail

.. _configaro_release_0_9_7:

0.9.7
=====

Features
--------

- improvements to API documentation

.. _configaro_release_0_9_6:

0.9.6
=====

Features
--------

- improvements to Usage documentation

.. _configaro_release_0_9_5:

0.9.5
=====

Features
--------

- :meth:`configaro.get` now accepts *default* keyword arg to pass value to be returned if property is not found, instead of raising error
- expanded test coverage
- added coverage checks to tox tests
- added style checks to tox tests
- improvements to documentation

.. _configaro_release_0_9_4:

0.9.4
=====

Features
--------

- tox automation
- improvements to documentation
- improvements to :meth:`configaro.put` API

Changes
-------

- converted to single module library
- removed duplication of release metadata
- renamed :meth:`configaro.initialize` to :meth:`configaro.init`

.. _configaro_release_0_9_3:

0.9.3
=====

Fixes
-----

- documentation build fixes

.. _configaro_release_0_9_2:

0.9.2
=====

Fixes
-----

- packaging and requirements fixes

Deletions
---------

- :meth:`configaro.render`

.. _configaro_release_0_9_1:

0.9.1
=====

Features
--------

- documentation improvements

.. _configaro_release_0_9_0:

0.9.0
=====

Initial release of **configaro**.

Features
--------

- a simple API that is easy to use and gets out of your way
- a system that allows for hierarchical configuration data that supports dot-addressable property access
- a system that allows for configuration defaults and local overrides
- a system with high degree of test coverage
- a system with high degree of documentation

Fixes
-----

- none

Changes
-------

- none

Deprecations
------------

- none

Deletions
---------

- none
