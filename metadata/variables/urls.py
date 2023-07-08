"""URLs relevant to the project.
"""

from . import project

HOMEPAGE: str = f"https://.rtfd.io"

LICENSE: str = f"{HOMEPAGE}/license"


CONTRIBUTORS: str = f"{HOMEPAGE}/about#contributors"
"""List of contributors according to All Contributors specifications."""


GITHUB_REPO: str = f"https://github.com/{project.GITHUB_USER}/{project.GITHUB_REPO}"

ISSUE_TRACKER: str = f"{GITHUB_REPO}/issues"
UPDTATE_TRACKER: str = f"{GITHUB_REPO}/pulls"
DISCUSSIONS: str = f"{GITHUB_REPO}/discussions"

CONTRIBUTING: str = "docs/CONTRIBUTING.md"
CODE_OF_CONDUCT: str = "docs/CODE_OF_CONDUCT.md"
SECURITY: str = "docs/SECURITY.md"
SUPPORT: str = "docs/SUPPORT.md"


PYPI: str = f"https://pypi.org/project/{project.PACKAGE_NAME}/"
