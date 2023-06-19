"""
A Short description of the module.

A longer description of the module

References
----------
* A sample reference
"""


class TemplateClass:
    """
    A short description of the class

    A longer description of the class
    """

    def __init__(self, name: str, user_id: int):
        """
        Parameters
        ----------
        name : str
            Name of the user.
        user_id : int
            User ID.
        """
        self._name = name
        self._user_id = user_id
        return

    @property
    def name(self) -> str:
        """
        Name of the user.
        """
        return self._name

    def email(self, website: str) -> str:
        """
        Email of the user for a given website.

        Parameters
        ----------
        website : str
            Website Address in the form 'example.com'.

        Returns
        -------
            Email address.
        """
        return f"{self._user_id}@{website}"


def template_function_in_module(x, y):
    """
    This is a function inside a module.

    This function adds two given numbers.

    Parameters
    ----------
    x : int
        First number to add.
    y : int
        Second number to add.

    Returns
    -------
    int
    """
    return x + y
