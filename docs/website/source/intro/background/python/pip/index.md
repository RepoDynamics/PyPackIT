(bg-pip)=
# Pip

[Pip](https://pip.pypa.io) is Python's official package manager maintained by [PyPA](#bg-pypa), 
used to install and manage Python packages. 
As a command-line tool often included with Python distributions, 
pip automates the installation of Python packages and their dependencies, 
significantly simplifying the setup and deployment of Python environments.

Pip can be used to download and install packages
from source distributions and binary wheels available locally or
in online repositories such as [PyPI](#bg-pypi)
and version control systems like Git.
It integrates seamlessly with Python virtual environments, 
ensuring project-specific dependency isolation.
Functionalities include version control with 
[requirement specifiers](https://pip.pypa.io/en/stable/reference/requirement-specifiers/),
bulk installation via [`requirements.txt`](https://pip.pypa.io/en/stable/reference/requirements-file-format/)
and [constraints](https://pip.pypa.io/en/stable/user_guide/#constraints-files) files,
and [editable installations](https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs).
