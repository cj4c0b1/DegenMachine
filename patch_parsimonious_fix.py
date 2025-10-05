import inspect
import sys

def getargspec(func):
    """
    A replacement for inspect.getargspec() that works in Python 3.11+
    """
    sig = inspect.signature(func)
    args = []
    varargs = None
    kwonlyargs = []
    kwonlydefaults = {}
    defaults = []
    
    for param in sig.parameters.values():
        if param.kind == param.POSITIONAL_OR_KEYWORD:
            args.append(param.name)
            if param.default != param.empty:
                defaults.append(param.default)
        elif param.kind == param.VAR_POSITIONAL:
            varargs = param.name
        elif param.kind == param.VAR_KEYWORD:
            varkw = param.name
        elif param.kind == param.KEYWORD_ONLY:
            kwonlyargs.append(param.name)
            if param.default != param.empty:
                kwonlydefaults[param.name] = param.default
    
    if not defaults:
        defaults = None
    elif len(defaults) < len(args):
        defaults = tuple([None] * (len(args) - len(defaults)) + list(defaults))
    else:
        defaults = tuple(defaults)
    
    return inspect.ArgSpec(args, varargs, varkw, defaults)

# Apply the patch to the inspect module
import inspect as _inspect
_inspect.getargspec = getargspec

# Import parsimonious after patching
import parsimonious  # noqa: F401
