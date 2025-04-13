"""Generate and/or install package dependencies."""

from __future__ import annotations as _annotations

import argparse as _argparse
import copy as _copy
import functools as _functools
import json as _json
import logging as _logging
import platform as _platform
import struct as _struct
import subprocess as _subprocess
import sys as _sys
import tempfile as _tempfile
import xml.dom.minidom as _xml_minidom
import xml.etree.ElementTree as _ET  # noqa: N814, ICN001
from pathlib import Path as _Path
from typing import TYPE_CHECKING as _TYPE_CHECKING

if _TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Literal

    PlatformName = Literal[
        "emscripten-wasm32",
        "linux-32",
        "linux-64",
        "linux-aarch64",
        "linux-armv6l",
        "linux-armv7l",
        "linux-ppc64",
        "linux-ppc64le",
        "linux-riscv32",
        "linux-riscv64",
        "linux-s390x",
        "osx-64",
        "osx-arm64",
        "wasi-wasm32",
        "win-32",
        "win-64",
        "win-arm64",
        "zos-z",
    ]
    SourceName = Literal["conda", "pip", "apt", "brew", "choco", "winget", "bash", "pwsh"]


_CONDA_SUBDIR_TO_OS_ARCH = {
    "emscripten-wasm32": {"unix", "emscripten", "wasm32"},
    "wasi-wasm32": {"wasi", "wasm32"},
    "freebsd-64": {"freebsd", "x86", "x86_64"},
    "linux-32": {"unix", "linux", "linux32", "x86"},
    "linux-64": {"unix", "linux", "linux64", "x86", "x86_64"},
    "linux-aarch64": {"unix", "linux", "aarch64"},
    "linux-armv6l": {"unix", "linux", "arm", "armv6l"},
    "linux-armv7l": {"unix", "linux", "arm", "armv7l"},
    "linux-ppc64": {"unix", "linux", "ppc64"},
    "linux-ppc64le": {"unix", "linux", "ppc64le"},
    "linux-riscv64": {"unix", "linux", "riscv64"},
    "linux-s390x": {"unix", "linux", "s390x"},
    "osx-64": {"unix", "osx", "x86", "x86_64"},
    "osx-arm64": {"unix", "osx", "arm64"},
    "win-32": {"win", "win32", "x86"},
    "win-64": {"win", "win64", "x86", "x86_64"},
    "win-arm64": {"win", "arm64"},
    "zos-z": {"zos", "z"},
}
"""Mapping of Conda subdirectory (i.e. build platform) names
to corresponding OS architecture keys expected to be True.

References
----------
- [Conda-build source code](https://github.com/conda/conda-build/blob/e5b060efd18665b2810ecabac48a89e322943266/tests/test_metadata.py#L480-L503)
"""


_CONDA_SELECTOR_VARS = set.union(*_CONDA_SUBDIR_TO_OS_ARCH.values())
"""Set of all available Conda selector variables
other than `py`, `np`, and `build_platform` variables.

References
----------
- https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html#preprocessing-selectors
- [Conda-build source code](https://github.com/conda/conda-build/blob/e5b060efd18665b2810ecabac48a89e322943266/tests/test_metadata.py#L446-L477)
"""


def run(  # noqa: PLR0913
    packages: Sequence[str | dict],
    *,
    python_version: str | None = None,
    build_platform: PlatformName | None = None,
    target_platform: PlatformName | None = None,
    sources: Sequence[SourceName] | None = None,
    exclude_sources: Sequence[SourceName] | None = None,
    exclude_installed: bool = True,
    pip_in_conda: bool = True,
    conda_env_name: str | None = None,
    install: Sequence[SourceName] | bool = True,
    exclude_install: Sequence[SourceName] | None = None,
    output_dir: str | _Path | None = None,
    overwrite: bool = False,
    filename_conda: str = "environment.yml",
    filename_pip: str = "requirements.txt",
    filename_apt: str = "apt.txt",
    filename_brew: str = "Brewfile",
    filename_choco: str = "packages.config",
    filename_winget: str = "packages.json",
    filename_bash: str = "install.sh",
    filename_pwsh: str = "install.ps1",
    indent_json: int | None = 4,
    indent_xml: int | None = 4,
    indent_yaml: int | None = 2,
    filepath: str | _Path = ".github/.repodynamics/metadata.json",
) -> tuple[dict[SourceName, list[dict]], dict[SourceName, str], dict[SourceName, str]]:
    """Generate and/or install package dependencies based on the given configurations."""
    filepath = _Path(filepath).resolve()
    if not filepath.is_file():
        error_msg = f"Metadata file not found at '{filepath}'"
        raise FileNotFoundError(error_msg)
    try:
        data = _json.loads(filepath.read_text())
    except _json.JSONDecodeError as e:
        error_msg = f"Failed to load dependencies from '{filepath}'"
        raise ValueError(error_msg) from e
    _logger.debug("Loaded metadata from '%s'", filepath)
    dependencies, files = DependencyInstaller(data).run(
        packages=packages,
        python_version=python_version,
        build_platform=build_platform,
        target_platform=target_platform,
        sources=sources,
        exclude_sources=exclude_sources,
        exclude_installed=exclude_installed,
        pip_in_conda=pip_in_conda,
        conda_env_name=conda_env_name,
        indent_json=indent_json,
        indent_xml=indent_xml,
        indent_yaml=indent_yaml,
    )
    if install:
        all_sources = ["conda", "pip", "apt", "brew", "choco", "winget", "bash", "pwsh"]
        if isinstance(install, bool):
            install_sources = set(all_sources)
        else:
            for source in install:
                if source not in all_sources:
                    error_msg = f"Source {source} is not recognized."
                    raise ValueError(error_msg)
            install_sources = set(install)
        if exclude_install:
            install_sources = install_sources - set(exclude_install)
        install_files({k: v for k, v in files.items() if k in install_sources})
    paths = {}
    if output_dir:
        paths = write_files(
            files=files,
            output_dir=output_dir,
            overwrite=overwrite,
            filename_conda=filename_conda,
            filename_pip=filename_pip,
            filename_apt=filename_apt,
            filename_brew=filename_brew,
            filename_choco=filename_choco,
            filename_winget=filename_winget,
            filename_bash=filename_bash,
            filename_pwsh=filename_pwsh,
        )
    return dependencies, files, paths


def install_files(
    files: dict[SourceName, str],
    cmd_bash: Sequence[str] = ("bash", "{filepath}"),
    cmd_pwsh: Sequence[str] = ("pwsh", "-ExecutionPolicy", "Bypass", "-File", "{filepath}"),
    cmd_apt: Sequence[str] = ("apt-get", "-y", "install", "--no-install-recommends"),
    cmd_brew: Sequence[str] = ("brew", "bundle", "--file", "{filepath}"),
    cmd_choco: Sequence[str] = ("choco", "install", "{filepath}", "-y"),
    cmd_winget: Sequence[str] = (
        "winget",
        "import",
        "--accept-source-agreements",
        "--accept-package-agreements",
        "-i",
        "{filepath}",
    ),
    cmd_conda: Sequence[str] = (
        "conda",
        "env",
        "update",
        "--file",
        "{filepath}",
    ),  # https://stackoverflow.com/questions/42352841/how-to-update-an-existing-conda-environment-with-a-yml-file
    cmd_pip: Sequence[str] = ("pip", "install", "-r", "{filepath}"),
):
    """Install dependencies from the given files."""
    inputs = locals()

    filename = {
        "conda": "environment.yml",
        "pip": "requirements.txt",
        "apt": "apt.txt",
        "brew": "Brewfile",
        "choco": "packages.config",
        "winget": "packages.json",
        "bash": "install.sh",
        "pwsh": "install.ps1",
    }
    with _tempfile.TemporaryDirectory() as temp_dir:
        for source in ("bash", "pwsh", "apt", "brew", "choco", "winget", "conda", "pip"):
            if source not in files:
                continue
            _logger.info("Installing dependencies from %s", source)
            if source == "apt":
                _subprocess.run(list(cmd_apt) + files[source].splitlines(), check=True)  # noqa: S603
            else:
                filepath = _Path(temp_dir) / filename[source]
                filepath.write_text(files[source])
                cmd_filled = [
                    cmd_part.format(filepath=str(filepath)) for cmd_part in inputs[f"cmd_{source}"]
                ]
                _subprocess.run(cmd_filled, check=True)  # noqa: S603
    return


def write_files(  # noqa: PLR0913
    files: dict[SourceName, str],
    output_dir: str | _Path,
    *,
    overwrite: bool = False,
    filename_conda: str = "environment.yml",
    filename_pip: str = "requirements.txt",
    filename_apt: str = "apt.txt",
    filename_brew: str = "Brewfile",
    filename_choco: str = "packages.config",
    filename_winget: str = "packages.json",
    filename_bash: str = "install.sh",
    filename_pwsh: str = "install.ps1",
) -> dict[SourceName, str]:
    """Create environment files for dependencies."""

    def _write_file(filename: str, dep_content: str):
        filepath = output_dir / filename
        out[source] = filepath
        filepath.parent.mkdir(parents=True, exist_ok=True)
        if not filepath.exists() or overwrite:
            _logger.info("Writing %s file to %s", source, filepath)
            filepath.write_text(dep_content)
        else:
            error_msg = f"File already exists: '{filepath}'"
            raise FileExistsError(error_msg)
        return

    inputs = locals()
    output_dir = _Path(output_dir).resolve()
    out = {}
    for source, content in files.items():
        _write_file(inputs[f"filename_{source}"], dep_content=content)
    return out


class DependencyInstaller:
    """Resolve and install dependencies based on given configurations."""

    def __init__(self, package_data: dict):
        self._data = package_data
        return

    def run(  # noqa: PLR0913
        self,
        packages: Sequence[str | dict],
        *,
        build_platform: PlatformName | None = None,
        target_platform: PlatformName | None = None,
        python_version: str | None = None,
        sources: Sequence[SourceName] | None = None,
        exclude_sources: Sequence[SourceName] | None = None,
        exclude_installed: bool = True,
        extra_pip_specs: Sequence[str] | None = None,
        pip_in_conda: bool = True,
        conda_env_name: str | None = None,
        indent_json: int | None = 4,
        indent_xml: int | None = 4,
        indent_yaml: int | None = 2,
    ) -> tuple[dict[SourceName, list[dict]], dict[SourceName, str]]:
        """Install dependencies for the given configuration."""
        resolved_packages = self._resolve_packages(packages)
        resolved_python_version = _resolve_python_version(
            [pkg["pkg"] for pkg in resolved_packages], python_version
        )
        dependencies = {}
        for pkg in resolved_packages:
            deps = _resolve_dependencies(
                pkg=pkg["pkg"],
                python_version=resolved_python_version,
                extras=pkg["extras"],
                build_platform=build_platform,
                target_platform=target_platform,
                variants=pkg["variants"],
                sources=sources,
                exclude_sources=exclude_sources,
                exclude_installed=exclude_installed,
            )
            for source, dep_data in deps.items():
                dependencies.setdefault(source, []).extend(dep_data)

        dependencies.setdefault("conda", []).append(
            {"install": {"conda": {"spec": f"conda-forge::python {resolved_python_version}"}}}
        )
        if extra_pip_specs:
            dependencies.setdefault("pip", []).extend(
                [{"install": {"pip": {"spec": spec}}} for spec in extra_pip_specs]
            )
        files = {}
        for source, dep_data in dependencies.items():
            deps = [dep["install"][source] for dep in dep_data]
            if source == "conda":
                files[source] = _create_env_file_conda(
                    deps,
                    pip_packages=[dep["install"]["pip"] for dep in dependencies.get("pip", [])]
                    if pip_in_conda
                    else None,
                    env_name=conda_env_name,
                    indent=indent_yaml,
                )
            elif source == "pip":
                if not pip_in_conda:
                    files[source] = _create_env_file_pip(deps)
            elif source == "apt":
                files[source] = _create_env_file_apt(deps)
            elif source == "brew":
                files[source] = _create_env_file_brew(deps)
            elif source == "choco":
                files[source] = _create_env_file_choco(deps, indent=indent_xml)
            elif source == "winget":
                files[source] = _create_env_file_winget(deps, indent=indent_json)
            else:
                # bash and pwsh
                files[source] = "\n\n".join(
                    ["set -e"]
                    + [f"# ----- {dep['name']} -----\n{dep['install'][source]}" for dep in dep_data]
                )
        return dependencies, files

    def _resolve_packages(self, packages: Sequence[str | dict]) -> list[dict]:
        """Resolve dependencies for the given packages."""
        resolved_packages = []
        for pkg_spec in packages:
            extras = "all"
            variants = None
            if isinstance(pkg_spec, str):
                lib = pkg_spec
            else:
                lib = pkg_spec["id"]
                extras = pkg_spec.get("extras", extras)
                variants = pkg_spec.get("variants", variants)
            key = f"pypkg_{lib}"
            resolved_packages.append(
                {"pkg": self._data[key], "extras": extras, "variants": variants}
            )
        return resolved_packages


def _resolve_python_version(packages: list[dict], python_version: str | None = None) -> str:
    """Get the Python version from the given packages."""
    python_versions = [set(pkg["python"]["version"]["minors"]) for pkg in packages]
    common_python_versions = list(_functools.reduce(set.intersection, python_versions))
    if not python_version:
        python_version = ".".join(map(str, _sys.version_info[:2]))
    if python_version not in ("latest", "earliest"):
        if python_version not in common_python_versions:
            error_msg = f"Python version '{python_version}' is not supported."
            raise ValueError(error_msg)
        return python_version
    python_versions = sorted(common_python_versions, key=lambda x: tuple(map(int, x.split("."))))
    return python_versions[-1] if python_version == "latest" else python_versions[0]


def _resolve_dependencies(  # noqa: PLR0912
    pkg: dict,
    *,
    python_version: str,
    extras: Sequence[str] | Literal["all"] | None = "all",
    build_platform: PlatformName | None = None,
    target_platform: PlatformName | None = None,
    variants: dict[str, str | int | bool] | None = None,
    sources: Sequence[SourceName] | None = None,
    exclude_sources: Sequence[SourceName] | None = None,
    exclude_installed: bool = True,
) -> dict[SourceName, list[dict]]:
    """Resolve dependencies for a given platform and set of variants.

    Parameters
    ----------
    pkg
        Package to get dependencies for.
    python_version
        Python version to resolve dependencies for.
    extras
        Optional runtime dependency groups to get in addition to core dependencies.
    build_platform
        Name of the build platform.
        This corresponds to the conda-build subdirectory name.
        If not provided, the current native platform is used.
    target_platform
        Name of the target platform.
        If not provided, the build platform is used.
    variants
        Dictionary of variant keys and values to resolve.
    sources
        List of sources to resolve dependencies from.
        Sources are given in order of precedence.
        If not provided, the default set of sources are
        used for the given platform.
    exclude_sources
        List of sources to exclude from the resolution.
        That is, dependencies installable from these sources
        are not considered.
    exclude_installed
        Whether to exclude dependencies that are already installed.
        This is determined by running the validator script
        provided in the dependency data.
    """
    if not build_platform:
        build_platform = _get_native_platform()
    if not target_platform:
        target_platform = build_platform
    selector_vars = (
        {
            "build_platform": build_platform,
            "target_platform": target_platform,
            "py": python_version,
            "py3k": python_version[0] == "3",
            "py2k": python_version[0] == "2",
        }
        | {key: key in _CONDA_SUBDIR_TO_OS_ARCH[target_platform] for key in _CONDA_SELECTOR_VARS}
        | _resolve_variants(pkg=pkg, pyver=python_version, input_variants=variants)
    )
    if not sources:
        sources = ["pip", "conda"]
        if target_platform.startswith("linux"):
            sources.extend(["apt", "bash", "brew"])
        elif target_platform.startswith("osx"):
            sources.extend(["brew", "bash"])
        elif target_platform.startswith("win"):
            sources.extend(["choco", "winget", "pwsh"])
    exclude_sources = set(exclude_sources or [])
    out = {}
    dependencies = _collect_dependencies(pkg, extras=extras)
    for dependency in dependencies:
        if exclude_sources and set(dependency.get("install", {}).keys()) & exclude_sources:
            continue
        selector = dependency.get("selector")
        if selector and not _evaluate_selector(selector, selector_vars):
            continue
        if exclude_installed and dependency.get("validator"):
            validator_result = _subprocess.run(  # noqa: S603
                ["python", "-c", dependency["validator"]],  # noqa: S607
                capture_output=True,
                check=False,
            )
            if validator_result.returncode == 0:
                continue
        for source in sources:
            if source in dependency["install"]:
                out.setdefault(source, []).append(dependency)
                break
        else:
            error_msg = (
                f"Dependency '{dependency['name']}' not installable from any source. "
                f"Available sources are: {list(dependency['install'].keys())}"
            )
            raise ValueError(error_msg)
    return out


def _collect_dependencies(
    pkg: dict,
    extras: Sequence[str] | Literal["all"] | None = "all",
) -> list[dict]:
    """Get a list of dependencies for the given configuration.

    Parameters
    ----------
    pkg
        Library type to get dependencies for.
    extras
        Optional runtime dependency groups to get in addition to core dependencies.
        If `build` is True, this is ignored.
    """
    data = pkg["dependency"]
    deps = list(data.get("core", {}).values())
    if extras:
        optional_group_keys = data.get("optional", {}).keys()
        if extras != "all":
            for extra in extras:
                if extra not in optional_group_keys:
                    error_msg = f"Invalid optional dependency group: {extra}"
                    raise ValueError(error_msg)
        for group in data.get("optional", {}).values():
            if extras == "all" or group["name"] in extras:
                deps.extend(list(group["package"].values()))
    return _copy.deepcopy(deps)


def _resolve_variants(  # noqa: PLR0912, C901
    pkg: dict, pyver: str, input_variants: dict[str, str | int | bool] | None = None
) -> dict:
    """Get a full set of variant values based on input variants and project variant data."""
    input_variants = input_variants or {}
    pkg_var_data = pkg["dependency"].get("variant", {})
    pkg_vars = pkg_var_data.get("variants", {})
    pkg_zip_keys = pkg_var_data.get("zip_keys", [])
    # Validate input variants
    for variant_key, variant_value in input_variants.items():
        if variant_key not in pkg_vars:
            error_msg = f"Invalid variant key '{variant_key}'"
            raise ValueError(error_msg)
        if variant_value not in pkg_vars[variant_key]:
            error_msg = f"Invalid variant value '{variant_value}' for key '{variant_key}'"
            raise ValueError(error_msg)
    for zip_keys in pkg_zip_keys:
        input_keys = []
        input_indices = []
        for zip_key in zip_keys:
            if zip_key in input_variants:
                input_keys.append(zip_key)
                input_indices.append(pkg_vars[zip_key].index(input_variants[zip_key]))
        if len(input_indices) > 1 and len(set(input_indices)) != 1:
            error_msg = f"Variant keys '{input_keys}' must be zipped, but values correspond to indices {input_indices}"
            raise ValueError(error_msg)
    output = {}
    # Set the variant values
    for pkg_var_key, pkg_var_items in pkg_vars.items():
        if pkg_var_key in input_variants:
            output[pkg_var_key] = input_variants[pkg_var_key]
            continue
        for zip_keys in pkg_zip_keys:
            if pkg_var_key not in zip_keys:
                continue
            other_keys = set(zip_keys) - {pkg_var_key}
            for other_key in other_keys:
                if other_key in input_variants:
                    other_value = input_variants[other_key]
                    other_value_idx = pkg_vars[other_key].index(other_value)
                    output[pkg_var_key] = pkg_var_items[other_value_idx]
                    break
            else:
                for other_key in other_keys:
                    if other_key in output:
                        other_value = output[other_key]
                        other_value_idx = pkg_vars[other_key].index(other_value)
                        output[pkg_var_key] = pkg_var_items[other_value_idx]
                        break
                else:
                    continue
                break
            break
        else:
            output[pkg_var_key] = pyver if pkg_var_key == "python" else pkg_var_items[0]
    return output


def _evaluate_selector(selector: str, selector_vars: dict[str, str | int | bool]) -> bool:
    """Evaluate a preprocessing selector expression using the given variables.

    Parameters
    ----------
    selector
        Selector expression to evaluate.
    selector_vars
        Dictionary of selector variables and their values.

    Returns
    -------
    result
        Result of the selector evaluation.
    """
    return eval(selector, selector_vars)  # noqa: S307


def _get_native_platform() -> PlatformName:
    """Get the native Conda subdirectory name on the current machine.

    Notes
    -----
    The implementation is the same as `conda.base.context.context.subdir`.

    References
    ----------
    - [Conda source code](https://github.com/conda/conda/blob/5408dd1225827e1e4f5b2f5f7861ae8358db9acd/conda/base/context.py#L666-L681)

    See Also
    --------
    - [`Platform.current()` in `py-rattler`](https://conda.github.io/rattler/py-rattler/platform/#rattler.platform.platform.Platform.current)
    - [Enum Platform](https://docs.rs/rattler_conda_types/latest/rattler_conda_types/enum.Platform.html)
    """
    _platform_map = {
        "freebsd13": "freebsd",
        "linux2": "linux",
        "linux": "linux",
        "darwin": "osx",
        "win32": "win",
        "zos": "zos",
    }
    non_x86_machines = {
        "armv6l",
        "armv7l",
        "aarch64",
        "arm64",
        "ppc64",
        "ppc64le",
        "riscv64",
        "s390x",
    }
    machine = _platform.machine()
    platform = _platform_map.get(_sys.platform)
    if not platform:
        error_msg = f"Unknown current platform: {_sys.platform}"
        raise RuntimeError(error_msg)
    if machine in non_x86_machines:
        return f"{platform}-{machine}"
    if platform == "zos":
        return "zos-z"
    bits = 8 * _struct.calcsize("P")
    return f"{platform}-{bits}"


def _create_env_file_conda(
    packages: list[dict] | None = None,
    pip_packages: list[dict] | None = None,
    env_name: str | None = None,
    indent: int | None = 2,
) -> str:
    """Create a Conda [environment.yml](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-file-manually) file.

    Parameters
    ----------
    packages:
        List of dictionaries with package details.
        All keys are the same as the attributes in the `environment.yml` file,
        but snake_case instead of camelCase.
    pip_packages
        List of dictionaries with pip package details.
    env_name
        Name of the conda environment.
    indent:
        Number of spaces to use for indentation.
        If `None`, a compact format is used with no indentation or newlines.
    """
    match_specs = [pkg["spec"] for pkg in (packages or [])]
    if not any((spec.startswith("pip ") or "::pip" in spec) for spec in match_specs):
        match_specs.append("conda-forge::pip")
    lines = []
    if env_name:
        lines.append(f"name: {env_name}")
    lines.append("dependencies:")
    lines.extend([f"{' ' * indent}- {match_spec}" for match_spec in sorted(match_specs)])
    if pip_packages:
        lines.append(f"{' ' * indent}- pip:")
        lines.extend([f"{' ' * (indent * 2)}- {pkg['spec']}" for pkg in pip_packages])
    return f"{'\n'.join(lines)}\n"


def _create_env_file_pip(packages: list[dict]) -> str:
    """Create a pip [requirements.txt](https://pip.pypa.io/en/stable/user_guide/#requirements-files) file.

    Parameters
    ----------
    packages:
        List of dictionaries with package details.
    """
    return f"{'\n'.join(sorted([pkg['spec'] for pkg in packages]))}\n"


def _create_env_file_apt(packages: list[dict]) -> str:
    """Create a text file with a list of apt packages.

    Parameters
    ----------
    packages:
        List of dictionaries with package details.
    """
    lines = []
    for pkg in packages:
        spec = pkg["name"]
        if "version" in pkg:
            spec += f"={pkg['version']}"
        if "release" in pkg:
            spec += f"/{pkg['release']}"
        lines.append(spec)
    return f"{'\n'.join(sorted(lines))}\n"


def _create_env_file_brew(packages: list[dict]) -> str:
    """Create a Homebrew [Brewfile](https://github.com/Homebrew/homebrew-bundle).

    Parameters
    ----------
    packages:
        List of dictionaries with package details.
    """
    out = {}
    for pkg in packages:
        if "tap" in pkg:
            out.setdefault("tap", []).append(pkg["tap"])
        out.setdefault(pkg["type"], []).append(pkg["spec"])
    sections = [
        "\n".join([f"{section}: {spec}" for spec in sorted(out[section])])
        for section in ("tap", "brew", "cask", "mas", "whalebrew", "vscode")
        if section in out
    ]
    return f"{'\n\n'.join(sections)}\n"


def _create_env_file_choco(packages: list[dict], indent: int | None = 4) -> str:
    """Create a Chocolatey [packages.config](https://docs.chocolatey.org/en-us/choco/commands/install/#packagesconfig) file.

    Parameters
    ----------
    packages:
        List of dictionaries with package details.
        All keys are the same as the attributes in the `packages.config` file,
        but snake_case instead of camelCase.
    indent:
        Number of spaces to use for indentation.
        If `None`, a compact format is used with no indentation or newlines.
    """
    root = _ET.Element("packages")
    for pkg in packages:
        package_element = _ET.SubElement(root, "package")
        for key, value in pkg.items():
            if value is not None and value not in ("homepage",):
                package_element.set(_snake_case_to_camel_case(key), str(value))
    xml_str = _ET.tostring(root, encoding="utf-8")
    # Format the XML string to add indentation
    parsed_xml = _xml_minidom.parseString(xml_str)  # noqa: S318
    if indent is None:
        # Produce a single-line XML with no newlines or indentation
        formatted_xml = parsed_xml.toxml(encoding="utf-8")
    else:
        # Format the XML string with specified indentation
        formatted_xml = parsed_xml.toprettyxml(indent=" " * indent, encoding="utf-8")
    return f"{formatted_xml.decode('utf-8').strip()}\n"


def _create_env_file_winget(packages: list[dict], indent: int | None = 4) -> str:
    """Create a winget [packages.json](https://github.com/microsoft/winget-cli/blob/master/schemas/JSON/packages/packages.schema.2.0.json) file.

    Parameters
    ----------
    packages:
        List of dictionaries with package details.
        Keys are the same as the attributes in the `packages.json` file,
        but snake_case instead of camelCase.
        Data is in a flat structure, with each package defining its source.
    indent:
        Number of spaces to use for indentation.
        If `None`, a compact format is used with no indentation or newlines.
    """
    file = {"Sources": []}
    for pkg in packages:
        source = {_snake_case_to_camel_case(key): value for key, value in pkg["source"].items()}
        package = {
            _snake_case_to_camel_case(key): value
            for key, value in pkg.items()
            if key not in ("source", "homepage")
        }
        for src in file["Sources"]:
            if src["SourceDetails"] == source:
                src["Packages"].append(package)
                break
        else:
            file["Sources"].append({"SourceDetails": source, "Packages": [package]})
    return f"{_json.dumps(file, sort_keys=True, indent=indent).strip()}\n"


def _snake_case_to_camel_case(string: str) -> str:
    """Convert a snake_case string to CamelCase."""
    components = string.split("_")
    return "".join([components[0]] + [x.title() for x in components[1:]])


def _parse_args() -> _argparse.Namespace:
    def source_list(value: str) -> list[str]:
        """Ensure the input is a comma-separated list of valid choices."""
        items = value.split(",")
        invalid = [item for item in items if item not in valid_sources]
        if invalid:
            error_msg = (
                f"Invalid choices: {', '.join(invalid)}. Valid options: {', '.join(valid_sources)}"
            )
            raise _argparse.ArgumentTypeError(error_msg)
        return items

    def boolean_or_source_list(value: str) -> bool | list[str]:
        """Parse input as boolean or a list of valid choices."""
        true_values = {"true", "yes", "1"}
        false_values = {"false", "no", "0"}
        if value.lower() in true_values:
            return True
        if value.lower() in false_values:
            return False
        return source_list(value)

    valid_sources = ["conda", "pip", "apt", "brew", "choco", "winget", "bash", "pwsh"]
    parser = _argparse.ArgumentParser(description="Install package and/or test-suite dependencies.")
    parser.add_argument("--filepath", type=str, default=".github/.repodynamics/metadata.json")
    parser.add_argument(
        "--packages",
        type=_json.loads,
        default='["main", "test"]',
        help="JSON string of package specifications.",
    )
    parser.add_argument("--python-version", type=str, default=None)
    parser.add_argument(
        "--build-platform",
        type=str,
        choices=list(_CONDA_SUBDIR_TO_OS_ARCH.keys()),
        default=None,
    )
    parser.add_argument(
        "--target-platform",
        type=str,
        choices=list(_CONDA_SUBDIR_TO_OS_ARCH.keys()),
        default=None,
    )
    parser.add_argument(
        "--sources",
        nargs="*",
        choices=valid_sources,
        default=None,
    )
    parser.add_argument(
        "--exclude-sources",
        nargs="*",
        choices=["conda", "pip", "apt", "brew", "choco", "winget", "bash", "pwsh"],
        default=None,
    )
    parser.add_argument("--exclude-installed", action=_argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--pip-in-conda", action=_argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--conda-env-name", type=str, default=None)
    parser.add_argument(
        "--install",
        type=boolean_or_source_list,
        default=True,
        help="Boolean (true/false) or a list of package managers (comma-separated): conda, pip, apt, brew, choco, winget, bash, pwsh",
    )
    parser.add_argument(
        "--exclude-install",
        nargs="*",
        choices=["conda", "pip", "apt", "brew", "choco", "winget", "bash", "pwsh"],
        default=None,
        help="List of package managers to exclude from installation: conda, pip, apt, brew, choco, winget, bash, pwsh",
    )
    parser.add_argument("--output-dir", type=str, default=None)
    parser.add_argument("--overwrite", action=_argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--filename-conda", type=str, default="environment.yml")
    parser.add_argument("--filename-pip", type=str, default="requirements.txt")
    parser.add_argument("--filename-apt", type=str, default="apt.txt")
    parser.add_argument("--filename-brew", type=str, default="Brewfile")
    parser.add_argument("--filename-choco", type=str, default="packages.config")
    parser.add_argument("--filename-winget", type=str, default="packages.json")
    parser.add_argument("--filename-bash", type=str, default="install.sh")
    parser.add_argument("--filename-pwsh", type=str, default="install.ps1")
    parser.add_argument("--indent-json", type=int, default=4)
    parser.add_argument("--indent-xml", type=int, default=4)
    parser.add_argument("--indent-yaml", type=int, default=2)
    return parser.parse_args()


_logger = _logging.getLogger(__name__)

if __name__ == "__main__":
    _logging.basicConfig(level=_logging.INFO)
    args = vars(_parse_args())
    _logger.info("Running with arguments: %s", args)
    run(**args)
