"""Command-line interface of the package."""

import argparse
import sys

from new_pyproject import __version__


def main() -> int:
    """Run the command-line interface."""
    args = _parse_args()
    return 0


def _parse_args() -> argparse.Namespace:
    """Generate the command line interface parser and parse input arguments.

    Notes
    -----
    The code for this function is automatically generated by the control center.
    """
    # begin auto-generated parser

    # end auto-generated parser
    return args


if __name__ == "__main__":
    sys.exit(main())
