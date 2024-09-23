"""Main command-line interface of the package."""

import argparse
import sys

from my_new_project import __version__


def main() -> int:
    """Run the main command-line interface of the package."""
    # AUTOCODE START: cli
    cli_description: str = "Command-line interface for the package."
    cli_greeting: str = "Welcome to the package's command-line interface!"
    cli_logo: str = ""
    # AUTOCODE END: cli

    parser = argparse.ArgumentParser(description=cli_description)
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the current version of the package.",
    )
    args = parser.parse_args()
    if not vars(args):
        if cli_logo:
            print(cli_logo)
        print(cli_greeting)
    return 0


if __name__ == "__main__":
    sys.exit(main())
