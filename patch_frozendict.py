import collections.abc
import sys

# Add the mapping ABCs to collections module
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping

# Import frozendict after patching collections
from frozendict import frozendict

# Make frozendict available in the global namespace
sys.modules['frozendict'] = sys.modules[__name__]
