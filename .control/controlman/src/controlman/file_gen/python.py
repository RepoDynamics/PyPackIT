"""Python Package File Generator"""

from typing import Literal
import textwrap
from pathlib import Path as _Path
import re as _re
import copy

import pyserials as _ps
import pysyntax as _pysyntax
from loggerman import logger

import controlman
from controlman.datatype import DynamicFileType, DynamicFile
from controlman import const as _const


class PythonPackageFileGenerator:
    def __init__(
        self,
        data: _ps.NestedDict,
        data_before: _ps.NestedDict,
        repo_path: _Path,
    ):
        self._data = data
        self._data_before = data_before
        self._path_repo = repo_path
        self._type = None
        self._pkg: dict = {}
        self._pkg_before: dict = {}
        self._pyproj_tool: dict | str | None = None
        self._path_root: _Path | None = None
        self._path_src: _Path | None = None
        self._path_import: _Path | None = None
        self._path_root_before: _Path | None = None
        self._path_src_before: _Path | None = None
        self._path_import_before: _Path | None = None
        self._contributors = controlman.read_contributors(self._path_repo)
        return

    def generate(self, typ: str) -> list[DynamicFile]:
        self._type = typ
        self._pkg = _ps.NestedDict(self._data[typ])
        self._pkg_before = _ps.NestedDict(self._data_before[typ] or {})
        self._path_root = _Path(self._data[f"{typ}.path.root"])
        self._path_src = self._path_root / self._data[f"{typ}.path.source_rel"]
        self._path_import = self._path_src / self._pkg["import_name"]
        if self._data_before[f"{typ}.path"]:
            self._path_root_before = _Path(self._data_before[f"{typ}.path.root"])
            self._path_src_before = self._path_root_before / self._data_before[f"{typ}.path.source_rel"]
            self._path_import_before = self._path_src_before / self._pkg_before["import_name"]
        return (
            self.pyproject()
            + self.python_files()
            + self.typing_marker()
            + self.conda()
        )

    def is_disabled(self, key: str):
        return not any(key in source for source in [self._pkg, self._pkg_before])

    def typing_marker(self) -> list[DynamicFile]:
        if self.is_disabled("typed"):
            return []
        file = DynamicFile(
            type=DynamicFileType.PKG_CONFIG,
            subtype=(f"{self._type}_typing", f"{self._type} Typing Marker"),
            content=(
                "# PEP 561 marker file. See https://peps.python.org/pep-0561/\n"
                if self._pkg["typed"] else None
            ),
            path=f"{self._pkg['path.import']}/{_const.FILENAME_PACKAGE_TYPING_MARKER}",
            path_before=f"{self._pkg_before['path.import']}/{_const.FILENAME_PACKAGE_TYPING_MARKER}" if self._pkg_before['path.import'] else None,
        )
        return [file]

    def conda(self):
        out = []
        changelogs = controlman.read_changelog(repo_path=self._path_repo)
        for _changelog in changelogs:
            if _changelog["type"] != "local":
                changelog = _changelog
                break
        else:
            changelog = {}
        for typ, changelog in (("local", None), ("global", changelog)):
            if "conda" not in self._pkg:
                continue
            meta = CondaRecipeGenerator(
                meta=self._pkg["conda.recipe.meta"],
                pkg=self._pkg,
                data=self._data,
                recipe_dir_path=self._pkg[f"conda.recipe.path.{typ}"],
                changelog=changelog,
            ).generate()
            file = DynamicFile(
                type=DynamicFileType.PKG_CONFIG,
                subtype=(f"{self._type}_conda_recipe_meta_{typ}", f"{self._type} Conda Recipe {typ.title()} Metadata"),
                content=meta,
                path=f"{self._pkg[f"conda.recipe.path.{typ}"]}/meta.yaml",
                path_before=f"{self._pkg_before[f'conda.recipe.path.{typ}']}/meta.yaml",
            )
            out.append(file)
        return out

    def python_files(self) -> list[DynamicFile]:
        mapping = {}
        # Generate import name mapping for dependencies
        core_dep_before = self._pkg_before.get("dependency", {}).get("core", {})
        for core_dep_name, core_dep in self._pkg.get("dependency", {}).get("core", {}).items():
            if core_dep_name in core_dep_before and all(
                "import_name" in dep for dep in (core_dep, core_dep_before[core_dep_name])
            ) and (
                core_dep["import_name"] != core_dep_before[core_dep_name]["import_name"]
            ):
                mapping[core_dep_before[core_dep_name]["import_name"]] = core_dep["import_name"]
        optional_dep_before = {}
        for opt_dep_group_before in self._pkg_before.get("dependency", {}).get("optional", {}).values():
            optional_dep_before |= opt_dep_group_before["package"]
        for opt_dep_name, opt_dep_group in self._pkg.get("dependency", {}).get("optional", {}).items():
            for opt_dep_name, opt_dep in opt_dep_group["package"].items():
                if opt_dep_name in optional_dep_before and all(
                    "import_name" in dep for dep in (opt_dep, optional_dep_before[opt_dep_name])
                ) and (
                    opt_dep["import_name"] != optional_dep_before[opt_dep_name]["import_name"]
                ):
                    mapping[optional_dep_before[opt_dep_name]["import_name"]] = opt_dep["import_name"]
        # Generate import name mapping for internal packages
        for key, pkg in self._data.items():
            if not key.startswith("pypkg_"):
                continue
            pkg_before = self._data_before[key] or {}
            import_name_before = pkg_before.get("import_name")
            if import_name_before and pkg["import_name"] != import_name_before:
                mapping[import_name_before] = pkg["import_name"]
        # Get all file glob matches
        path_to_globs_map = {}
        abs_path = self._path_repo / (self._path_import_before or self._path_import)
        for config_id, file_config in self._pkg.get("source_file", {}).items():
            for filepath_match in abs_path.glob(file_config["glob"]):
                path_to_globs_map.setdefault(filepath_match, []).append((config_id, file_config))
        if not (mapping or path_to_globs_map):
            return []
        # Process each file
        out = []
        for filepath in abs_path.glob("**/*.py"):
            file_content = filepath.read_text()
            if mapping:
                file_content = _pysyntax.modify.imports(code=file_content, mapping=mapping)
            if filepath in path_to_globs_map:
                for config_id, file_config in path_to_globs_map[filepath]:
                    if "docstring" in file_config:
                        docstring_before = self._pkg_before.get("source_file", {}).get(config_id, {}).get("docstring")
                        if docstring_before != file_config["docstring"]:
                            file_content = self._update_docstring(
                                file_content,
                                file_config["docstring"],
                                docstring_before,
                            )
                    if "header_comments" in file_config:
                        header_commens_before = self._pkg_before.get("source_file", {}).get(config_id, {}).get("header_comments")
                        if header_commens_before != file_config["header_comments"]:
                            file_content = self._update_header_comments(
                                file_content,
                                file_config["header_comments"],
                                header_commens_before,
                            )
            subtype = filepath.relative_to(self._path_repo / self._path_src)
            subtype_display = str(subtype.with_suffix("")).replace("/", ".")
            fullpath_import_before = self._path_repo / (self._path_import_before or self._path_import)
            out.append(
                DynamicFile(
                    type=DynamicFileType.PKG_SOURCE,
                    subtype=(str(subtype), subtype_display),
                    content=file_content,
                    path=str(self._path_import / filepath.relative_to(fullpath_import_before)),
                    path_before=str(filepath.relative_to(self._path_repo)),
                )
            )
        return out

    def _update_docstring(self, file_content: str, template: dict, template_before: dict) -> str:

        def get_wrapped_docstring(templ: dict) -> str:
            max_line_length = templ.get("max_line_length")
            if not max_line_length:
                return templ["content"]
            lines = []
            for line in templ["content"].splitlines():
                line_parts = textwrap.wrap(line, width=max_line_length, subsequent_indent=self._get_whitespace(line, leading=True))
                lines.append('') if not line_parts else lines.extend(line_parts)
            wrapped_docstring = "\n".join(lines)
            return f"{wrapped_docstring}{self._get_whitespace(templ['content'], leading=False)}"

        docstring_text = get_wrapped_docstring(template)
        docstring_before = _pysyntax.parse.docstring(file_content)
        if template["mode"] == "replace" or docstring_before is None:
            docstring_replacement = docstring_text
        elif not template_before:
            if template["mode"] == "prepend":
                docstring_replacement = f"{docstring_text}{docstring_before}"
            else:
                docstring_replacement = f"{docstring_before}{docstring_text}"
        else:
            template_before_wrapped = get_wrapped_docstring(template_before)
            docstring_replacement = docstring_before.replace(template_before_wrapped, "", 1)
            if template["mode"] == "prepend":
                docstring_replacement = f"{docstring_text}{docstring_replacement}"
            else:
                docstring_replacement = f"{docstring_replacement}{docstring_text}"
        return _pysyntax.modify.docstring(file_content, docstring_replacement)

    def _update_header_comments(self, file_content: str, template: dict, template_before: dict) -> str:

        def get_wrapped_header_comments(templ: dict) -> str:
            max_line_length = templ.get("max_line_length")
            lines = []
            current_newlines = 0
            for line in templ["content"].splitlines():
                if not line:
                    current_newlines += 1
                    continue
                if current_newlines:
                    if current_newlines == 2:
                        lines.append('#')
                    elif current_newlines > 2:
                        lines.append('')
                    current_newlines = 0
                if max_line_length:
                    line_indent = self._get_whitespace(line, leading=True)
                    line_parts = textwrap.wrap(
                        line,
                        width=max_line_length,
                        initial_indent=f"# {line_indent}",
                        subsequent_indent=f"# {line_indent}{templ['line_continuation_indent'] * " "}",
                    )
                else:
                    line_parts = [f"# {line}"]
                lines.extend(line_parts)
            return "\n".join(lines)

        header_comments_text = get_wrapped_header_comments(template)
        header_comments_before = "\n".join(_pysyntax.parse.header_comments(file_content))
        newlines = "\n" * (template["empty_lines"] + 1)
        if template["mode"] == "replace" or header_comments_before is None:
            header_comments_replacement = header_comments_text
        elif not template_before:
            if template["mode"] == "prepend":
                header_comments_replacement = f"{header_comments_text}{newlines}{header_comments_before.strip()}"
            else:
                header_comments_replacement = f"{header_comments_before.strip()}{newlines}{header_comments_text}"
        else:
            template_before_wrapped = get_wrapped_header_comments(template_before)
            header_comments_replacement = header_comments_before.replace(template_before_wrapped, "", 1)
            if template["mode"] == "prepend":
                header_comments_replacement = f"{header_comments_text}{newlines}{header_comments_replacement.strip()}"
            else:
                header_comments_replacement = f"{header_comments_replacement.strip()}{newlines}{header_comments_text}"
        return _pysyntax.modify.header_comments(file_content, header_comments_replacement)

    def pyproject(self) -> list[DynamicFile]:
        pyproject = {
            "build-system": {"requires": "array"},
            "project": {
                "license-files": "array",
                "keywords": "array",
                "classifiers": "array",
                "authors": "array_of_inline_tables",
                "maintainers": "array_of_inline_tables",
                "dependencies": "array",
                "optional-dependencies": "table_of_arrays",
                "entry-points": "table_of_tables",
                "dynamic": "array",
            },
        }
        out = {}
        for key, value in sorted(self._pkg["pyproject"].items()):
            if not value:
                continue
            if key in pyproject:
                out[key] = self._convert_to_toml_format(data=value, types=pyproject[key])
            else:
                out[key] = value
        file_content = _ps.write.to_toml_string(data=out, sort_keys=True)
        file = DynamicFile(
            type=DynamicFileType.PKG_CONFIG,
            subtype=(f"{self._type}_pyproject", f"{self._type.upper()} PyProject"),
            content=file_content,
            path=str(self._path_root / _const.FILENAME_PKG_PYPROJECT),
            path_before=str(self._path_root_before / _const.FILENAME_PKG_PYPROJECT) if self._path_root_before else None,
        )
        return [file]

    @staticmethod
    def _convert_to_toml_format(data: dict, types: dict) -> dict:
        out = {}
        for key, val in sorted(data.items()):
            if not val:
                continue
            if key in types:
                out[key] = _ps.format.to_toml_object(data=val, toml_type=types[key])
            else:
                out[key] = val
        return out

    @staticmethod
    def _get_whitespace(string: str, leading: bool) -> str:
        match = _re.match(r"^\s*", string) if leading else _re.search(r"\s*$", string)
        return match.group() if match else ""


class CondaRecipeGenerator:

    def __init__(self, meta: dict, pkg: dict, data: _ps.NestedDict, recipe_dir_path: str, changelog: dict | None = None):
        self._path = recipe_dir_path
        self._meta_full = meta
        self._meta = meta["values"]
        self._pkg = pkg
        self._data = data
        self._changelog = changelog
        self._full_ver_env_var_name = "PKG_FULL_VERSION"
        return

    def generate(self):
        blocks = [
            self._make_header(),
            self._make_package(),
            self._make_source(),
            self._make_build(),
            self._make_requirements(),
            self._make_test(),
            self._make_about(),
        ]
        for top_level_key in ("app", "extra"):
            if top_level_key in self._meta:
                block = _ps.write.to_yaml_string(
                    data=self._meta[top_level_key],
                    end_of_file_newline=False,
                )
                blocks.append(block)
        self._meta_full.get("append", "").strip()
        return "\n\n".join(block for block in blocks if block).strip() + "\n"

    def _make_header(self) -> str:
        version = (
            f'"{self._changelog["version"]}"' if self._changelog
            else f'environ.get("{self._full_ver_env_var_name}", environ.get("GIT_DESCRIBE_TAG", "0.0.0")).removeprefix("{self._data["tag.version.prefix"]}")'
        )
        headers = [
            f'{{% set name = "{self._pkg["name"]}" %}}',
            f"{{% set version = {version} %}}",
            f'{{% set pkg_dir = "{"." if self._changelog else self._pkg["path"]["root"]}/" %}}',
            self._meta_full.get("prepend", ""),
        ]
        return "\n".join(headers).strip()

    @staticmethod
    def _make_package() -> str:
        pkg =  {
            "name": "{{ name | lower }}",
            "version": "{{ version }}",
        }
        return _ps.write.to_yaml_string({"package": pkg}, end_of_file_newline=False)

    def _make_source(self) -> str:
        source = {}
        if self._changelog:
            files = self._changelog.get("pypi", {}).get("files", [])
            for file in files:
                if file["name"].endswith(".tar.gz"):
                    source = {
                        "url": f"https://pypi.org/packages/source/{{{{ name[0]|lower }}}}/{file["name"]}",
                        "sha256": file["sha256"],
                        "sha1": file["sha1"],
                        "md5": file["md5"],
                    }
                    break
        if not source:
            source = {"path": "../" * len(self._path.split("/"))}
        return _ps.write.to_yaml_string({"source": source}, end_of_file_newline=False)

    def _make_build(self):

        def add_noarch():
            if self._pkg["python"]["pure"]:
                lines.append("noarch: python")

        def add_skip():
            condition = build.get("condition")
            if condition:
                lines.append(f"skip: True  # [{condition}]")
            return

        def add_number():
            number = "0" if self._changelog else f'{{{{ "0" if environ.get("{self._full_ver_env_var_name}") else environ.get("GIT_DESCRIBE_NUMBER", 0) }}}}'
            lines.append(f"number: {number}")
            return

        def add_string():
            if self._changelog:
                return
            lines.extend(
                self._make_multi_key_entry(key="string", data=build)
            )
            for key in ("force_use_keys", "force_ignore_keys"):
                lines.extend(
                    self._make_yaml_array(key=key, data=build)
                )
            return

        def add_entry_points():
            entry_points = self._pkg.get("entry", {})
            out = []
            for key in ("cli", "gui"):
                if key in entry_points:
                    for entry in entry_points[key].values():
                        conda_selector = entry["conda"]
                        if not conda_selector:
                            continue
                        selector = "" if conda_selector is True else f"  # [{conda_selector}]"
                        out.append(f"  - {entry["name"]} = {entry["ref"]}{selector}")
            if not out:
                return
            lines.append("entry_points:")
            lines.extend(out)
            return

        def add_ignore_prefix_files():
            key = "ignore_prefix_files"
            if key not in build:
                return
            data = build[key]
            if isinstance(data, list):
                lines.extend(self._make_yaml_array(key=key, data=build))
            else:
                lines.extend(self._make_multi_key_entry(key=key, data=build))
            return

        def add_script_env():
            lines.extend(
                self._make_yaml_array(
                    key="script_env",
                    data=build,
                    add_items=[f"- {self._full_ver_env_var_name}"] if not self._changelog else None
                )
            )
            return

        def add_run_exports():
            exports = build.get("run_exports")
            if not exports:
                return
            sublines = []
            for key in ("strong", "weak"):
                sublines.extend(self._make_yaml_array(key=key, data=exports))
            lines.extend(self._prepend_and_append(sublines, exports))
            return

        build = self._meta.get("build", {}).get("values", {})
        lines = []

        for key, typ in (
            ("noarch", add_noarch),
            ("skip", add_skip),
            ("script", "multi"),
            ("number", add_number),
            ("string", add_string),
            ("entry_points", add_entry_points),
            ("osx_is_app", "multi"),
            ("python_site_packages_path", "multi"),
            ("track_features", "array"),
            ("preserve_egg_dir", "multi"),
            ("skip_compile_pyc", "array"),
            ("no_link", "array"),
            ("rpaths", "array"),
            ("always_include_files", "array"),
            ("binary_relocation", "multi"),
            ("detect_binary_files_with_prefix", "multi"),
            ("binary_has_prefix_files", "array"),
            ("has_prefix_files", "array"),
            ("ignore_prefix_files", add_ignore_prefix_files),
            ("include_recipe", "multi"),
            ("script_env", add_script_env),
            ("run_exports", add_run_exports),
            ("ignore_run_exports", "array"),
            ("ignore_run_exports_from", "array"),
            ("pin_depends", "multi"),
            ("overlinking_ignore_patterns", "array"),
            ("missing_dso_whitelist", "array"),
            ("runpath_whitelist", "array")
        ):
            if typ == "multi":
                lines.extend(self._make_multi_key_entry(key=key, data=build))
            elif typ == "array":
                lines.extend(self._make_yaml_array(key=key, data=build))
            else:
                typ()
        final_lines = self._make_yaml_mapping(key="build", lines=lines, data=self._meta["build"])
        return "\n".join(final_lines).strip()

    def _make_requirements(self):
        reqs = self._meta.get("requirements", {}).get("values", {})
        lines = []
        for key in ("build", "host", "run", "run_constrained"):
            lines.extend(self._make_yaml_array(key=key, data=reqs))
        final_lines = self._make_yaml_mapping(key="requirements", lines=lines, data=self._meta["requirements"])
        return "\n".join(final_lines).strip()

    def _make_test(self):
        test = self._meta.get("test", {}).get("values", {})
        lines = []
        for key in ("imports", "requires", "commands", "files", "source_files", "downstreams"):
            lines.extend(self._make_yaml_array(key=key, data=test))
        final_lines = self._make_yaml_mapping(key="test", lines=lines, data=self._meta["test"])
        return "\n".join(final_lines).strip()

    def _make_about(self):
        about = copy.deepcopy(self._meta["about"])
        readme = self._pkg["pyproject"]["project"].get("readme", {})
        if "text" in readme:
            about["description"] = readme["text"]
        elif "file" in readme:
            about["description"] = "\n".join(
                (
                    "{{",
                    "  load_file_regex(",
                    f'    load_file=pkg_dir ~ "{readme["file"]}",',
                    f'    regex_pattern="(?s)^(.*)$",',
                    '  )[1] | default("") | indent(width=4)',
                    "}}"
                )
            )
        return _ps.write.to_yaml_string(data={"about": about}, end_of_file_newline=False)

    def _make_multi_key_entry(self, key: str, data: dict) -> list[str]:
        if key not in data:
            return []
        entries = data[key]
        out = []
        for entry in entries:
            out.append(f"{key}: {entry["value"]}{self._make_selector(entry)}")
        return out

    def _make_yaml_array(self, key: str, data: dict, add_items: list[str] | None = None) -> list[str]:
        lines = []
        array = data.get(key, {})
        for value in array.get("values", []):
            lines.append(f"- {value["value"]}{self._make_selector(value)}")
        lines.extend(add_items or [])
        all_lines = self._prepend_and_append(lines, array)
        if not all_lines:
            return []
        return [f"{key}:"] + [f"  {line}" for line in all_lines]

    def _make_yaml_mapping(self, key: str, lines: list[str], data: dict):
        return [f"{key}:"] + [f"  {line}" for line in self._prepend_and_append(lines, data)]

    @staticmethod
    def _prepend_and_append(core: list[str], data: dict):
        lines = []
        prepend = data.get("prepend")
        if prepend:
            lines.extend(prepend.splitlines())
        lines.extend(core)
        append = data.get("append")
        if append:
            lines.extend(append.splitlines())
        return lines

    @staticmethod
    def _make_selector(data: dict):
        selector = data.get("selector")
        return f"  # [{selector}]" if selector else ""