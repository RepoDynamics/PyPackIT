from __future__ import annotations

import argparse
import json
from typing import TYPE_CHECKING

import actionman
import github_contexts
import mdit
import pyserials
import rich.text
from loggerman import logger

import proman
from proman import __version__
from proman.exception import ProManException

if TYPE_CHECKING:
    from collections.abc import Callable

    from proman.manager import Manager
    from proman.token_manager import TokenManager


def cli():
    proman.report.initialize_logger()
    kwargs, token_manager = _read_args()
    gh_context = kwargs.get("github_context")
    reporter = proman.report.Reporter(github_context=gh_context)
    manager = proman.manager.create(
        token_manager=token_manager,
        reporter=reporter,
        repo_path=kwargs["repo"],
        metadata_ref=kwargs.get("metadata_ref"),
        metadata_filepath=kwargs.get("metadata_filepath"),
        repo_path_main=kwargs.get("repo_upstream"),
        metadata_filepath_main=kwargs.get("main_metadata_filepath"),
        validate_metadata=kwargs.get("validate_metadata", True),
        github_context=gh_context,
    )
    current_branch = manager.git.current_branch_name()
    current_hash = manager.git.commit_hash_normal()
    endpoint = _get_endpoint(endpoint_name=kwargs.pop("endpoint"))
    current_log_section_level = logger.current_section_level
    try:
        endpoint(kwargs | {"manager": manager})
    except ProManException:
        pass
    except Exception as e:
        traceback = logger.traceback()
        error_name = e.__class__.__name__
        logger.critical(
            f"Unexpected Error: {error_name}",
            traceback,
        )
        reporter.update(
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
    try:
        logger.section_end(target_level=current_log_section_level)
    except Exception:
        pass
    _finalize(
        manager=manager,
        branch=current_branch,
        commit_hash=current_hash,
        endpoint=kwargs["command"],
    )
    return


def _read_args() -> tuple[dict, TokenManager]:
    """Read inputs and return them as a namespace object."""
    args = _parse_args()
    github_context = (
        json.loads(args.github_context)
        if "github_context" in args
        else actionman.env_var.read("GITHUB_CONTEXT", typ=dict, remove=args.remove_tokens)
    )
    if github_context:
        github_token = github_context.pop("token")
        args.github_context = github_contexts.github.create(github_context)
        if github_token:
            args.github_token = github_token
    kwargs = vars(args)
    token_manager = proman.token_manager.create(
        github=kwargs.pop("github_token", None),
        github_admin=kwargs.pop("github_admin_token", None),
        zenodo=kwargs.pop("zenodo_token", None),
        zenodo_sandbox=kwargs.pop("zenodo_sandbox_token", None),
        remove_from_env=args.remove_tokens,
    )
    logger.debug("Input Arguments", logger.pretty(kwargs | {"token_manager": token_manager}))
    return kwargs, token_manager


def _get_endpoint(endpoint_name: str) -> Callable[[dict], None]:
    def get_recursive(parts, current_object):
        if len(parts) == 1:
            return getattr(current_object, parts[0])
        return get_recursive(parts[1:], getattr(current_object, parts[0]))

    parts = endpoint_name.split(".")
    return get_recursive(parts, proman.script)


@logger.sectioner("Output Generation")
def _finalize(
    manager: Manager,
    branch: str,
    commit_hash: str,
    endpoint: str,
) -> None:
    dir_path = manager.git.repo_path / manager.data["local"]["report"]["path"] / "proman" / endpoint
    dir_path.mkdir(parents=True, exist_ok=True)
    if endpoint == "gha":
        workflow_output = manager.output.generate()
        _write_step_outputs(workflow_output)

        report_gha = manager.reporter.generate(gha=True)
        _write_step_summary(report_gha)

        filename = (
            f"{manager.gh_context.repository_name}-workflow-run"
            f"-{manager.gh_context.run_id}-{manager.gh_context.run_attempt}.{{}}.{{}}"
        )
        output_str = pyserials.write.to_json_string(
            workflow_output, sort_keys=True, indent=3, default=str
        )
        file = dir_path / filename.format("output", "json")
        file.write_text(output_str)

    report_html = manager.reporter.generate()

    log = logger.report
    target_config, sphinx_output = proman.report.make_sphinx_target_config()
    log.target_configs["sphinx"] = target_config
    log_html = log.render(target="sphinx")
    logger.info(
        "Log Generation Logs",
        mdit.element.rich(rich.text.Text.from_ansi(sphinx_output.getvalue())),
    )

    filename = (
        f"{proman.util.date.from_now_to_internal(time=True)}--{branch}--{commit_hash}--{{}}.html"
    )
    for file_type, content in {
        "report": report_html,
        "log": log_html,
    }.items():
        file = dir_path / filename.format(file_type)
        file.write_text(content)
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


def _parse_args() -> argparse.Namespace:
    """Generate the command line interface for the project manager and parse input arguments.

    Notes
    -----
    The code for this function is automatically generated by the control center.
    """
    # begin auto-generated parser
    parser = argparse.ArgumentParser(
        description=f"Project Manager CLI",
    )
    parser.add_argument(
        "--repo",
        help=f"Local path to the repository's root directory.",
        default=f"./",
    )
    parser.add_argument(
        "--repo-upstream",
        help=f"Local path to the upstream repository's root directory.",
    )
    parser.add_argument(
        "--metadata-ref",
        help=f"Git reference to read the metadata.json file from.",
    )
    parser.add_argument(
        "--metadata-filepath",
        help=f"Relative path to the metadata.json file.",
    )
    parser.add_argument(
        "--main-metadata-filepath",
        help=f"Relative path to the metadata.json file in the default branch.",
    )
    parser.add_argument(
        "--github-token",
        help=f"GitHub token for accessing the repository.",
    )
    parser.add_argument(
        "--remove-tokens",
        help=f"Remove all tokens read from the environment.",
        action=f"store_true",
    )
    parser.add_argument(
        "--no-validation",
        help=f"Skip validation of the metadata.json file.",
        dest=f"validate_metadata",
        action=f"store_false",
    )
    parser.add_argument(
        "--version",
        help=f"Output the version of the package and exit.",
        action=f"version",
        version=f"{__version__}",
    )
    # Sub-parsers for parser
    subparsers_main = parser.add_subparsers(
        dest=f"command",
        required=True,
    )
    subparser_cca = subparsers_main.add_parser(
        "cca",
        help=f"Run Continuous Configuration Automation on the repository.",
    )
    subparser_cca.add_argument(
        "-x",
        "--action",
        help=f"Action to perform.",
        choices=['report', 'apply', 'pull', 'merge', 'commit', 'amend'],
        default=f"apply",
    )
    subparser_cca.add_argument(
        "-b",
        "--branch-version",
        help=f"Branch-name to version mappings (e.g., -b main=0.0.0 dev=1.0.0a1) to use instead of git tags.",
        type=str,
        nargs=f"*",
        metavar=f"BRNACH=VERSION",
    )
    subparser_cca.add_argument(
        "-p",
        "--control-center",
        help=f"Path to the control center directory containing configuration files.",
        type=str,
    )
    subparser_cca.add_argument(
        "-c",
        "--clean-state",
        help=f"Ignore the metadata.json file and start from scratch.",
        action=f"store_true",
    )
    subparser_cca.set_defaults(endpoint="cca.run_cli")
    subparser_lint = subparsers_main.add_parser(
        "lint",
        help=f"Run pre-commit hooks on the repository.",
    )
    subparser_lint.add_argument(
        "-x",
        "--action",
        help=f"Action to perform.",
        type=str,
        choices=['report', 'apply', 'pull', 'merge', 'commit', 'amend'],
        default=f"apply",
    )
    subparser_lint.add_argument(
        "-r2",
        "--to-ref",
        help=f"Run on files changed until the given git ref. This must be accompanied by --from-ref.",
    )
    subparser_lint_mutually_exclusive_hook = subparser_lint.add_mutually_exclusive_group()
    subparser_lint_mutually_exclusive_hook.add_argument(
        "-i",
        "--hook-id",
        help=f"Specific hook ID to run. This will only run the specified hook.",
        type=str,
    )
    subparser_lint_mutually_exclusive_hook.add_argument(
        "-s",
        "--hook-stage",
        help=f"Specific hook stage to run. This will only run hooks in the specified stage.",
        type=str,
    )
    subparser_lint_mutually_exclusive_file = subparser_lint.add_mutually_exclusive_group()
    subparser_lint_mutually_exclusive_file.add_argument(
        "-a",
        "--all-files",
        help=f"Run on all files in the repository.",
        action=f"store_true",
    )
    subparser_lint_mutually_exclusive_file.add_argument(
        "-f",
        "--files",
        help=f"Run on specific files.",
        nargs=f"+",
    )
    subparser_lint_mutually_exclusive_file.add_argument(
        "-r1",
        "--from-ref",
        help=f"Run on files changed since the given git ref. This must be accompanied by --to-ref.",
    )
    subparser_lint.set_defaults(endpoint="lint.run_cli")
    subparser_version = subparsers_main.add_parser(
        "version",
        help=f"Print the current version of the project.",
    )
    subparser_version.set_defaults(endpoint="version.run_cli")
    subparser_build = subparsers_main.add_parser(
        "build",
        help=f"Build project components.",
    )
    # Sub-parsers for subparser_build
    subparsers_build = subparser_build.add_subparsers(
        dest=f"build",
        required=True,
    )
    subparser_conda = subparsers_build.add_parser(
        "conda",
        help=f"Build a conda package in the project.",
    )
    subparser_conda.add_argument(
        "-p",
        "--pkg",
        help=f"Package ID, i.e., the `pypkg_` key suffix in configuration files.",
        default=f"main",
    )
    subparser_conda.add_argument(
        "-o",
        "--output",
        help=f"Path to the local conda channel directory.",
        type=str,
        default=f".local/temp/conda-channel",
    )
    subparser_conda.add_argument(
        "-r",
        "--recipe",
        help=f"Type of recipe to build.",
        type=str,
        choices=['local', 'global'],
        default=f"local",
    )
    subparser_conda.add_argument(
        "--args",
        help=f"Additional arguments to pass to the conda build command.",
        nargs=argparse.REMAINDER,
    )
    subparser_conda.set_defaults(endpoint="build.conda.run_cli")
    subparser_python = subparsers_build.add_parser(
        "python",
        help=f"Build a Python package in the project.",
    )
    subparser_python.add_argument(
        "-p",
        "--pkg",
        help=f"Package ID, i.e., the `pypkg_` key suffix in configuration files.",
        default=f"main",
    )
    subparser_python.add_argument(
        "-o",
        "--output",
        help=f"Path to the local PyPI channel directory.",
        type=str,
        default=f".local/temp/wheelhouse",
    )
    subparser_python.add_argument(
        "--args",
        help=f"Additional arguments to pass to the Python build command.",
        nargs=argparse.REMAINDER,
    )
    subparser_python.set_defaults(endpoint="build.python.run_cli")
    subparser_render = subparsers_main.add_parser(
        "render",
        help=f"Render documents in the project.",
    )
    # Sub-parsers for subparser_render
    subparsers_render = subparser_render.add_subparsers(
        dest=f"render",
        required=True,
    )
    subparser_pypi = subparsers_render.add_parser(
        "pypi",
        help=f"Render package README file for PyPI.",
    )
    subparser_pypi.add_argument(
        "-p",
        "--pkg",
        help=f"Package ID, i.e., the `pypkg_` key suffix in configuration files.",
        default=f"main",
    )
    subparser_pypi.add_argument(
        "-o",
        "--output",
        help=f"Output directory to write the rendered HTML file.",
        type=str,
        default=f".local/temp/readme-pypi",
    )
    subparser_pypi.set_defaults(endpoint="render.pypi.run_cli")
    subparser_gha = subparsers_main.add_parser(
        "gha",
        help=f"Run CI/CD pipelines in GitHub Actions.",
    )
    subparser_gha.set_defaults(endpoint="gha.run_cli")
    # Process inputs
    args = parser.parse_args()
    if args.command == "cca":
        if args.branch_version:
            try:
                args.branch_version = dict(pair.split("=", 1) for pair in args.branch_version)
            except ValueError:
                parser.error(
                    "--branch-version must be in the format BRANCH=VERSION (e.g., -b main=1.0.0 dev=2.0.0)."
                )
    if args.command == "lint":
        if (args.from_ref and not args.to_ref) or (args.to_ref and not args.from_ref):
            parser.error("Both --from-ref and --to-ref must be provided together.")
    # end auto-generated parser
    return args


if __name__ == "__main__":
    cli()
