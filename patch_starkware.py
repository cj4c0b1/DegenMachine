import sys
import importlib.util
import dataclasses
import functools

def patch_starkware():
    """
    Patch the starkware package to fix the mutable default argument issue.
    """
    try:
        # Check if starkware is installed
        spec = importlib.util.find_spec('starkware')
        if spec is None:
            return  # starkware is not installed
            
        # Import the problematic module
        from starkware.cairo.lang import instances
        
        # Patch the dataclass decorator to handle mutable defaults
        original_dataclass = dataclasses.dataclass
        
        def patched_dataclass(cls=None, /, **kwargs):
            if cls is None:
                return functools.partial(patched_dataclass, **kwargs)
                
            # Get the original class attributes
            cls_annotations = cls.__dict__.get('__annotations__', {})
            
            # Process each field to handle mutable defaults
            for name, field_type in cls_annotations.items():
                if hasattr(cls, name):
                    default = getattr(cls, name)
                    if isinstance(default, (list, dict, set)):
                        # Replace mutable defaults with field(default_factory=...)
                        default_factory = type(default)
                        delattr(cls, name)
                        setattr(cls, name, dataclasses.field(default_factory=default_factory))
            
            # Create the dataclass with the original decorator
            return original_dataclass(cls, **kwargs)
        
        # Apply the patch to the module
        instances.dataclasses.dataclass = patched_dataclass
        
        # Re-import the module to apply the patch
        importlib.reload(instances)
        
    except Exception as e:
        print(f"Warning: Failed to patch starkware: {e}")
        print("Consider using an older version of Python (3.8-3.10) or a different starkware version.")

# Apply the patch when this module is imported
patch_starkware()
