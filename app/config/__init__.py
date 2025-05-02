__all__ = ["var"]


# Import the submodules
try:
    from . import var

except ImportError as e:
    raise ImportError(f"Error importing submodules: {e}")
