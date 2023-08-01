"""
General functionalities used in the package.

A short description.

A long description.
"""


# Standard libraries
import inspect


def f():
    s = inspect.stack()
    print(s)
    module_name = inspect.getmodule(s[1][0]).__name__
    print(module_name)


def returns_2() -> int:
    """
    Sample function.

    Function description
    """
    return 2


f()
