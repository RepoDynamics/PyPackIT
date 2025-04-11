from __future__ import annotations

from typing import TYPE_CHECKING

import actionman

import mdit
import pyserials as ps
from github_contexts.github.enum import EventType
from loggerman import logger


from proman import event_handler as handler

if TYPE_CHECKING:
    from proman.manager import Manager


@logger.sectioner("Continuous Pipeline")
def run(manager: Manager):
    _set_git_api(manager=manager)
    event_to_handler = {
        EventType.ISSUES: handler.IssuesEventHandler,
        EventType.ISSUE_COMMENT: handler.IssueCommentEventHandler,
        EventType.PULL_REQUEST: handler.PullRequestEventHandler,
        EventType.PULL_REQUEST_TARGET: handler.PullRequestTargetEventHandler,
        EventType.PUSH: handler.PushEventHandler,
        EventType.SCHEDULE: handler.ScheduleEventHandler,
        EventType.WORKFLOW_DISPATCH: handler.WorkflowDispatchEventHandler,
    }
    handler_class = event_to_handler.get(manager.gh_context.event_name)
    if handler_class:
        try:
            handler_class(manager=manager).run()
        except Exception as e:
            _finalize(manager=manager, fail=True)
            raise e
    else:
        supported_events = mdit.inline_container(
            *(mdit.element.code_span(enum.value) for enum in event_to_handler),
            separator=", ",
        )
        event_description = mdit.inline_container(
            "Unsupported triggering event ",
            mdit.element.code_span(manager.gh_context.event_name.value),
        )
        manager.reporter.update_event_summary(event_description)
        summary = mdit.inline_container(
            "Unsupported triggering event. Supported events are: ",
            supported_events,
        )
        manager.reporter.update("main", status="skip", summary=summary)
    _finalize(manager=manager)
    return


def run_cli(args: dict) -> None:
    """Run from CLI."""
    run(manager=args["manager"])
    return


@logger.sectioner("Git API Setting")
def _set_git_api(manager: Manager) -> None:
    REPODYNAMICS_BOT_USER = (
        "RepoDynamicsBot",
        "146771514+RepoDynamicsBot@users.noreply.github.com",
    )
    # TODO: make authenticated
    # Refs:
    # - https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits
    # - https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key
    # - https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account
    # - https://github.com/crazy-max/ghaction-import-gpg
    # - https://stackoverflow.com/questions/61096521/how-to-use-gpg-key-in-github-actions
    # - https://github.com/sigstore/gitsign
    # - https://www.chainguard.dev/unchained/keyless-git-commit-signing-with-gitsign-and-github-actions
    # - https://github.com/actions/runner/issues/667
    # - https://sourceforge.net/projects/gpgosx/
    # - https://www.gnupg.org/download/

    apis = [("Target Repository", manager.git)]
    if manager.main.git.repo_path != manager.git.repo_path:
        apis.append(("Upstream Repository", manager.main.git))
    for title, git_api in apis:
        for user_type, name, email in (
            (
                "author",
                manager.gh_context.event.sender.login,
                manager.gh_context.event.sender.github_email,
            ),
            ("committer", *REPODYNAMICS_BOT_USER),
        ):
            git_api.set_user(
                name=name,
                email=email,
                typ=user_type,
                scope="process",
            )
            logger.info(
                title,
                f"{user_type.capitalize()} set to {name} <{email}>.",
            )
    return


@logger.sectioner("GitHub API Verification")
def _check_github_api(manager: Manager) -> None:
    in_repo_creation_event = (
        self.gh_context.event_name is _ghc_enum.EventType.PUSH
        and self.gh_context.ref_type is _ghc_enum.RefType.BRANCH
        and self.gh_context.event.action is _ghc_enum.ActionType.CREATED
        and self.gh_context.ref_is_main
    )
    log_title = "Admin Token Verification"
    if not admin_token:
        has_admin_token = False
        if in_repo_creation_event:
            logger.info(
                log_title,
                "Repository creation event detected; no admin token required.",
            )
        elif self.gh_context.event.repository.fork:
            logger.info(
                log_title,
                "Forked repository detected; no admin token required.",
            )
        else:
            logger.critical(
                log_title,
                "No admin token provided.",
            )
            reporter.update(
                "main",
                status="fail",
                summary="No admin token provided.",
            )
            raise ProManException()
    else:
        try:
            check = api_admin.info
        except _WebAPIError as e:
            details = e.report.body
            details.extend(*e.report.section["details"].content.body.elements())
            logger.critical(log_title, "Failed to verify the provided admin token.", details)
            reporter.update(
                "main",
                status="fail",
                summary="Failed to verify the provided admin token.",
                section=mdit.document(
                    heading="Admin Token Verification",
                    body=details.elements(),
                ),
            )
            raise ProManException()
        has_admin_token = True
        logger.success(
            log_title,
            "Admin token verified successfully.",
        )
    return api_admin, api_actions, link_gen, has_admin_token


@logger.sectioner("Output Generation")
def _finalize(manager: Manager, fail: bool | None = None) -> None:
    workflow_output = manager.output.generate(failed=fail)
    _write_step_outputs(workflow_output)

    report_gha = manager.reporter.generate(gha=True)
    _write_step_summary(report_gha)

    filename = (
        f"{manager.gh_context.repository_name}-workflow-run"
        f"-{manager.gh_context.run_id}-{manager.gh_context.run_attempt}.{{}}.{{}}"
    )
    dir_path = manager.git.repo_path / manager.data["local"]["report"]["path"] / "proman" / "gha"
    dir_path.mkdir(parents=True, exist_ok=True)

    output_str = ps.write.to_json_string(workflow_output, sort_keys=True, indent=3, default=str)
    file = dir_path / filename.format("output", "json")
    file.write_text(output_str)
    return


def _write_step_outputs(kwargs: dict) -> None:
    log_outputs = []
    for name, value in kwargs.items():
        output_name = name.lower().replace("_", "-")
        written_output = actionman.step_output.write(name=output_name, value=value)
        log_outputs.append(
            mdit.element.code_block(
                written_output,
                caption=f"{output_name} [{type(value).__name__}]",
            )
        )
    logger.debug("GHA Step Outputs", *log_outputs)
    return


def _write_step_summary(content: str) -> None:
    logger.debug("GHA Summary Output", mdit.element.code_block(content))
    actionman.step_summary.write(content)
    return
