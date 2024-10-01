"""Run all tests for the package."""

import argparse
import json

import my_new_project_testsuite as testsuite


def main():
    # AUTOCODE START: cli
    cli_description: str = "Command-line interface for the test-suite."
    cli_logo: str = ""
    # AUTOCODE END: cli
    parser = argparse.ArgumentParser(description=cli_description)
    parser.add_argument('--pyargs', help='Pyargs argument')
    parser.add_argument('--args', help='Args argument')
    parser.add_argument('--overrides', help='Overrides argument')
    parser.add_argument('--cache', help='Cache argument')
    parser.add_argument('--report', help='Report argument')

    if cli_logo:
        print(cli_logo)

    args = parser.parse_args()

    parsed_args = {}
    for arg_name, arg_type in (
        ('pyargs', list),
        ('args', list),
        ('overrides', dict),
    ):
        input_arg = getattr(args, arg_name)
        if input_arg is None:
            continue
        try:
            parsed_arg = json.loads(input_arg)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse '{arg_name}' argument as JSON.") from e
        if not isinstance(parsed_arg, arg_type):
            raise ValueError(f"Expected '{arg_name}' argument to be of type '{arg_type}'.")
        parsed_args[arg_name] = parsed_arg

    testsuite.run(
        **parsed_args,
        path_cache=args.cache,
        path_report=args.report,
    )


if __name__ == '__main__':
    main()
