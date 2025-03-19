from __future__ import annotations as _annotations

import copy
from typing import TYPE_CHECKING as _TYPE_CHECKING
import xml.etree.ElementTree as _xml_ET
import xml.dom.minidom as _xml_minidom
from pathlib import Path as _Path
import os as _os

import jsonpath_ng as _jpath
import mdit as _mdit
import pyserials as _ps
import pylinks as _pl
import jinja2 as _jinja
from loggerman import logger as _logger

if _TYPE_CHECKING:
    from typing import Literal, Callable, Any, Sequence


def create_env_file_conda(
    packages: list[dict] | None = None,
    pip_packages: list[dict] | None = None,
    env_name: str | None = None,
    variables: list[dict] | None = None,
) -> dict:
    """Create a Conda
    [environment.yml](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-file-manually)
    file.

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
    variables:
        Environment variables to set in the conda environment.
    """
    file = {}
    if env_name:
        file["name"] = env_name
    dependencies = [pkg["spec"]["full"] for pkg in (packages or [])]
    if pip_packages and not any(spec.startswith("pip ") for spec in dependencies):
        dependencies.append("pip")
    if pip_packages:
        pip_specs = sorted([pkg["spec"]["full"] for pkg in pip_packages])
        dependencies.append({"pip": pip_specs})
    file["dependencies"] = dependencies
    if variables:
        # https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html#setting-environment-variables
        # https://stackoverflow.com/questions/31598963/how-to-set-specific-environment-variables-when-activating-conda-environment
        file["variables"] = {var["key"]: var["value"] for var in variables}
    return file


def create_environment_files(
    dependencies: list[dict],
    env_name: str = "",
    python_version_spec: str = "",
) -> dict[str, dict[str, str | None]]:
    """Create pip `requirements.txt` and conda `environment.yml` files from a list of dependencies.

    Parameters
    ----------
    dependencies : list[dict]
        A list of dependencies as dictionaries with paths `pip.spec`, `conda.spec`, and `conda.channel`.
    env_name : str, default: 'conda_env'
        The name of the conda environment.

    Returns
    -------
    conda_env : str
        The contents of the `environment.yaml` conda environment file.
    pip_env : str | None
        The contents of the `requirements.txt` pip requirements file,
        or `None` if no pip dependencies were found.
    pip_full : bool
        Whether the pip requirements file contains all dependencies.
    """
    def make_env_file(manager: Literal["apt", "brew", "conda", "pip", "pwsh"], deps: list[str]) -> str:
        if manager == "conda":
            env = {"dependencies": deps}
            if env_name:
                env["name"] = env_name
            return _ps.write.to_yaml_string(data=env, end_of_file_newline=True)
        return "\n".join(deps)

    availability_types = ("inclusive", "exclusive")
    # Initialize lists of specifiers
    deps = {
        availability_type: {
            "apt": [],
            "brew": [],
            "conda": [f"python {python_version_spec}".strip()],
            "pip": [],
            "pwsh": [],
        } for availability_type in availability_types
    }
    pip_but_not_conda = []

    for dependency in dependencies:
        # Generate specifiers
        specs = {
            "apt": dependency.get("apt", {}).get("spec"),
            "brew": dependency.get("brew", {}).get("spec"),
            "conda": (
                # Specify channels for each package separately:
                #   https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-file-manually
                # Selectors are not yet available for environment files:
                #   https://github.com/conda/conda/issues/8089
                f"{dependency["conda"]["channel"]}::{dependency["conda"]["spec"]}"
                if "conda" in dependency else None
            ),
            "pip": (
                f"{dependency["pip"]["spec"].strip()}{f"; {dependency["pip"]["selector"].strip()}" if "selector" in dependency["pip"] else ""}"
                if "pip" in dependency else None
            ),
            "pwsh": dependency.get("pwsh", {}).get("spec"),
        }
        availability_count = 0
        available_manager = None
        # Add any available specifier to its corresponding 'full' list
        for manager, spec in specs.items():
            if spec:
                availability_count += 1
                available_manager = manager
                deps["inclusive"][manager].append(spec)
        # If only one specifier is available, add it to the 'only' list
        if availability_count == 1:
            deps["exclusive"][available_manager].append(specs[available_manager])
        # If neither 'pip' nor 'conda' are defined, add available specifiers to system package managers' 'only' list
        elif not (specs["conda"] or specs["pip"]):
            for manager in ("apt", "brew", "pwsh"):
                if specs[manager]:
                    deps["exclusive"][manager].append(specs[manager])
        if specs["pip"] and not specs["conda"]:
            pip_but_not_conda.append(specs["pip"])
    if pip_but_not_conda:
        deps["inclusive"]["conda"].insert(1, "pip")
        deps["full"]["conda"].append({"pip": pip_but_not_conda})
    env_files = {}
    for availability_type in availability_types:
        type_env_files = env_files.setdefault(availability_type, {})
        for manager in ("apt", "brew", "conda", "pip", "pwsh"):
            deps_ = deps[availability_type][manager]
            type_env_files[manager] = "" if not deps_ or (
                manager == "conda" and len(deps_) == 1
            ) else make_env_file(manager=manager, deps=deps_)
    return env_files


def create_dynamic_file(
    file_type: Literal["yaml", "json", "toml", "txt", "exec"],
    content,
    filters: Sequence[tuple[str, Callable[[Any], bool], bool]] = (),
    content_item_separator: str = "\n",
    content_item_prefix: str = "",
    content_item_suffix: str = "",
    sort_keys: bool = True,
    order: list[str] | None = None,
    indent: int | None = None,
    end_of_file_newline: bool = True,
    mapping_indent: int = 2,
    sequence_indent: int = 4,
    sequence_indent_offset: int = 2,
    block_string: bool = True,
    remove_top_level_indent: bool = True
) -> str:
    if filters and isinstance(content, (list, dict)):
        has_non_inplace = False
        # Apply in-place filters
        for jsonpath_str, filter_func, inplace in filters:
            if inplace:
                jsonpath = _jpath.parse(jsonpath_str)
                content = jsonpath.filter(filter_func, content)
        # Apply non-in-place filters to a copy
        if has_non_inplace:
            content = copy.deepcopy(content)
            for jsonpath_str, filter_func, inplace in filters:
                if not inplace:
                    jsonpath = _jpath.parse(jsonpath_str)
                    content = jsonpath.filter(filter_func, content)
    if order:
        key_priority = {key: index for index, key in enumerate(order)}
        sorted_items = sorted(
            content.items(),
            key=lambda item: key_priority.get(item[0], len(order))
        )
        content = dict(sorted_items)
    if file_type in ("txt", "exec"):
        if isinstance(content, str):
            return content
        elif isinstance(content, (list, dict)):
            return content_item_separator.join(
                f"{content_item_prefix}{content_item}{content_item_suffix}"
                for content_item in (content if isinstance(content, list) else content.values())
            )
        raise ValueError(f"Content type {type(content)} not supported for dynamic files.")
    return _ps.write.to_string(
        data=content,
        data_type=file_type,
        end_of_file_newline=end_of_file_newline,
        sort_keys=sort_keys,
        indent=indent,
        indent_mapping=mapping_indent,
        indent_sequence=sequence_indent,
        indent_sequence_offset=sequence_indent_offset,
        multiline_string_to_block=block_string,
        remove_top_level_indent=remove_top_level_indent,
    )


def create_md_content(file: dict, repo_path: str | _Path) -> str:
    current_dir = _Path.cwd()
    _os.chdir(repo_path)
    try:
        doc = _mdit.generate(file["content"])
    finally:
        _os.chdir(current_dir)
    setting = file["file_setting"]["md"]
    doc_str = doc.source(
        target=setting["target"],
        filters=setting.get("filters"),
        heading_number_explicit=setting["heading_number"],
        separate_sections=False,
    )
    return doc_str


def fill_jinja_templates(templates: dict | list | str, jsonpath: str, env_vars: dict | None = None) -> dict:

    def recursive_fill(template, path):
        if isinstance(template, dict):
            filled = {}
            for key, value in template.items():
                new_path = f"{path}.{key}"
                filled[recursive_fill(key, new_path)] = recursive_fill(value, new_path)
            return filled
        if isinstance(template, list):
            filled = []
            for idx, value in enumerate(template):
                new_path = f"{path}[{idx}]"
                filled.append(recursive_fill(value, new_path))
            return filled
        if isinstance(template, str):
            try:
                filled = _jinja.Template(template).render(env_vars)
            except Exception as e:
                _logger.critical(
                    "Jinja Templating",
                    f"Failed to render Jinja template at '{path}': {e}",
                    _logger.traceback()
                )
                raise ValueError(f"Failed to render Jinja template at '{path}'") from e
            return filled
        return template

    return recursive_fill(templates, jsonpath)



def create_chocolatey_packages_config(packages: list[dict], indent: int | None = 4) -> str:
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
            if value is not None:
                package_element.set(_pl.string.snake_to_camel(key), str(value))
    xml_str = _xml_ET.tostring(root, encoding='utf-8')
    # Format the XML string to add indentation
    parsed_xml = _xml_minidom.parseString(xml_str)
    if indent is None:
        # Produce a single-line XML with no newlines or indentation
        formatted_xml = parsed_xml.toxml(encoding="utf-8")
    else:
        # Format the XML string with specified indentation
        formatted_xml = parsed_xml.toprettyxml(indent=" " * indent, encoding="utf-8")
    return formatted_xml.decode("utf-8")


def create_winget_packages_json(packages: list[dict], indent: int | None = 4) -> str:
    """Create a winget
    [packages.json](https://github.com/microsoft/winget-cli/blob/master/schemas/JSON/packages/packages.schema.2.0.json)
    file.

    Parameters
    ----------
    packages:
        List of dictionaries with package details.
        Keys are the same as the attributes in the `packages.json` file,
        but snake_case instead of camelCase.
        However, here data are in a flat structure, with each package defining its source.
    """
    file = {"Sources": []}
    for pkg in packages:
        source = {_pl.string.snake_to_camel(key): value for key, value in pkg["source"].items()}
        package = {_pl.string.snake_to_camel(key): value for key, value in pkg.items() if key != "source"}
        for src in file["Sources"]:
            if src["SourceDetails"] == source:
                src["Packages"].append(package)
                break
        else:
            file["Sources"].append({"SourceDetails": source, "Packages": [package]})
    return _ps.write.to_json_string(data=file, sort_keys=True, indent=indent)


def create_homebrew_brewfile(packages: list[dict]) -> str:
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
    return "\n\n".join(sections)




def create_pep508_dependency_specifier(pkg: dict) -> str:
    """Create a PEP 508 dependency specifier string from a dictionary of dependency details.
    """
    spec = [pkg["name"]]
    if "extras" in pkg:
        spec.append(f"[{','.join(pkg['extras'])}]")
    if "version" in pkg:
        spec.append(pkg["version"])
    if "marker" in pkg:
        spec.append(f"; {pkg['marker']}")
    return " ".join(spec)

