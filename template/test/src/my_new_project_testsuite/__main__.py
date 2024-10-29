"""Run all tests for the package."""

from __future__ import annotations

import argparse
import json
import sys

import my_new_project_testsuite as testsuite


class TestSuiteCLIInputError(Exception):
    """Raised when there is an error in CLI user inputs."""


class TestSuiteCLIInputDecodeError(TestSuiteCLIInputError):
    """Raised when there is an error decoding JSON user inputs."""

    def __init__(self, arg_name: str, arg_value: str, cause: json.JSONDecodeError):
        self.arg_name = arg_name
        self.arg_value = arg_value
        self.cause = cause
        super().__init__(
            f"Failed to parse input argument '{arg_name}' as JSON: {cause}\n"
            f"Input value: '{arg_value}'"
        )
        return


class TestSuiteCLIInputTypeError(TestSuiteCLIInputError):
    """Raised when there is a type mismatch in CLI user inputs."""

    def __init__(
        self,
        arg_name: str,
        arg_value: str | bool | float | list | dict,
        arg_type: type,
    ):
        self.arg_name = arg_name
        self.arg_value = arg_value
        self.arg_type = arg_type
        super().__init__(
            f"Expected input argument '{arg_name}' to be of type '{arg_type.__name__}', "
            f"but got '{type(arg_value).__name__}'.\n"
            f"Input value: '{arg_value}'"
        )
        return


def main():
    """Run the command-line interface of the test suite."""
    # AUTOCODE START: cli
    cli_description: str = "Command-line interface for the test-suite."
    cli_logo: str = ""
    # AUTOCODE END: cli
    parser = argparse.ArgumentParser(description=cli_description)
    parser.add_argument("--pyargs", help="Pyargs argument")
    parser.add_argument("--args", help="Args argument")
    parser.add_argument("--overrides", help="Overrides argument")
    parser.add_argument("--cache", help="Cache argument")
    parser.add_argument("--report", help="Report argument")

    if cli_logo:
        print(cli_logo)

    args = parser.parse_args()

    parsed_args = {}
    for arg_name, arg_type in (
        ("pyargs", list),
        ("args", list),
        ("overrides", dict),
    ):
        input_arg = getattr(args, arg_name)
        if input_arg is None:
            continue
        try:
            parsed_arg = json.loads(input_arg)
        except json.JSONDecodeError as e:
            raise TestSuiteCLIInputDecodeError(
                arg_name=arg_name, arg_value=input_arg, cause=e
            ) from e
        if not isinstance(parsed_arg, arg_type):
            raise TestSuiteCLIInputTypeError(
                arg_name=arg_name, arg_value=parsed_arg, arg_type=arg_type
            )
        parsed_args[arg_name] = parsed_arg

    return testsuite.run(
        **parsed_args,
        path_cache=args.cache,
        path_report=args.report,
    )


if __name__ == "__main__":
    sys.exit(main())
