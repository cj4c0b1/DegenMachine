import sys
import inspect
import collections.abc
from unittest.mock import patch

# Add collections.Mapping for Python 3.10+ compatibility
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping

# Create a wrapper for getfullargspec to make it compatible with getargspec
def getargspec(func):
    """A replacement for inspect.getargspec that works in Python 3.11+"""
    fullargspec = inspect.getfullargspec(func)
    return inspect.ArgSpec(
        args=fullargspec.args,
        varargs=fullargspec.varargs,
        varkw=fullargspec.varkw,
        defaults=fullargspec.defaults
    )

# Apply the patches
sys.modules['inspect'].getargspec = getargspec

# Now import parsimonious after patching
import parsimonious  # noqa: F401
