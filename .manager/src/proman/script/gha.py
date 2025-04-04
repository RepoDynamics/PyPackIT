from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import actionman as _actionman
import github_contexts as _github_contexts
import mdit
import pyserials as ps
from github_contexts.github.enum import EventType as _EventType
from loggerman import logger as _logger
from rich.text import Text

from proman import event_handler as _handler
from proman import exception as _exception
from proman.dstruct import Token
from proman.output import OutputManager
from proman.report import Reporter, make_sphinx_target_config

if TYPE_CHECKING:
    import argparse


def run(
    path_repo_base: str | Path,
    path_repo_head: str | Path,
    token_github: str,
    token_zenodo: str,
    token_zenodo_sandbox: str,
    github_context: _github_contexts.GitHubContext,
):
    _logger.section("Execution")
    event_to_handler = {
        _EventType.ISSUES: _handler.IssuesEventHandler,
        _EventType.ISSUE_COMMENT: _handler.IssueCommentEventHandler,
        _EventType.PULL_REQUEST: _handler.PullRequestEventHandler,
        _EventType.PULL_REQUEST_TARGET: _handler.PullRequestTargetEventHandler,
        _EventType.PUSH: _handler.PushEventHandler,
        _EventType.SCHEDULE: _handler.ScheduleEventHandler,
        _EventType.WORKFLOW_DISPATCH: _handler.WorkflowDispatchEventHandler,
    }

    reporter = Reporter(github_context=github_context)
    output_writer = OutputManager()
    handler_class = event_to_handler.get(github_context.event_name)
    current_log_section_level = _logger.current_section_level
    if handler_class:
        try:
            handler_class(
                github_context=github_context,
                reporter=reporter,
                output_writer=output_writer,
                admin_token=token_github,
                zenodo_token=token_zenodo,
                zenodo_sandbox_token=token_zenodo_sandbox,
                path_repo_base=path_repo_base,
                path_repo_head=path_repo_head,
            ).run()
        except _exception.ProManException:
            _logger.section_end(target_level=current_log_section_level)
            _finalize(
                github_context=github_context,
                reporter=reporter,
                output_writer=output_writer,
                repo_path=path_repo_head,
            )
            return
        except Exception as e:
            traceback = _logger.traceback()
            error_name = e.__class__.__name__
            _logger.critical(
                f"Unexpected Error: {error_name}",
                traceback,
            )
            reporter.add(
                "main",
                status="fail",
                summary=f"An unexpected error occurred: `{error_name}`",
                body=mdit.element.admonition(
                    title=error_name,
                    body=traceback,
                    type="error",
                    dropdown=True,
                    opened=True,
                ),
            )
            _logger.section_end(target_level=current_log_section_level)
            _finalize(
                github_context=github_context,
                reporter=reporter,
                output_writer=output_writer,
                repo_path=path_repo_head,
            )
            return
    else:
        supported_events = mdit.inline_container(
            *(mdit.element.code_span(enum.value) for enum in event_to_handler),
            separator=", ",
        )
        event_description = mdit.inline_container(
            "Unsupported triggering event ",
            mdit.element.code_span(github_context.event_name.value),
        )
        reporter.event(event_description)
        summary = mdit.inline_container(
            "Unsupported triggering event. Supported events are: ",
            supported_events,
        )
        reporter.add("main", status="skip", summary=summary)
    _finalize(
        github_context=github_context,
        reporter=reporter,
        output_writer=output_writer,
        repo_path=path_repo_head,
    )
    return


def run_cli(args: argparse.Namespace):
    """Run the CLI.

    Parameters
    ----------
    args : argparse.Namespace, optional
        The parsed arguments. If None, the arguments are parsed from sys.argv.
    """
    path_repo_base = _actionman.env_var.read(name="PATH_REPO_BASE", typ=str)
    path_repo_head = _actionman.env_var.read(name="PATH_REPO_HEAD", typ=str)
    admin_token = Token(
        _actionman.env_var.read(name="GITHUB_ADMIN_TOKEN", typ=str), name="GitHub Admin"
    )
    zenodo_token = Token(_actionman.env_var.read(name="ZENODO_TOKEN", typ=str), name="Zenodo")
    zenodo_sandbox_token = Token(
        _actionman.env_var.read(name="ZENODO_SANDBOX_TOKEN", typ=str), name="Zenodo Sandbox"
    )
    github_context = _github_contexts.github.create(
        context=_actionman.env_var.read(name="GITHUB_CONTEXT", typ=dict)
    )

    run(
        path_repo_base=path_repo_base,
        path_repo_head=path_repo_head,
        token_github=admin_token,
        token_zenodo=zenodo_token,
        token_zenodo_sandbox=zenodo_sandbox_token,
        github_context=github_context,
    )
    return


@_logger.sectioner("Output Generation")
def _finalize(
    github_context: _github_contexts.GitHubContext,
    reporter: Reporter,
    output_writer: OutputManager,
    repo_path: str,
):
    workflow_output, report_path = output_writer.generate(failed=reporter.failed)
    _write_step_outputs(workflow_output)

    report_gha, report_full = reporter.generate()
    _write_step_summary(report_gha)

    log = _logger.report
    target_config, sphinx_output = make_sphinx_target_config()
    log.target_configs["sphinx"] = target_config
    log_html = log.render(target="sphinx")
    _logger.info(
        "Log Generation Logs",
        mdit.element.rich(Text.from_ansi(sphinx_output.getvalue())),
    )
    filename = (
        f"{github_context.repository_name}-workflow-run"
        f"-{github_context.run_id}-{github_context.run_attempt}.{{}}.{{}}"
    )
    dir_path = Path(repo_path) / report_path / "proman"
    dir_path.mkdir()

    output_str = ps.write.to_json_string(workflow_output, sort_keys=True, indent=3, default=str)

    for file_data, file_suffix, file_ext in (
        (output_str, "output", "json"),
        (report_full, "report", "html"),
        (log_html, "log", "html"),
    ):
        file = dir_path / filename.format(file_suffix, file_ext)
        file.write_text(file_data)
    return


def _write_step_outputs(kwargs: dict) -> None:
    log_outputs = []
    for name, value in kwargs.items():
        output_name = name.lower().replace("_", "-")
        written_output = _actionman.step_output.write(name=output_name, value=value)
        log_outputs.append(
            mdit.element.code_block(
                written_output,
                caption=f"{output_name} [{type(value).__name__}]",
            )
        )
    _logger.debug("GHA Step Outputs", *log_outputs)
    return


def _write_step_summary(content: str) -> None:
    _logger.debug("GHA Summary Output", mdit.element.code_block(content))
    _actionman.step_summary.write(content)
    return
