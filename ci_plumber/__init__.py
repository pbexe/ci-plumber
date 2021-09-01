# Programmatically get module version so that it is always in sync with poetry.
try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata  # type: ignore

__version__ = importlib_metadata.version(__name__)

from ci_plumber.module_attributes import Module_attribute
