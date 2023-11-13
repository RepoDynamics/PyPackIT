import templaterepo as pkg


def version_test():
    """Sample test"""
    assert isinstance(pkg.__version__, str)
    assert len(pkg.__version__.split(".")) >= 3
    return
