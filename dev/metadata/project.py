
import datetime as _dt
import re
import sys
from typing import Literal

import requests


NAME: str = "PyPACKIT"
"""Name of the project.

This is only used in documents to refer to the project, so technically it can contain any unicode character,
but it is highly recommended to keep all names consistent, i.e. the package name, which has restrictions,
should be the normalized version of the project name. Therefore, we enforce the restrictions of a
valid non-normalized package name here, and then derive the package name from project name via normalization.

A valid name consists only of ASCII alphanumeric characters, period (.), underscore (_) and hyphen (-). 
It must start and end with a letter or number.

References
----------
* [Python Packaging User Guide > PyPA specifications > Package name normalization](https://packaging.python.org/en/latest/specifications/name-normalization/)
"""
if not re.match(r'^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$', NAME, flags=re.IGNORECASE):
    raise ValueError(
        "NAME can only consist of alphanumeric characters, period (.), underscore (_) and hyphen (-), "
        f"and can only start and end with an alphanumeric character, but got {NAME}. "
        "See https://packaging.python.org/en/latest/specifications/name-normalization/ for more details."
    )


SHORT_DESCRIPTION: str = "Effortlessly Create, Document, Test, Deploy, and Maintain Python Projects"
"""A single-sentence description of the project.
"""


LONG_DESCRIPTION: str = (
    "PyPackIT is an open-source software for creating other open-source software, "
    "specifically Python packages. It streamlines all the tedious and time-consuming "
    '"administrative" jobs of the software development process, so you can only focus ' 
    "on what truly matters -- implementing your ideas.\n"
    "With a single command, PyPackIT creates a professional and robust infrastructure."
)
"""A long description of the project that can have multiple paragraphs.
"""


KEYWORDS: list[str] = ["python", "package", "packaging", "repository", "documentation", "automated"]
"""Keywords to describe the project.
"""


OWNER: str = "aariam"


AUTHORS: list[str] = [
    "aariam",
]


START_YEAR: int = 2023
"""The year the project first started.

This is used e.g. to create a copyright notice.
"""
if START_YEAR < 1970 or START_YEAR > _dt.date.today().year:
    raise ValueError(
        f"START_YEAR must be between 1970 and {_dt.date.today().year}, but got {START_YEAR}."
    )


LICENSE: str = "GNU Affero General Public License v3 or later (AGPLv3+)"
"""Name of the license of the project.

    "GNU Affero General Public License v3 or later (AGPLv3+)", GNU_AGPLv3+
    "GNU Affero General Public License v3",
    "GNU General Public License v3 or later (GPLv3+)",
    "GNU General Public License v3 (GPLv3)",
    "GNU Lesser General Public License v3 or later (LGPLv3+)",
    "GNU Lesser General Public License v3 (LGPLv3)",
    "MIT License",
    "Boost Software License 1.0 (BSL-1.0)",
    "BSD License",
    "The Unlicense (Unlicense)"

"""


GITHUB: dict[Literal['USER', 'REPO'], str] = {
    'USER': OWNER,
    'REPO': re.sub(r'[^A-Za-z0-9_.-]', '-', NAME),
}
"""
GitHub repository address:
    USER : str
        Username of the repository owner
    REPO : str
        Repository name. 

Notes
-----
There seems to be no official GitHub documentation regarding repository naming rules.
Experimentally determined rules are (see https://stackoverflow.com/a/59082561/14923024):
GitHub repository names can only contain alphanumeric characters,
plus hyphen (-), underscore (_), and dot (.), i.e. they must match the regex '^[A-Za-z0-9_.-]+$'. 
All other characters are automatically replaced with hyphens.
Also, GitHub retains the capitalization only when displaying the repository name, 
otherwise, names are not case-sensitive. That is, "PyPackIT" will be displayed as is,
but any other capitalization of the word in any URL or address will also point to the same repository.
"""
# Validate repository name based on rules mentioned above.
if not re.match(r'^[A-Za-z0-9_.-]+$', GITHUB['REPO']):
    raise ValueError(
        "GITHUB_REPO can only contain alphanumeric characters, hyphens (-), underscores (_), and dots (.), " 
        f"but got {GITHUB['REPO']}."
    )
# Get the name of default branch
GITHUB['BRANCH']: str = requests.get(
    f"https://api.github.com/repos/{GITHUB['USER']}/{GITHUB['REPO']}"
).json()['default_branch']


