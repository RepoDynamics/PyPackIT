"""Constants for ControlMan.

These include paths to files and directories in the user repository.
"""


# ControlMan Constants
DIRPATH_CC_DEFAULT = ".control"

DIRNAME_LOCAL_REPORT = "reports"
DIRNAME_LOCAL_REPODYNAMICS = "RepoDynamics"

FILEPATH_METADATA = ".github/.repodynamics/metadata.json"
FILEPATH_CHANGELOG = ".github/.repodynamics/changelog.json"
FILEPATH_CONTRIBUTORS = ".github/.repodynamics/contributors.json"
FILEPATH_VARIABLES = ".github/.repodynamics/variables.json"
FILENAME_METADATA_CACHE = ".metadata_cache.yaml"
FILENAME_LOCAL_CONFIG = "config.yaml"

DIRNAME_CC_HOOK = "hooks"

FILENAME_CC_HOOK_REQUIREMENTS = "requirements.txt"
FILENAME_CC_HOOK_STAGED = "cca.py"
FILENAME_CC_HOOK_INLINE = "cca_inline.py"

FUNCNAME_CC_HOOK_INIT = "initialization"
FUNCNAME_CC_HOOK_LOAD = "load"
FUNCNAME_CC_HOOK_LOAD_VALID = "load_validation"
FUNCNAME_CC_HOOK_AUGMENT = "augmentation"
FUNCNAME_CC_HOOK_AUGMENT_VALID = "augmentation_validation"
FUNCNAME_CC_HOOK_TEMPLATE = "templating"
FUNCNAME_CC_HOOK_TEMPLATE_VALID = "templating_validation"
FUNCNAME_CC_HOOK_OUTPUT = "output_generation"
FUNCNAME_CC_HOOK_SYNC = "synchronization"
FUNCNAME_CC_HOOK_FINAL = "finalization"

CC_EXTENSION_TAG = u"!ext"

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
