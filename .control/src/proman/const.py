"""Constants.

These include paths to files and directories in the user repository.
"""

METADATA_LINKER_PATH = ".github/.pypackit"

OUTPUT_RELEASE_REPO_PATH = "repo"
OUTPUT_RELEASE_ARTIFACT_PATH = "artifacts"

RELATIVE_TEMPLATE_KEYS = ["__temp__"]
CUSTOM_KEY = "__data__"

# GitHub Constants
DIRPATH_ISSUES = ".github/ISSUE_TEMPLATE"
FILEPATH_ISSUES_CONFIG = f"{DIRPATH_ISSUES}/config.yml"
DIRPATH_DISCUSSIONS = ".github/DISCUSSION_TEMPLATE"
FILEPATH_PULL_TEMPLATE_MAIN = ".github/pull_request_template.md"
DIRPATH_PULL_TEMPLATES = ".github/PULL_REQUEST_TEMPLATE"

# Git Constants
ISSUE_FORM_TOP_LEVEL_KEYS = (
    "name",
    "description",
    "title",
    "projects",
)
ISSUE_FORM_BODY_KEY = "body"
ISSUE_FORM_BODY_TOP_LEVEL_KEYS = (
    "type",
    "id",
    "attributes",
    "validations",
)

# Python Constants
FILENAME_PACKAGE_TYPING_MARKER = "py.typed"
FILENAME_PKG_PYPROJECT = "pyproject.toml"
