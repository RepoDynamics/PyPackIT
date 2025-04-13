# PyPackIT-TestSuite © 2023–2024 RepoDynamics
# SPDX-License-Identifier: AGPL-3.0-or-later

"""PyPackIT-TestSuite: Test Suite for PyPackIT."""

import tempfile
from pathlib import Path

import pkgdata
import pytest

__version_info__: dict[str, str] = {"version": "0.0.0"}
"""Details of the currently installed version of the package,
including version number, date, branch, and commit hash."""

__version__: str = __version_info__["version"]
"""Version number of the currently installed package."""


def run(
    pyargs: list[str] | None = None,
    args: list[str] | None = None,
    overrides: dict[str, str] | None = None,
    path_cache: str | Path | None = None,
    path_report: str | Path | None = None,
    template_start: str = "$|| ",
    template_end: str = " ||",
) -> int:
    """Run the test-suite.

    Parameters
    ----------
    pyargs
        Fully qualified names of test cases to run.
        These can be sub-packages, modules, classes, or individual test functions
        in the test-suite. If not provided, the entire test-suite will be run.
    args
        Additional command-line arguments to pass to pytest.
    overrides
        Configuration options to override in the default pytest configuration file.
        These should be specified as key-value pairs, corresponding to the configuration
        option name and the new value, respectively.
        They are passed to pytest as `--override-ini {KEY}={VALUE}` arguments.
    path_cache
        Path to the directory where cache files will be stored.
        If not provided, a temporary directory will be created
        and automatically cleaned up after the test-suite is run.
    path_report
        Path to the directory where test reports will be stored.
        If not provided, a temporary directory will be created
        and automatically cleaned up after the test-suite is run.
    template_start
        Start marker of the template string used in the configuration files
        to inject dynamic values.
    template_end
        End marker of the template string used in the configuration files
        to inject dynamic values.

    Returns
    -------
    Exit code of PyTest. This is 0 if the test suite ran successfully and all tests passed.
    Otherwise, it is a non-zero value indicating the type of failure.

    Notes
    -----
    For templating, the supported keys are:
    - `path_report`: Path to the directory where test reports will be stored.
    - `path_cache`: Path to the directory where cache files will be stored.
    - `path_config`: Path to the directory
       where PyTest and its plugins look for configuration files.
       Test-suite configuration files are stored internally as data files within the package.
       Each time the test suite is run, it uses its current path to update the
       `path_config` variable in the configuration files,
       so that PyTest and its plugins can find them regardless of
       the current working directory.
    For each value, the template string should be formatted as
    `{template_start}{key}{template_end}`,
    so for example if `template_start` is `"$|| "` and `template_end` is " ||",
    the template string for `path_report` would be `$|| path_report ||`.
    """
    path_root = pkgdata.get_package_path_from_caller(top_level=True).resolve()
    path_config = path_root / "data" / "config"
    path_pytest_config = None
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        path_config_temp = temp_dir_path / "config"
        path_cache = Path(path_cache) if path_cache else temp_dir_path / "cache"
        path_report = Path(path_report) if path_report else temp_dir_path / "report"
        for path in (path_config_temp, path_cache, path_report):
            path.mkdir(parents=True, exist_ok=True)
        for path in path_config.iterdir():
            if not path.is_file():
                continue
            (path_cache / path.stem).mkdir(exist_ok=True)
            (path_report / path.stem).mkdir(exist_ok=True)
            config = path.read_text()
            for template, value in (
                (f"{template_start}{template_name}{template_end}", template_value)
                for template_name, template_value in (
                    ("path_config", path_config_temp),
                    ("path_report", path_report),
                    ("path_cache", path_cache),
                )
            ):
                config = config.replace(template, value.as_posix())
            file_temp_path = path_config_temp / path.name
            file_temp_path.write_text(config)
            if path.stem == "pytest":
                path_pytest_config = file_temp_path
        final_args = [f"--rootdir={path_root}"]
        if path_pytest_config:
            final_args.append(f"--config-file={path_pytest_config}")
        if args:
            final_args.extend(args)
        if overrides:
            for override_key, override_value in overrides.items():
                # https://docs.pytest.org/en/stable/reference/reference.html#configuration-options
                final_args.extend(["--override-ini", f"{override_key}={override_value}"])
        pyargs = pyargs or [pkgdata.get_package_name_from_caller(top_level=True)]
        final_args.extend(["--pyargs", *pyargs])
        print(final_args)
        return pytest.main(final_args)
