"""Inline hooks passed to code templates in control center YAML files."""

from __future__ import annotations

import json as _json
import shlex as _shlex
from typing import TYPE_CHECKING

import mdit
import pkgdata
import pylinks as pl
import pyserials as ps
from loggerman import logger
from pylinks.exception.api import WebAPIError as _WebAPIError

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any, Literal, Sequence

    from proman.manager import Manager


class InlineDataGenerator:
    """Inline Hooks.

    During control center synchronization events,
    this class is instantiated with the given parameters,
    and made available to code templates in control center YAML files
    as a variable named `hook`.

    Parameters
    ----------
    repo_path
        Path to the root of the repository.
    ccc
        Control center configurations
        from the existing `metadata.json` file
        on the current branch.
    ccc_main
        Control center configurations
        from the existing `metadata.json` file
        on the main branch.
    cache_manager
        Cache manager with `get` and `set` methods
        to retrieve and set cached values.
    github_token
        GitHub token for making authenticated GitHub API requests.
        This is always provided when running on the cloud,
        but on local machines it is only provided if the user explicitly
        inputs one.
    kwargs
        For forward compatibility with newer PyPackIT versions
        that may add additional input argument.
    """

    def __init__(self, manager: Manager):
        self.manager = manager
        self.repo_path = self.manager.git.repo_path
        self.ccc = self.manager.data
        self.ccc_main = self.manager.main.data
        self.cache_manager = self.manager.cache
        self.get = None

        self._binder_files = {}
        return

    def __call__(self, get_metadata: Callable[[str, Any, bool], Any]) -> InlineDataGenerator:
        """Prime this instance with the JSONPath resolver function.

        This method is used internally by PyPackIT,
        and is of no use to the user.
        It exists due to a technical detail,
        namely that the JSONPath resolver function
        is not available during instantiation.
        When this instance is passed to code templates,
        this method is already called.

        Parameters
        ----------
        get_metadata
            A function to retrieve current control center configurations.
        """
        self.get = get_metadata
        return self

    def docker_apt(
        self,
        devcontainer_id: str,
        group: str,
        steps: Literal["install", "post_install", "all"] = "all"
    ) -> list[dict[str, str]]:
        apt_packages = self.get(f"devcontainer_{devcontainer_id}.apt", {})
        group_packages = [pkg for pkg in apt_packages.values() if pkg["group"] == group]
        out = []
        if not group_packages:
            return out
        apt_group_repos = False
        apt_group_post_install = False
        for apt_group_pkg in group_packages:
            if "repo" in apt_group_pkg:
                apt_group_repos = True
            if "post_install" in apt_group_pkg:
                apt_group_post_install = True
        apt_paths = self.get(f"devcontainer_{devcontainer_id}.path.apt.{group}")
        container_share_dir = self.get(f"devcontainer_{devcontainer_id}.var.share_dir")
        container_log_dir = self.get(f"devcontainer_{devcontainer_id}.var.log_dir")
        if steps in ("install", "all"):
            argname_pkg_file = f"APT_{group.upper()}_PACKAGES"
            packages_filepath = apt_paths["packages"]
            out.extend(
                [
                    {"ARG": {argname_pkg_file: f"{container_share_dir}/{packages_filepath}"}},
                    {"COPY": f'["{packages_filepath}", "${argname_pkg_file}"]'},
                ]
            )
            if apt_group_repos:
                repos_filepath = apt_paths["repos"]
                argname_repo_file = f"APT_{group.upper()}_REPOS"
                out.extend(
                    [
                        {"ARG": {argname_repo_file: f"{container_share_dir}/{repos_filepath}"}},
                        {"COPY": f'["{repos_filepath}", "${argname_repo_file}"]'},
                    ]
                )
            repofile_arg = f' --apt-repos "${argname_repo_file}" ' if apt_group_repos else " "
            logfile = f"{container_log_dir}/apt_install_{group}.log"
            run = f'"$SYSPKG_INSTALL_SCRIPT" --apt "${argname_pkg_file}"{repofile_arg}--logfile {logfile}'
            out.append({"RUN": run})
        if steps in ("post_install", "all") and apt_group_post_install:
            post_install_filepath = apt_paths["post_install"]
            argname_post_install_file = f"APT_{group.upper()}_POST_INSTALL"
            out.extend(
                [
                    {"ARG": {argname_post_install_file: f"{container_share_dir}/{post_install_filepath}"}},
                    {"COPY": f'["{post_install_filepath}", "${argname_post_install_file}"]'},
                    {
                        "RUN": (
                            f"chmod +x ${argname_post_install_file};\n"
                            f'${argname_post_install_file}'
                        )
                    },
                ]
            )
        return out

    def pypkg_test(self, test_pkg_id: str) -> dict:
        """Create test package data."""

        def install_env_script(
            build_platform: str,
            python_version: str,
            conda_env_name: str,
            source: Literal["pip", "conda"],
        ) -> str:
            sources = ["pip", "conda"] if source == "pip" else ["conda", "pip"]
            if build_platform.startswith("linux"):
                sources.extend(["apt", "bash", "brew"])
            elif build_platform.startswith("osx"):
                sources.extend(["brew", "bash"])
            elif build_platform.startswith("win"):
                sources.extend(["choco", "pwsh"])
            return (
                f"python {install_script_path} "
                f"--packages {packages} "
                f"--build-platform {build_platform} "
                f"--sources {' '.join(sources)} "
                f"--python-version {python_version} "
                f"--conda-env-name {conda_env_name} "
                "--exclude-install conda "
                f"--output-dir {env_output_dir} "
                "--overwrite "
                f"--filename-conda {conda_filename} "
                f"--no-self"
            )

        def install_pkg_script(
            source: Literal["pip", "conda"],
        ) -> str:
            if source == "conda":
                return f"micromamba install -c ./conda_channel/ {package_names_str}"
            return f"pip uninstall -y {package_names_str}\npip install --no-deps --no-index --find-links=./wheelhouse/ --only-binary :all: {package_names_str}"

        env_output_dir = "_temp_test_env"
        conda_filename = "environment.yaml"
        install_script_path = self.get("devcontainer.feature.installer.install_py.path")
        pkg_id = self.get(".__key__").removeprefix("pypkg_")
        packages = _shlex.quote(_json.dumps([pkg_id, test_pkg_id]))
        package_names = [self.get(".name").lower(), self.get(f"pypkg_{test_pkg_id}.name").lower()]
        package_names_str = " ".join(package_names)
        oss = self.get(".os")
        python = self.get(".python")
        out = {}
        for os in oss.values():
            for source in ("pip", "conda"):
                for python_version in python["version"]["minors"]:
                    conda_env_name = (
                        f"{pkg_id}-{os['platform']}-{os['runner']}-{source}-py{python_version}"
                    )
                    out[f"{os['platform']}_{os['runner']}_{source}_py{python_version}"] = {
                        "name": f"py{python_version} | {source} | {os['name']}",
                        "runner": os["runner"],
                        "script": {
                            "install_env": install_env_script(
                                build_platform=os["platform"],
                                python_version=python_version,
                                conda_env_name=conda_env_name,
                                source=source,
                            ),
                            "install_pkg": install_pkg_script(source=source),
                            "test": f"python -m {self.get(f'pypkg_{test_pkg_id}.import_name')} --report ./report",
                        },
                        "conda_env": {
                            "name": conda_env_name,
                            "path": f"{env_output_dir}/{conda_filename}",
                        },
                        "codecov": {
                            "env": {
                                "PLATFORM": os["platform"],
                                "RUNNER": os["runner"],
                                "PYTHON": python_version,
                                "PKG_MANAGER": source,
                            }
                        },
                        "artifact_name_suffix": f" - {source} - {os['runner']} - {os['platform']} - py{python_version}",
                    }
        return out

    def binder_config_file(self, source: Literal["conda", "apt", "bash"]) -> str:
        """Create environment dependencies for binder."""
        if self._binder_files:
            return self._binder_files.get(source, "")
        package_keys = ("pypkg_main", "pypkg_test")
        package_data = {k: self.get(k) for k in package_keys}
        pkg_install_script_path = self.get("devcontainer.feature.installer.install_py.path")
        install = pkgdata.import_module_from_path(self.repo_path / pkg_install_script_path)
        _, files, self_installation_cmd = install.DependencyInstaller(package_data).run(
            packages=[package_key.removeprefix("pypkg_") for package_key in package_keys],
            build_platform="linux-64",
            target_platform="linux-64",
            # Oldest supported Python version, since repo2docker does not support brand new Python versions.
            python_version=package_data["pypkg_main"]["python"]["version"]["minors"][0],
            sources=["conda", "pip", "apt", "bash"],
            exclude_installed=False,
            path_to_repo="./",  # postBuild script is run from root directory
            indent_json=self.get("default.file_setting.json.indent"),
            indent_yaml=self.get("default.file_setting.yaml.sequence_indent_offset"),
        )
        if "bash" in files:
            files["bash"] = f"#!/bin/bash\n\n{files['bash']}"
        files["bash"] = (
            f"{files.get('bash', '').strip()}\n{_shlex.join(self_installation_cmd)}\n".lstrip()
        )
        self._binder_files = files
        return self._binder_files.get(source, "")

    def commit_labels(self) -> dict:
        """Create labels for `$.label.commit.label`."""
        out = {}
        release_commits = self.get("commit.release")
        commit_config = self.get("commit.config")
        label_prefix = self.get("label.commit.prefix")
        label_sep = self.get("label.commit.separator")
        scope_start = commit_config["scope_start"]
        scope_end = commit_config["scope_end"]
        scope_sep = commit_config["scope_separator"]
        for commit_id, commit_data in release_commits.items():
            scopes = commit_data.get("scope")
            if isinstance(scopes, str):
                scopes = [scopes]
            scope = f"{scope_start}{scope_sep.join(scopes)}{scope_end}" if scopes else ""
            label_suffix = f"{commit_data['type']}{scope}"
            out[commit_id] = {
                "suffix": label_suffix,
                "description": commit_data.get("type_description", ""),
                "name": f"{label_prefix}{label_sep}{label_suffix}",
            }
        return out

    def conda_req(self, typ: Literal["host", "run", "run_constrained"]) -> list[dict]:
        """Create requirements for conda recipe."""
        out = []
        dep_key = {"host": "build", "run": "core", "run_constrained": "optional"}[typ]
        dep_groups = self.get(f"..dependency.{dep_key}")
        if not dep_groups:
            return out
        if typ == "run_constrained":
            reqs = []
            for dep_group in dep_groups.values():
                reqs.extend(list(dep_group["package"].values()))
        else:
            reqs = dep_groups.values()
        for req in reqs:
            conda = req["install"].get("conda")
            if not conda:
                continue
            spec = [conda["channel"]]
            for part_name, part_prefix in (
                ("subdir", "/"),
                ("name", "::"),
                ("version", " "),
                ("build", " "),
            ):
                if part_name in conda:
                    spec.append(f"{part_prefix}{conda[part_name]}")
            entry = {"value": "".join(spec)}
            selector = conda.get("selector", "")
            if selector:
                entry["selector"] = selector
            out.append(entry)
        return out

    def trove_classifiers(self) -> list[str]:
        """Create trove classifiers for the package/test-suite."""

        def programming_language() -> list[str]:
            base = "Programming Language :: Python"
            return [base] + [
                f"{base} :: {version}"
                for version in ["3 :: Only", *self.get(f"{key}.python.version.minors")]
            ]

        def operating_system() -> list[str]:
            base = "Operating System :: {}"
            trove = {
                "ubuntu": "POSIX :: Linux",
                "macos": "MacOS",
                "windows": "Microsoft :: Windows",
            }
            out = [
                base.format(trove[runner_type])
                for runner_type in {
                    os["runner"].split("-")[0] for os in self.get(f"{key}.os").values()
                }
            ]
            if self.get(f"{key}.python.pure"):
                out.append(base.format("OS Independent"))
            return out

        def development_phase() -> str:
            log = self.manager.changelog.current_public
            ver = log["version"]
            phase = log.get("phase")
            if ver == "0.0.0":
                code = 1
            elif phase == "dev":
                code = 2
            elif phase == "alpha":
                code = 3
            elif phase in ("beta", "rc") or ver.startswith("0"):
                code = 4
            else:
                highest_major = max(int(version[0]) for version in self.get("project.versions"))
                code = 5 if int(ver[0]) == highest_major else 6
            code_name = {
                1: "Planning",
                2: "Pre-Alpha",
                3: "Alpha",
                4: "Beta",
                5: "Production/Stable",
                6: "Mature",
                7: "Inactive",
            }
            return f"Development Status :: {code} - {code_name[code]}"

        key = self.get(".__key__")
        out = programming_language() + operating_system() + [development_phase()]
        if self.get(f"{key}.typed"):
            out.append("Typing :: Typed")
        return sorted(out)

    def web_page(self) -> dict[str, dict[str, str]]:
        """Create `$.web.page` data."""
        path = self.repo_path / (self.ccc["web.path.source"] or self.get("web.path.source"))
        url_home = self.get("web.url.home")
        pages = {}
        blog = {}
        for md_filepath in path.rglob("*.md", case_sensitive=False):
            if not md_filepath.is_file():
                continue
            rel_path = md_filepath.relative_to(path)
            dirhtml_path = str(rel_path.with_suffix("")).removesuffix("/index")
            text = md_filepath.read_text()
            frontmatter = mdit.parse.frontmatter(text) or {}
            if "ccid" in frontmatter:
                pages[pl.string.to_slug(frontmatter["ccid"])] = {
                    "title": mdit.parse.title(text),
                    "path": dirhtml_path,
                    "url": f"{url_home}/{dirhtml_path}",
                }
            for key in ["category", "tags"]:
                val = frontmatter.get(key)
                if not val:
                    continue
                if isinstance(val, str):
                    val = [item.strip() for item in val.split(",")]
                if not isinstance(val, list):
                    logger.warning(
                        mdit.inline_container(
                            "Invalid webpage frontmatter: ",
                            mdit.element.code_span(str(rel_path)),
                        ),
                        mdit.inline_container(
                            "Invalid frontmatter value for ", mdit.element.code_span(key), " :"
                        ),
                        mdit.element.code_block(
                            ps.write.to_yaml_string(val, end_of_file_newline=False),
                            language="yaml",
                        ),
                    )
                blog.setdefault(key, []).extend(val)
        if "blog" not in pages:
            return pages
        for key, values in blog.items():
            for value in set(values):
                value_slug = pl.string.to_slug(value)
                key_singular = key.removesuffix("s")
                final_key = f"blog_{key_singular}_{value_slug}"
                if final_key in pages:
                    logger.error(
                        mdit.inline_container(
                            "Duplicate webpage ID ", mdit.element.code_span(final_key)
                        ),
                        f"Generated ID '{final_key}' already exists "
                        f"for page '{pages[final_key]['path']}'. "
                        "Please do not use `ccid` values that start with 'blog_'.",
                    )
                blog_group_path = f"{pages['blog']['path']}/{key_singular}/{value_slug}"
                pages[final_key] = {
                    "title": value,
                    "path": blog_group_path,
                    "url": f"{url_home}/{blog_group_path}",
                }
        return pages

    def file_codeowners(self) -> str:
        """Create CODEOWNERS file content."""
        data: dict[int, dict[str, list[str]]] = {}
        pattern_description: dict[str, str] = {}
        team = self.get("team")
        role = self.get("role")
        for member in team.values():
            for glob_def in member.get("ownership", []):
                data.setdefault(glob_def["priority"], {}).setdefault(glob_def["glob"], []).append(
                    member["github"]["id"]
                )
                if glob_def.get("description"):
                    pattern_description[glob_def["glob"]] = glob_def["description"]
            for member_role in member.get("role", {}):
                for glob_def in role[member_role].get("ownership", []):
                    data.setdefault(glob_def["priority"], {}).setdefault(
                        glob_def["glob"], []
                    ).append(member["github"]["id"])
                    if glob_def.get("description"):
                        pattern_description[glob_def["glob"]] = glob_def["description"]
        if not data:
            return ""
        # Get the maximum length of patterns to align the columns when writing the file
        max_len = max(
            [len(glob_pattern) for priority_dic in data.values() for glob_pattern in priority_dic]
        )
        lines = []
        for priority_defs in [defs for priority, defs in sorted(data.items())]:
            for pattern, reviewers_list in sorted(priority_defs.items()):
                comment = pattern_description.get(pattern, "")
                lines.extend([f"# {comment_line}" for comment_line in comment.splitlines()])
                reviewers = " ".join(
                    [f"@{reviewer_id}" for reviewer_id in sorted(set(reviewers_list))]
                )
                lines.append(f"{pattern: <{max_len}}   {reviewers}{'\n' if comment else ''}")
        return f"{'\n'.join(lines)}\n"

    @staticmethod
    def create_cff_person_or_entity(entity: dict) -> dict:
        """Create a CFF person or entity from a control center entity."""
        out = {}
        if entity["name"].get("legal"):
            # Entity
            out["name"] = entity["name"]["legal"]
            for in_key, out_key in (
                ("location", "location"),
                ("date_start", "date-start"),
                ("date_end", "date-end"),
            ):
                if entity.get(in_key):
                    out[out_key] = entity[in_key]
        else:
            # Person
            name = entity["name"]
            for in_key, out_key in (
                ("last", "family-names"),
                ("first", "given-names"),
                ("particle", "name-particle"),
                ("suffix", "name-suffix"),
                ("affiliation", "affiliation"),
            ):
                if name.get(in_key):
                    out[out_key] = name[in_key]
        # Common
        for contact_type, contact_key in (("orcid", "url"), ("email", "id")):
            if entity.get(contact_type):
                out[contact_type] = entity[contact_type][contact_key]
        for key in (
            "alias",
            "website",
            "tel",
            "fax",
            "address",
            "city",
            "region",
            "country",
            "post-code",
        ):
            if entity.get(key):
                out[key] = entity[key]
        return out

    def validate_codecov_yaml(self, content_src: dict, content_str: str) -> None:  # noqa: ARG002
        """Validate the Codecov configuration file."""
        try:
            # Validate the config file
            # https://docs.codecov.com/docs/codecov-yaml#validate-your-repository-yaml
            pl.http.request(
                verb="POST",
                url="https://codecov.io/validate",
                data=content_str.encode(),
            )
        except _WebAPIError as e:
            logger.error(
                "CodeCov Configuration File Validation",
                "Validation of Codecov configuration file failed.",
                str(e),
            )
        return

    def pyproject_dependency(
        self, typ: Literal["build", "core", "optional"], pkg: str | None = None
    ) -> dict | list:
        """Create PEP 508 dependencies from a control center dependency."""

        def create(pkgs: dict) -> list[str]:
            return [
                pkg["install"]["pip"]["spec"] for pkg in pkgs.values() if "pip" in pkg["install"]
            ]

        base_path = f"pypkg_{pkg}" if pkg else ""
        if typ == "optional":
            opt_deps = {}
            for opt_dep_group in self.get(f"{base_path}.dependency.optional", {}).values():
                opt_deps[opt_dep_group["name"]] = create(opt_dep_group["package"])
            return opt_deps
        return create(self.get(f"{base_path}.dependency.{typ}"))

    def pyproject_entry_points(self) -> dict[str, dict[str, str]]:
        """Create pyproject entry points from control center data."""
        entry_points = {}
        for entry_group in self.get(".entry.api", {}).values():
            entry_group_out = {}
            for entry_point in entry_group["entry"].values():
                entry_group_out[entry_point["name"]] = entry_point["ref"]
            entry_points[entry_group["name"]] = entry_group_out
        return entry_points

    def pyproject_scripts(self, typ: Literal["cli", "gui"]) -> dict[str, str]:
        """Create pyproject script from control center data."""
        scripts = {}
        for entry in self.get(f".entry.{typ}", {}).values():
            if entry["pypi"]:
                scripts[entry["name"]] = entry["ref"]
        return scripts

    @staticmethod
    def entity_in_pyproject(entity: dict) -> dict:
        """Create a PEP 621 entity from a control center entity."""
        out = {"name": entity["name"]["full"]}  # Name is always available
        if entity.get("email"):
            out["email"] = entity["email"]["id"]
        return out
