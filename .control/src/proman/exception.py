from __future__ import annotations

from functools import partial as _partial
from typing import TYPE_CHECKING as _TYPE_CHECKING

import ruamel.yaml as _yaml
import mdit as _mdit
import pyserials as _ps
from loggerman import logger as _logger
from exceptionman import ReporterException as _ReporterException

if _TYPE_CHECKING:
    from typing import Literal
    from pathlib import Path
    from mdit import Document
    from pylinks.exception.api import WebAPIError


class PromanError(_ReporterException):
    """Base class for all exceptions raised by ControlMan."""

    def __init__(self, report: Document | None = None):
        if report:
            sphinx_config = {"html_title": "ProMan Error Report"}
            report.target_configs["sphinx"] = _mdit.target.sphinx(
                renderer=_partial(
                    _mdit.render.sphinx, config=_mdit.render.get_sphinx_config(sphinx_config)
                )
            )
            super().__init__(report=report)
        return


class PromanRemoteGitHubRepoNotFoundError(PromanError):
    """Exception raised when issues are encountered with the Git(Hub) repository."""

    def __init__(
        self,
        repo_path: Path,
        remotes: dict,
    ):
        intro = "Failed to determine the GitHub address of the remote repository."
        problem = _mdit.inline_container(
            "The Git repository ",
            _mdit.element.code_span(repo_path.stem),
            " has no remote set for push to origin.",
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


class PromanDataReadError(PromanError):
    """Base class for all exceptions raised when a data cannot be read."""

    def __init__(
        self,
        intro,
        problem,
        section: dict | None = None,
        data: str | dict | None = None,
        cause: Exception | None = None,
    ):
        report = _mdit.document(
            heading="Data Read Error",
            body={"intro": intro, "problem": problem},
            section=section,
        )
        super().__init__(report)
        self.data = data
        self.cause = cause
        return


class PromanConfigFileReadError(PromanDataReadError):
    """Base class for all exceptions raised when a control center configuration file cannot be read."""

    def __init__(
        self,
        filepath: str | Path,
        data: str | dict,
        problem,
        section: dict | None = None,
        cause: Exception | None = None,
    ):
        intro = _mdit.inline_container(
            "Failed to read control center configuration file at ",
            _mdit.element.code_span(str(filepath)),
            ".",
        )
        super().__init__(
            intro=intro,
            problem=problem,
            data=data,
            section=section,
            cause=cause,
        )
        self.filepath = filepath
        return


class PromanInvalidConfigFileDataError(PromanConfigFileReadError):
    """Exception raised when a control center configuration file data is invalid YAML."""

    def __init__(self, cause: _ps.exception.read.PySerialsInvalidDataError):
        super().__init__(
            filepath=cause.filepath,
            data=cause.data,
            problem=cause.report.body["problem"].content,
            section=cause.report.section,
            cause=cause,
        )
        return


class PromanDuplicateConfigFileDataError(PromanConfigFileReadError):
    """Exception raised when a control center configuration file contains duplicate data."""

    def __init__(
        self,
        filepath: Path,
        cause: _ps.exception.update.PySerialsUpdateRecursiveDataError,
    ):
        problem = _mdit.inline_container(
            "The value of type ",
            _mdit.element.code_span(cause.type_data_addon.__name__),
            " at ",
            _mdit.element.code_span(cause.path),
            " already exists in another configuration file",
            "."
            if cause.problem_type == "duplicate"
            else _mdit.inline_container(
                " with type ", _mdit.element.code_span(cause.type_data.__name__), "."
            ),
        )
        super().__init__(
            filepath=filepath,
            data=cause.data_addon_full,
            problem=problem,
            cause=cause,
        )
        return


class PromanInvalidConfigFileTagError(PromanConfigFileReadError):
    """Base class for all exceptions raised when a control center configuration file contains an invalid tag."""

    def __init__(
        self,
        filepath: str | Path,
        data: str,
        problem,
        node: _yaml.ScalarNode,
        cause: Exception | None = None,
        section: dict | None = None,
    ):
        self.node = node
        self.start_line = node.start_mark.line + 1
        self.end_line = node.end_mark.line + 1
        self.start_column = node.start_mark.column + 1
        self.end_column = node.end_mark.column + 1
        self.tag_name = node.tag
        super().__init__(
            filepath=filepath,
            data=data,
            problem=problem,
            cause=cause,
            section=section,
        )
        return


class PromanEmptyTagInConfigFileError(PromanInvalidConfigFileTagError):
    """Exception raised when a control center configuration file contains an empty tag."""

    def __init__(
        self,
        filepath: Path,
        data: str,
        node: _yaml.ScalarNode,
    ):
        problem = _mdit.inline_container(
            "The ",
            _mdit.element.code_span(node.tag),
            " tag at line ",
            _mdit.element.code_span(str(node.start_mark.line + 1)),
            " has no value.",
        )
        _logger.critical(
            "Empty Tag in Configuration File",
            problem,
        )
        super().__init__(
            filepath=filepath,
            data=data,
            problem=problem,
            node=node,
        )
        return


class PromanUnreachableTagInConfigFileError(PromanInvalidConfigFileTagError):
    """Exception raised when a control center configuration file contains an unreachable tag."""

    def __init__(
        self,
        filepath: Path,
        data: str,
        node: _yaml.ScalarNode,
        url: str,
        cause: WebAPIError,
    ):
        problem = _mdit.inline_container(
            "Failed to download external configurations from ",
            _mdit.element.code_span(url),
            " defined in ",
            _mdit.element.code_span(node.tag),
            " tag at line ",
            _mdit.element.code_span(str(node.start_mark.line + 1)),
            ". ",
            cause.report.body["intro"].content,
        )
        _logger.critical(
            "Unreachable Tag in Configuration File",
            problem,
            cause.report.section["details"].content,
        )
        super().__init__(
            filepath=filepath,
            data=data,
            problem=problem,
            node=node,
            cause=cause,
            section=cause.report.section,
        )
        return


class PromanInvalidMetadataError(PromanDataReadError):
    """Exception raised when a control center metadata file contains invalid data."""

    def __init__(
        self,
        cause: _ps.exception.read.PySerialsReadException,
        filepath: str | Path | None = None,
        commit_hash: str | None = None,
    ):
        intro = _mdit.inline_container(
            "Failed to read project metadata ",
            _mdit.inline_container(
                "file at ",
                _mdit.element.code_span(str(filepath)),
                _mdit.inline_container(
                    " from commit hash ",
                    _mdit.element.code_span(str(commit_hash)),
                )
                if commit_hash
                else "",
            )
            if filepath
            else "from input string",
            ".",
        )
        super().__init__(
            intro=intro,
            problem=cause.report.body["problem"].content,
            section=cause.report.section,
            data=getattr(cause, "data", None),
            cause=cause,
        )
        return


class PromanSchemaValidationError(PromanDataReadError):
    """Exception raised when a control center file is invalid against its schema."""

    def __init__(
        self,
        source: Literal["source", "compiled"] = "source",
        before_substitution: bool = False,
        cause: _ps.exception.validate.PySerialsValidateException | None = None,
        problem: str | None = None,
        json_path: str | None = None,
        data: dict | None = None,
    ):
        intro = _mdit.inline_container(
            "Control center configurations are " if source == "source" else "Project metadata is ",
            "invalid against the schema",
            "."
            if not json_path
            else _mdit.inline_container(
                " at path ",
                _mdit.element.code_span(f"$.{json_path}"),
                ".",
            ),
        )
        problem = problem or cause.report.body["problem"].content if cause else ""
        _logger.critical(
            "Schema Validation Error",
            intro,
            problem,
        )
        super().__init__(
            intro=intro,
            problem=problem,
            section=cause.report.section if cause else None,
            data=data or cause.data,
            cause=cause,
        )
        self.source = source
        self.before_substitution = before_substitution
        self.key = json_path
        return
