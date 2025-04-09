"""Continuous Configuration Automation (CCA) script."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from loggerman import logger

from controlman.exception import ControlManException

if TYPE_CHECKING:
    from proman.manager import Manager


@logger.sectioner("Continuous Configuration Automation")
def run(
    *,
    branch_manager: Manager,
    main_manager: Manager,
    branch_version: dict[str, str] | None = None,
    control_center: str | None = None,
    dry_run: bool = False,
    clean_state: bool = False,
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
    with logger.sectioning("Initialization"):
        center_manager = branch_manager.control_center(
            data_main=main_manager.data,
            future_versions=branch_version,
            control_center_path=control_center,
            clean_state=clean_state,
        )
    with logger.sectioning("Execution"):
        reporter = center_manager.report()




    if not dry_run:
        center_manager.apply_changes()
    return reporter


def run_cli(kwargs: dict) -> None:
    """Run the CLI.

    Parameters
    ----------
    kwargs
        Input arguments for the CLI.
    """
    try:
        report = run(
            branch_manager=kwargs["manager"],
            main_manager=kwargs["main_manager"],
            branch_version=kwargs["branch_version"],
            control_center=kwargs["control_center"],
            dry_run=kwargs["dry_run"],
            clean_state=kwargs["clean_state"],
        ).report()
    except ControlManException as e:
        report = e.report
    report_str = report.render()
    report_path = Path(kwargs["repo"]) / ".local" / "report" / "cca" / "report.html"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_str)
    return
