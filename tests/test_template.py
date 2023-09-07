# Standard libraries
import sys

# Self
import templaterepo


def test_import():
    """Sample test, will always pass so long as import statement worked."""
    assert "templaterepo" in sys.modules
