# Non-standard libraries
import template_package
import template_package._utils as utils


def test_import():
    """Sample test, will always pass so long as import statement worked."""
    # Standard libraries
    import sys

    assert "template_package" in sys.modules


def test_sample():
    assert utils.returns_2() == 2
