from typing import NamedTuple as _NamedTuple
from enum import Enum as _Enum


class DynamicFileType(_Enum):
    DEVCONTAINER_METADATA = ("devcontainer_metadata", "Devcontainer Metadata")
    DEVCONTAINER_DOCKERFILE = ("devcontainer_dockerfile", "Devcontainer Dockerfile")
    DEVCONTAINER_APT = ("devcontainer_apt", "Devcontainer Apt Packages")
    DEVCONTAINER_CONDA = ("devcontainer_conda", "Devcontainer Conda Environment")
    DEVCONTAINER_TASK_LOCAL = ("devcontainer_task_local", "Devcontainer Bash Tasks (Local)")
    DEVCONTAINER_TASK_GLOBAL = ("devcontainer_task_global", "Devcontainer Bash Tasks (Global)")
    DEVCONTAINER_FEATURE_METADATA = ("devcontainer_feature_metadata", "Devcontainer Feature Metadata")
    DEVCONTAINER_FEATURE_INSTALL = ("devcontainer_feature_install", "Devcontainer Feature Install Script")
    CUSTOM = ("custom", "Custom")
    CONFIG = ("config", "Configuration")
    TOOL_ENV_CONDA = ("tool_env_conda", "Tool Conda Environment")
    TOOL_ENV_PIP = ("tool_env_pip", "Tool Pip Environment")
    TOOL_CONFIG = ("tool_config", "Tool Configuration")
    WEB_CONFIG = ("web_config", "Website Configuration")
    DISCUSSION_FORM = ("discussion_form", "Discussion Category Form")
    ISSUE_FORM = ("issue_form", "Issue Form")
    PULL_TEMPLATE = ("pull_template", "Pull Request Template")
    PKG_CONFIG = ("pkg_config", "Package Configuration")
    TEST_CONFIG = ("test_config", "Test Suite Configuration")
    PKG_SOURCE = ("pkg_source", "Package Source")
    TEST_SOURCE = ("test_source", "Test Suite Source")
    DOC = ("document", "Document")


class DynamicDirType(_Enum):
    CONTROL = "Control Center"
    LOCAL = "Local"
    THEME = "Media"
    WEB_ROOT = "Website Root"
    WEB_SRC = "Website Source"
    PKG_ROOT = "Package Root"
    PKG_SRC = "Package Source"
    PKG_IMPORT = "Package Import"
    TEST_ROOT = "Test Suite Root"
    TEST_SRC = "Test Suite Source"
    TEST_IMPORT = "Test Suite Import"


class DynamicFileChangeTypeContent(_NamedTuple):
    title: str
    emoji: str


class DynamicFileChangeType(_Enum):
    REMOVED = DynamicFileChangeTypeContent("Removed", "🔴")
    MODIFIED = DynamicFileChangeTypeContent("Modified", "🟣")
    MOVED_MODIFIED = DynamicFileChangeTypeContent("Moved & Modified", "🟠")
    MOVED = DynamicFileChangeTypeContent("Moved", "🟡")
    ADDED = DynamicFileChangeTypeContent("Added", "🟢")
    UNCHANGED = DynamicFileChangeTypeContent("Unchanged", "⚪️")
    DISABLED = DynamicFileChangeTypeContent("Disabled", "⚫")
    INACTIVE = DynamicFileChangeTypeContent("Inactive", "🔵")


class DynamicFile(_NamedTuple):
    type: DynamicFileType
    subtype: tuple[str, str]
    content: str | None = None
    path: str | None = None
    path_before: str | None = None
    change: DynamicFileChangeType | None = None
    executable: bool = False


class DynamicDir(_NamedTuple):
    type: DynamicDirType
    path: str | None = None
    path_before: str | None = None
    change: DynamicFileChangeType | None = None
