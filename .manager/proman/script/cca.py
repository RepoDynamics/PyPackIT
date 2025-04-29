"""Continuous Configuration Automation (CCA) script."""

from __future__ import annotations

from typing import TYPE_CHECKING

import htmp
from loggerman import logger

import proman
from proman.exception import PromanError

if TYPE_CHECKING:
    from typing import Literal

    from proman.manager import Manager


@logger.sectioner("Continuous Configuration Automation")
def run(
    *,
    manager: Manager,
    action: Literal["report", "apply", "pull", "merge", "commit", "amend"] = "apply",
    control_center: str | None = None,
    clean_state: bool = False,
    branch_version: dict[str, str] | None = None,
):
    """Run Continuous Configuration Automation on the repository.

    Parameters
    ----------
    branch_version : dict[str, str], optional
        Mapping of branch names to version numbers to override the version from git tags.
    control_center : str, optional
        Path to the control center directory containing configuration files.
        If given, the metadata.json file is ignored,
        thus everything is synchronized without access to a prior state.
    dry_run : bool, optional
        If True, changes are not applied.
    clean_state
        Ignore the metadata.json file and start from a clean state.
    """
    try:
        with logger.sectioning("Initialization"):
            center_manager = manager.control_center(
                future_versions=branch_version,
                control_center_path=control_center,
                clean_state=clean_state,
            )
        with logger.sectioning("Execution"):
            reporter = center_manager.report()
    except PromanError as e:
        manager.reporter.update(
            "cca",
            status="fail",
            summary=e.report.body["intro"].content,
            body=e.report.body,
            section=e.report.section,
            section_is_container=True,
        )
        raise PromanError()

    new_manager = proman.manager.update(
        manager=manager, project_metadata=center_manager.generate_data()
    )
    report = reporter.report()
    summary = report.body["summary"].content
    new_manager.reporter.update(
        "cca",
        status="fail" if reporter.has_changes and action in ["report", "pull"] else "pass",
        summary=summary,
        section=report.section,
        section_is_container=True,
    )

    commit_hash = None
    if reporter.has_changes and action != "report":
        # Apply and optionally push/pull changes
        summary += " These were synced and changes were applied to"
        with logger.sectioning("Synchronization"):
            pr_branch = None
            if action in ["pull", "merge"]:
                # Create new branch for PR
                pr_branch = new_manager.branch.new_auto(auto_type="config_sync")
                new_manager.branch.checkout_to_auto(branch=pr_branch)
            # Apply changes to the branch
            center_manager.apply_changes()
            proman.script.lint.run(
                manager=new_manager,
                action="apply",
                hook_stage="manual",
                files=[file.path for file in reporter.modified_files],
                process_id="cca",
            )
            if action == "apply":
                summary += " the current branch without committing."
            elif action in ["pull", "merge", "commit", "amend"]:
                # Commit changes
                commit_msg = (
                    new_manager.commit.create_auto(id="config_sync")
                    if action in ["pull", "merge", "commit"]
                    else ""
                )
                commit_hash = new_manager.git.commit(
                    message=str(commit_msg) if action != "amend" else "",
                    stage="all",
                    amend=action == "amend",
                )
            if action in ["commit", "amend"]:
                # Add commit summary
                link = f"[`{commit_hash[:7]}`]({new_manager.gh_link.commit(commit_hash)})"
                summary += " the current branch " + (
                    f"in commit {link}."
                    if action == "commit"
                    else f"by amending the latest commit (new hash: {link})."
                )
            elif pr_branch:
                # Create PR
                commit_hash = None
                new_manager.git.push(target="origin", set_upstream=True)
                new_manager.branch.checkout_from_auto()
                pull_data = new_manager.gh_api_admin.pull_create(
                    head=pr_branch.name,
                    base=pr_branch.target.name,
                    title=commit_msg.description,
                    body=report.source(
                        target="github", filters=["short, github"], separate_sections=False
                    ),
                )
                link = f"[#{pull_data['number']}]({pull_data['url']})"
                summary += f" branch {htmp.element.code(pr_branch.name)} in PR {link}."
                if action == "merge":
                    # TODO: Merge the PR
                    pass
    return new_manager, reporter, commit_hash


def run_cli(kwargs: dict) -> None:
    """Run from CLI."""
    run(
        manager=kwargs["manager"],
        branch_version=kwargs["branch_version"],
        control_center=kwargs["control_center"],
        action=kwargs["action"],
        clean_state=kwargs["clean_state"],
    )
    return
