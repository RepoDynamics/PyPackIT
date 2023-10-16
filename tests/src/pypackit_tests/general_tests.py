import sys
import pypackit as pkg


def version_test():
    """Sample test, will always pass so long as import statement worked."""
    assert isinstance(pkg.__version__, str)
    assert len(pkg.__version__.split(".")) >= 3
