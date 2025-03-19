from pathlib import Path as _Path

import mdit as _mdit
from loggerman import logger as _logger
import pyserials as _ps

from controlman.exception import ControlManException as _ControlManException


class RemoteGitHubRepoNotFoundError(_ControlManException):
    """Exception raised when issues are encountered with the Git(Hub) repository."""

    def __init__(
        self,
        repo_path: _Path,
        remotes: dict,
    ):
        intro = "Failed to determine the GitHub address of the remote repository."
        problem = _mdit.inline_container(
            "The Git repository ",
            _mdit.element.code_span(repo_path.stem),
            " has no remote set for push to origin."
        )
        remotes_code_block = _mdit.element.code_block(
            content=_ps.write.to_yaml_string(remotes),
            language="yaml",
        )
        remotes_admonition = _mdit.element.admonition(
            title="Found Remotes",
            body=remotes_code_block,
            type="note",
            dropdown=True,
        )
        _logger.critical(
            "Repository Data",
            intro,
            problem,
            remotes_admonition,
        )
        report = _mdit.document(
            heading="Repository Error",
            body={
                "intro": intro,
                "problem": problem,
            },
            section={
                "details": _mdit.document(
                    heading="Error Details",
                    body=remotes_admonition,
                )
            },
        )
        super().__init__(report)
        self.repo_path = repo_path
        return


class ControlManWebsiteError(_ControlManException):
    """Exception raised when issues are encountered with the website."""

    def __init__(self, problem: str):
        report = _mdit.document(
            heading="Website Error",
            body={
                "intro": "An error occurred with the website.",
                "problem": problem,
            },
        )
        super().__init__(report)
        return


class ControlManHookError(_ControlManException):
    """Exception raised when issues are encountered with the hook manager."""

    def __init__(self, details, hook_name: str | None = None, problem = None):
        intro = _mdit.inline_container(
            "Failed to ",
            "initialize user hooks." if hook_name is None else _mdit.inline_container(
                "execute user hook ",
                _mdit.element.code_span(hook_name),
                "."
            ),
        )
        body = {"intro": intro, "problem": problem} if problem else {"intro": intro}
        report = _mdit.document(
            heading="User Hook Error",
            body=body,
            section={
                "details": _mdit.document(
                    heading="Error Details",
                    body=details,
                )
            }
        )
        super().__init__(report)
        return
