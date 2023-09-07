# Standard libraries
import re
from typing import Any

# Non-standard libraries
import versioningit
from setuptools import setup


def versioningit_format_custom(
    *,
    description: versioningit.VCSDescription,
    base_version: str,
    next_version: str,
    params: dict[str, Any],
) -> str:
    branch: str | None = description.branch
    if not branch:
        issue_nr = "999999999"
    elif branch == params["default-branch"]:
        issue_nr = "0"
    else:
        match = re.match(r"^dev/(\d+)$", branch)
        issue_nr = match.group(1) if match else "999999999"

    fields = {
        **description.fields,
        "issue_nr": issue_nr,
        "base_version": base_version,
        "next_version": next_version,
    }
    formats = {
        "distance": "{base_version}.{issue_nr}.dev{distance}",
        "dirty": "{base_version}.{issue_nr}.dev{distance}.{author_date:%Y.%m.%d}.{rev}.dirty",
        "distance-dirty": "{base_version}.{issue_nr}.dev{distance}.{author_date:%Y.%m.%d}.{rev}.dirty",
    }
    if description.state not in formats:
        raise versioningit.ConfigError(f"No format string found for state {description.state!r}.")
    fmt = formats[description.state]
    return fmt.format_map(fields)


if __name__ == "__main__":
    setup(cmdclass=versioningit.get_cmdclasses())
