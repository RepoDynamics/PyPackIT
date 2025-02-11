# PyPackIT © 2023–2024 RepoDynamics
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Generate and/or install package dependencies."""

from __future__ import annotations as _annotations

import subprocess as _subprocess
import copy as _copy
from typing import TYPE_CHECKING as _TYPE_CHECKING
from pathlib import Path as _Path
import json as _json
import platform as _platform
import sys as _sys
import struct as _struct
import xml.etree.ElementTree as _xml_ET
import xml.dom.minidom as _xml_minidom

if _TYPE_CHECKING:
    from typing import Literal, Sequence
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


_REL_DEP_FILEPATH = "data/dependencies.json"
"""Relative path from this file to the dependency data file."""


class DependencyInstaller:
    """Resolve and install dependencies based on given configurations.

    Parameters
    ----------
    filepath
        Path to the JSON file containing dependency data.
        If not provided, the default dependency file is used.
    """

    def __init__(self, filepath: str | _Path | None = None):
        input_filepath = filepath or _Path(__file__).parent / _REL_DEP_FILEPATH
        dependency_filepath = _Path(input_filepath).resolve()
        if not dependency_filepath.is_file():
            raise FileNotFoundError(f"Dependency file not found at '{dependency_filepath}'")
        try:
            dep_data = _json.loads(dependency_filepath.read_text())
        except _json.JSONDecodeError as e:
            raise ValueError(f"Failed to load dependencies from '{dependency_filepath}'") from e
        if not isinstance(dep_data, dict):
            raise ValueError(f"Invalid dependencies data loaded from '{dependency_filepath}'")
        self._data = dep_data
        return

    def create_installation_files(
        self,
        dependencies: dict[SourceName, list[dict]],
        indent_json: int | None = 4,
        indent_xml: int | None = 4,
        indent_yaml: int | None = 2,
        conda_env_name: str | None = None,
        combine_scripts: bool = True,
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
        filename_bash_template: str = "bash/{}.sh",
        filename_pwsh_template: str = "pwsh/{}.ps1",
    ):
        """Create environment files for dependencies."""

        def _write_file(filename: str):
            filepath = output_dir / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            if not filepath.exists() or overwrite:
                filepath.write_text(dep_content)
            else:
                raise FileExistsError(f"File already exists: '{filepath}'")
            return

        inputs = locals()
        out = {}
        for source, dep_data in dependencies.items():
            deps = [dep["install"][source] for dep in dep_data]
            if source == "conda":
                out[source] = create_env_file_conda(deps, env_name=conda_env_name, indent=indent_yaml)
            elif source == "pip":
                out[source] = create_env_file_pip(deps)
            elif source == "apt":
                out[source] = create_env_file_apt(deps)
            elif source == "brew":
                out[source] = create_env_file_brew(deps)
            elif source == "choco":
                out[source] = create_env_file_choco(deps, indent=indent_xml)
            elif source == "winget":
                out[source] = create_env_file_winget(deps, indent=indent_json)
            else:
                # bash and pwsh
                if not combine_scripts:
                    out[source] = {dep["name"]: dep["install"][source] for dep in dep_data}
                else:
                    out[source] = "\n\n".join(
                        [f"# ----- {dep["name"]} -----\n{dep["install"][source]}" for dep in dep_data]
                    )
        if output_dir:
            output_dir = _Path(output_dir)
            for source, content in out.items():
                if source in {"bash", "pwsh"} and not combine_scripts:
                    for dep_name, dep_content in content.items():
                        _write_file(inputs[f"filename_{source}_template"].format(dep_name))
                else:
                    _write_file(inputs[f"filename_{source}"])
        return out

    def resolve_dependencies(
        self,
        dependencies: list[dict],
        platform: PlatformName | None = None,
        variants: dict[str, str | int | bool] | None = None,
        sources: Sequence[SourceName] | None = None,
        exclude_sources: Sequence[SourceName] | None = None,
        exclude_installed: bool = True,
    ) -> dict[SourceName, list[dict]]:
        """Resolve dependencies for a given platform and set of variants.

        Parameters
        ----------
        dependencies
            List of dependencies to resolve.
            This can be the output of `get_dependencies`.
        platform
            Name of the target platform.
            This corresponds to the conda-build subdirectory name.
            If not provided, the current native platform is used.
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

        Returns
        -------

        """
        if not platform:
            platform = get_native_platform()
        selector_vars = {"build_platform": platform} | {
            key: key in _CONDA_SUBDIR_TO_OS_ARCH[platform] for key in _CONDA_SELECTOR_VARS
        } | self.get_variants(variants)
        if not sources:
            sources = ["conda", "pip"]
            if platform.startswith("linux"):
                sources.extend(["apt", "bash", "brew"])
            elif platform.startswith("osx"):
                sources.extend(["brew", "bash"])
            elif platform.startswith("win"):
                sources.extend(["choco", "winget", "pwsh"])
        exclude_sources = set(exclude_sources or [])
        out = {}
        for dependency in dependencies:
            if exclude_sources and set(dependency.get("install", {}).keys()) & exclude_sources:
                continue
            selector = dependency.get("selector")
            if selector and not evaluate_selector(selector, selector_vars):
                continue
            if exclude_installed and dependency.get("validator"):
                validator_result = _subprocess.run(["python", "-c", dependency["validator"]], capture_output=True)
                if validator_result.returncode == 0:
                    continue
            for source in sources:
                if source in dependency["install"]:
                    out.setdefault(source, []).append(dependency)
                    break
            else:
                raise ValueError(
                    f"Dependency '{dependency['name']}' not installable from any source. "
                    f"Available sources are: {list(dependency['install'].keys())}"
                )
        return out

    def get_dependencies(
        self,
        build: bool = False,
        extras: Sequence[str] | None = None,
    ) -> list[dict]:
        """Get a list of dependencies for the given configuration.

        Parameters
        ----------
        build
            Whether to get build (True) or runtime dependencies (False).
        extras
            Optional runtime dependency groups to get in addition to core dependencies.
            If `build` is True, this is ignored.
        """
        deps = list(self._data.get("build" if build else "core", {}).values())
        if extras and not build:
            self.verify_compatibility(extras)
            optional_group_keys = []
            for extra in extras:
                for group in self._data.get("group", {}).values():
                    if extra == group["name"]:
                        optional_group_keys.extend(group["optionals"])
                        break
                else:
                    for group_key, group in self._data.get("optional", {}).items():
                        if extra == group["name"]:
                            optional_group_keys.append(group_key)
                            break
                    else:
                        raise ValueError(f"Invalid optional dependency group: {extra}")
            for group_key in set(optional_group_keys):
                deps.extend(list(self._data["optional"][group_key]["package"].values()))
        return _copy.deepcopy(deps)

    def verify_compatibility(self, extras: Sequence[str]):
        """Verify that the given optional dependency groups are compatible with one another."""
        set_extras = set(extras)
        for group in self._data.get("group", {}).values():
            if group["compatible"]:
                continue
            intersection = set(group["optionals"]) & set_extras
            if len(intersection) > 1:
                raise ValueError(
                    f"Incompatible optional dependency groups: {intersection}\n{group['description']}"
                )
        return

    def get_variants(self, input_variants: dict[str, str | int | bool] | None = None) -> dict:
        """Get a full set of variant values based on input variants and project variant data."""
        input_variants = input_variants or {}
        project_variant_data = self._data.get("variant", {})
        project_variants = project_variant_data.get("variants", {})
        project_zip_keys = project_variant_data.get("zip_keys", [])
        # Validate input variants
        for variant_key, variant_value in input_variants.items():
            if variant_key not in project_variants:
                raise ValueError(f"Invalid variant key '{variant_key}'")
            if variant_value not in project_variants[variant_key]:
                raise ValueError(f"Invalid variant value '{variant_value}' for key '{variant_key}'")
        for zip_keys in project_zip_keys:
            input_keys = []
            input_indices = []
            for zip_key in zip_keys:
                if zip_key in input_variants:
                    input_keys.append(zip_key)
                    input_indices.append(project_variants[zip_key].index(input_variants[zip_key]))
            if len(input_indices) > 1 and len(set(input_indices)) != 1:
                raise ValueError(
                    f"Variant keys '{input_keys}' must be zipped, but values correspond to indices {input_indices}")
        output = {}
        # Set the variant values
        for project_variant_key, project_variant_values in project_variants.items():
            if project_variant_key in input_variants:
                output[project_variant_key] = input_variants[project_variant_key]
                continue
            for zip_keys in project_zip_keys:
                if project_variant_key not in zip_keys:
                    continue
                other_keys = set(zip_keys) - {project_variant_key}
                for other_key in other_keys:
                    if other_key in input_variants:
                        other_value = input_variants[other_key]
                        other_value_idx = project_variants[other_key].index(other_value)
                        output[project_variant_key] = project_variant_values[other_value_idx]
                        break
                else:
                    for other_key in other_keys:
                        if other_key in output:
                            other_value = output[other_key]
                            other_value_idx = project_variants[other_key].index(other_value)
                            output[project_variant_key] = project_variant_values[other_value_idx]
                            break
                    else:
                        continue
                    break
                break
            else:
                output[project_variant_key] = (
                    ".".join(_sys.version_info[:2]) if project_variant_key == "python" else project_variant_values[0]
                )
        return output


def evaluate_selector(selector: str, selector_vars: dict[str, str | int | bool]) -> bool:
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
    return eval(selector, selector_vars)


def get_native_platform() -> PlatformName:
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
        raise RuntimeError(f"Unknown current platform: {_sys.platform}")
    if machine in non_x86_machines:
        return f"{platform}-{machine}"
    if platform == "zos":
        return "zos-z"
    bits = 8 * _struct.calcsize("P")
    return f"{platform}-{bits}"


def create_env_file_conda(
    packages: list[dict],
    env_name: str | None = None,
    indent: int | None = 2,
) -> str:
    """Create a Conda
    [environment.yml](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-file-manually)
    file.

    Parameters
    ----------
    packages:
        List of dictionaries with package details.
        All keys are the same as the attributes in the `environment.yml` file,
        but snake_case instead of camelCase.
    env_name
        Name of the conda environment.
    indent:
        Number of spaces to use for indentation.
        If `None`, a compact format is used with no indentation or newlines.
    """
    lines = []
    if env_name:
        lines.append(f"name: {env_name}")
    lines.append("dependencies:")
    for pkg in packages:
        lines.append(f"{" " * indent}- {pkg["spec"]}")
    return f"{"\n".join(lines)}\n"


def create_env_file_pip(packages: list[dict]) -> str:
    """Create a pip
    [requirements.txt](https://pip.pypa.io/en/stable/user_guide/#requirements-files) file.

    Parameters
    ----------
    packages:
        List of dictionaries with package details.
    """
    return f"{"\n".join([pkg["spec"]["pep508"] for pkg in packages])}\n"


def create_env_file_apt(packages: list[dict]) -> str:
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
    return f"{"\n".join(lines)}\n"


def create_env_file_brew(packages: list[dict]) -> str:
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
    sections = []
    for section in ("tap", "brew", "cask", "mas", "whalebrew", "vscode"):
        if section in out:
            sections.append("\n".join([f"{section}: {spec}" for spec in out[section]]))
    return f"{"\n\n".join(sections)}\n"


def create_env_file_choco(packages: list[dict], indent: int | None = 4) -> str:
    """Create a Chocolatey
    [packages.config](https://docs.chocolatey.org/en-us/choco/commands/install/#packagesconfig) file.

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
    root = _xml_ET.Element("packages")
    for pkg in packages:
        package_element = _xml_ET.SubElement(root, "package")
        for key, value in pkg.items():
            if value is not None and value not in ("homepage", ):
                package_element.set(snake_case_to_camel_case(key), str(value))
    xml_str = _xml_ET.tostring(root, encoding='utf-8')
    # Format the XML string to add indentation
    parsed_xml = _xml_minidom.parseString(xml_str)
    if indent is None:
        # Produce a single-line XML with no newlines or indentation
        formatted_xml = parsed_xml.toxml(encoding="utf-8")
    else:
        # Format the XML string with specified indentation
        formatted_xml = parsed_xml.toprettyxml(indent=" " * indent, encoding="utf-8")
    return f"{formatted_xml.decode("utf-8").strip()}\n"


def create_env_file_winget(packages: list[dict], indent: int | None = 4) -> str:
    """Create a winget
    [packages.json](https://github.com/microsoft/winget-cli/blob/master/schemas/JSON/packages/packages.schema.2.0.json)
    file.

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
        source = {snake_case_to_camel_case(key): value for key, value in pkg["source"].items()}
        package = {snake_case_to_camel_case(key): value for key, value in pkg.items() if key not in ("source", "homepage")}
        for src in file["Sources"]:
            if src["SourceDetails"] == source:
                src["Packages"].append(package)
                break
        else:
            file["Sources"].append({"SourceDetails": source, "Packages": [package]})
    return f"{_json.dumps(file, sort_keys=True, indent=indent).strip()}\n"


def snake_case_to_camel_case(string: str) -> str:
    """Convert a snake_case string to CamelCase."""
    components = string.split('_')
    return ''.join([components[0]] + [x.title() for x in components[1:]])
