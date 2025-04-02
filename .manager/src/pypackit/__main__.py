import argparse

from loggerman import logger

from pypackit import script


def cli():
    def get_endpoint(endpoint_name: str):
        def get_recursive(parts, current_object):
            if len(parts) == 1:
                return getattr(current_object, parts[0])
            else:
                return get_recursive(parts[1:], getattr(current_object, parts[0]))
        parts = endpoint_name.split(".")
        return get_recursive(parts, script)

    logger.initialize(realtime_levels=list(range(7)))
    # begin auto-generated parser
    parser = argparse.ArgumentParser(description="Project Manager CLI")
    parser.add_argument("--repo", type=str, help="Local path to the repository root directory.")
    # Sub-parsers for parser
    subparsers_main = parser.add_subparsers(dest="command", required=True)
    subparser_cca = subparsers_main.add_parser("cca", help="Run Continuous Configuration Automation on the repository.")
    subparser_cca.add_argument("-t", "--token", type=str, help="GitHub token for accessing the repository.")
    subparser_cca.add_argument("-b", "--branch-version", help="Branch-name to version mappings (e.g., -b main=0.0.0 dev=1.0.0a1) to use instead of git tags.", type=str, nargs="*", metavar="BRNACH=VERSION")
    subparser_cca.add_argument("-c", "--control-center", help="Path to the control center directory containing configuration files.", type=str)
    subparser_cca.add_argument("-d", "--dry-run", help="Perform a dry run without making any changes.", action="store_true")
    subparser_cca.add_argument("-n", "--no-validate", help="Skip validation of the metadata.json file.", dest="validate", action="store_false")
    subparser_cca.set_defaults(endpoint="cca.run_cli")
    subparser_lint = subparsers_main.add_parser("lint", help="Run pre-commit hooks on the repository.")
    subparser_lint.add_argument("-x", "--action", help="Lint mode.", type=str, choices=['report', 'run', 'validate'], default="run")
    subparser_lint.add_argument("-c", "--config", help="Path to the pre-commit configuration file.", type=str, default=".devcontainer/config/pre-commit.yaml")
    subparser_lint.add_argument("-r2", "--to-ref", help="Run on files changed until the given git ref. This must be accompanied by --from-ref.")
    subparser_lint_mutually_exclusive_hook = subparser_lint.add_mutually_exclusive_group()
    subparser_lint_mutually_exclusive_hook.add_argument("-i", "--hook-id", help="Specific hook ID to run. This will only run the specified hook.", type=str)
    subparser_lint_mutually_exclusive_hook.add_argument("-s", "--hook-stage", help="Specific hook stage to run. This will only run hooks in the specified stage.", type=str)
    subparser_lint_mutually_exclusive_file = subparser_lint.add_mutually_exclusive_group()
    subparser_lint_mutually_exclusive_file.add_argument("-a", "--all-files", help="Run on all files in the repository.", action="store_true")
    subparser_lint_mutually_exclusive_file.add_argument("-f", "--files", help="Run on specific files.", nargs="+")
    subparser_lint_mutually_exclusive_file.add_argument("-r1", "--from-ref", help="Run on files changed since the given git ref. This must be accompanied by --to-ref.")
    subparser_lint.set_defaults(endpoint="lint.run_cli")
    subparser_version = subparsers_main.add_parser("version", help="Print the current version of the project.")
    subparser_build = subparsers_main.add_parser("build", help="Build project components.")
    # Sub-parsers for subparser_build
    subparsers_build = subparser_build.add_subparsers(dest="build", required=True)
    subparser_conda = subparsers_build.add_parser("conda", help="Build a conda package in the project.")
    subparser_conda.add_argument("args", help="Additional arguments to pass to the conda build command.", nargs="*")
    subparser_conda.add_argument("-p", "--pkg", help="Package ID, i.e., the `pypkg_` key suffix in configuration files.", default="main")
    subparser_conda.add_argument("-o", "--output", help="Path to the local conda channel directory.", type=str, default=".local/temp/conda-channel")
    subparser_conda.add_argument("-r", "--recipe", help="Type of recipe to build.", type=str, choices=['local', 'global'], default="local")
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
    logger.debug("Input Arguments", args)
    endpoint = get_endpoint(args.endpoint)
    endpoint(args)
    return
