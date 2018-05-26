"""Configaro configuration system.

This configuration system provides one that:
- supports hierarchical configuration data
- supports attribute dot-addressable access
- supports defaults and local overrides
- does not leak module imports into the configuration

"""

from .configaro import *

__all__ = [
    'ConfigaroError',
    'ConfigNotFoundError',
    'ConfigNotValidError',
    'NotInitializedError',
    'PropertyNotFoundError',
    'PropertyNotScalarError',
    'get',
    'initialize',
    'put',
    'render'
]
