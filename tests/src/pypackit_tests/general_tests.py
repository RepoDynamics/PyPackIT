"""General tests"""  # noqa: D400


# Self
import pypackit as pkg


def version_test():
    """Sample test."""
    min_len_ver_elements = 3
    assert isinstance(pkg.__version__, str)
    assert len(pkg.__version__.split(".")) >= min_len_ver_elements
    return
