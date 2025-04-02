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


def run_cli(parser: argparse.ArgumentParser, args: argparse.Namespace) -> int:
    """Run the CLI for Continuous Configuration Automation.
    
    Parameters
    ----------
    parser : argparse.ArgumentParser
        The argument parser to use for parsing command line arguments.
    args : argparse.Namespace, optional
        The parsed arguments. If None, the arguments are parsed from sys.argv.
    Returns
    -------
    int
        The exit code of the program.
    """
    if args.branch_version:
        try:
            args.branch_version = dict(pair.split("=", 1) for pair in args.branch_version)
        except ValueError:
            parser.error(
                "--branch-version must be in the format BRANCH=VERSION (e.g., -b main=1.0.0 dev=2.0.0)."
            )
    try:
        report = run(**vars(args)).report()
        exit_code = 0
    except ControlManException as e:
        report = e.report
        exit_code = 1
    report_str = report.render()
    return sys.exit(exit_code)


def cli_parser(subparsers: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:
    description = "Run Continuous Configuration Automation on the repository."
    if subparsers:
        parser = subparsers.add_parser("cca", help=description)
    else:
        parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-r", "--repo", type=str, help="Path to the repository.")
    parser.add_argument(
        "-t", "--token", type=str, help="GitHub token for accessing the repository."
    )
    parser.add_argument(
        "-b",
        "--branch-version",
        type=str,
        nargs="*",
        metavar="BRANCH=VERSION",
        help="Branch-to-version mappings (e.g., -b main=1.0.0 dev=2.0.0).",
    )
    parser.add_argument(
        "-c",
        "--control-center",
        type=str,
        help="Path to the control center directory containing configuration files.",
    )
    parser.add_argument(
        "-d", "--dry-run", action="store_true", help="If set, changes are not applied."
    )
    parser.add_argument(
        "-n",
        "--no-validate",
        action="store_false",
        dest="validate",
        help="Disable validation of the metadata.json file against the schema.",
    )
    return parser


if __name__ == "__main__":
    logger.initialize(realtime_levels=list(range(7)))
    parser = cli_parser()
    run_cli(parser, parser.parse_args())
