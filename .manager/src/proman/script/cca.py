from __future__ import annotations

import argparse
import sys
from pathlib import Path

from loggerman import logger

import controlman
from controlman.exception import ControlManException


def run(
    *,
    repo: str | None = None,
    token: str | None = None,
    branch_version: dict[str, str] | None = None,
    control_center: str | None = None,
    dry_run: bool = False,
    validate: bool = True,
):
    """Run Continuous Configuration Automation on the repository.

    Parameters
    ----------
    repo : str
        Path to the repository.
    token : str, optional
        GitHub token for accessing the repository.
    branch_version : dict[str, str], optional
        Mapping of branch names to version numbers to override the version from git tags.
    control_center : str, optional
        Path to the control center directory containing configuration files.
        If given, the metadata.json file is ignored,
        thus everything is synchronized without access to a prior state.
    dry_run : bool, optional
        If True, changes are not applied.
    validate : bool, optional
        Validate the metadata.json file against the schema.
    """
    logger.section("CCA")
    with logger.sectioning("Initialization"):
        center_manager = controlman.manager(
            repo=repo or Path.cwd(),
            future_versions=branch_version,
            control_center_path=control_center,
            validate=validate,
            github_token=token,
        )
    with logger.sectioning("Execution"):
        reporter = center_manager.report()
    if not dry_run:
        center_manager.apply_changes()
    return reporter


def run_cli(args: argparse.Namespace) -> int:
    """Run the CLI for Continuous Configuration Automation.

    Parameters
    ----------
    args : argparse.Namespace, optional
        The parsed arguments. If None, the arguments are parsed from sys.argv.
    Returns
    -------
    int
        The exit code of the program.
    """
    try:
        report = run(
            repo=args.repo,
            token=args.token,
            branch_version=args.branch_version,
            control_center=args.control_center,
            dry_run=args.dry_run,
            validate=args.validate,
        ).report()
        exit_code = 0
    except ControlManException as e:
        report = e.report
        exit_code = 1
    report_str = report.render()
    return sys.exit(exit_code)
