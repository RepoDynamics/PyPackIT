import re as _re

import jinja2 as _jinja2
from gittidy import Git as _Git
from versionman import pep440_semver as _ver
from loggerman import logger as _logger
import pyserials as _ps

import controlman as _controlman
from controlman import exception as _exception


class RepoDataGenerator:

    def __init__(
        self,
        data: _ps.NestedDict,
        git_manager: _Git,
        data_main: _ps.NestedDict | None = None,
        future_versions: dict[str, str | _ver.PEP440SemVer] | None = None,
    ):
        self._data = data
        self._data_main = data_main
        self._git = git_manager
        self._future_versions = future_versions or {}
        return

    def generate(self):
        self._package_releases()
        self._repo_labels()
        return

    def _package_releases(self) -> None:
        curr_branch, other_branches = self._git.get_all_branch_names()
        main_branch = self._data["repo.default_branch"]
        release_prefix, pre_release_prefix = allowed_prefixes = tuple(
            self._data_main[f"branch.{group_name}.name"] for group_name in ["release", "pre"]
        )
        branch_pattern = _re.compile(rf"^({release_prefix}|{pre_release_prefix}|{main_branch})")
        self._git.fetch_remote_branches_by_pattern(branch_pattern=branch_pattern)
        ver_tag_prefix = self._data_main.fill("tag.version.prefix")
        branches = other_branches + [curr_branch]
        release_info: dict = {}
        curr_branch_latest_version = None
        self._git.stash()
        for branch in branches:
            if not (branch.startswith(allowed_prefixes) or branch == main_branch):
                continue
            self._git.checkout(branch)
            if self._future_versions.get(branch):
                ver = _ver.PEP440SemVer(str(self._future_versions[branch]))
            else:
                ver = _ver.latest_version_from_tags(
                    tags=self._git.get_tags(),
                    version_tag_prefix=ver_tag_prefix,
                )
            if not ver:
                _logger.warning(f"Failed to get latest version from branch '{branch}'; skipping branch.")
                continue
            if branch == curr_branch:
                branch_metadata = self._data
                curr_branch_latest_version = ver
            elif branch == main_branch:
                branch_metadata = self._data_main
            else:
                try:
                    branch_metadata = _controlman.from_json_file(repo_path=self._git.repo_path)
                except _exception.ControlManException as e:
                    _logger.warning(f"Failed to read metadata from branch '{branch}'; skipping branch.")
                    _logger.debug("Error Details", e)
                    continue
            if branch == main_branch:
                branch_name = self._data.fill("branch.main.name")
            elif branch.startswith(release_prefix):
                new_prefix = self._data.fill("branch.release.name")
                branch_name = f"{new_prefix}{branch.removeprefix(release_prefix)}"
            else:
                new_prefix = self._data.fill("branch.pre.name")
                branch_name = f"{new_prefix}{branch.removeprefix(pre_release_prefix)}"
            version_info = {"branch": branch_name}
            pkg_info = branch_metadata["pypkg_main"]
            if pkg_info:
                package_managers = [
                    package_man_name for platform_name, package_man_name in (
                        ("pypi", "pip"), ("conda", "conda")
                    ) if platform_name in pkg_info
                ]
                if branch == curr_branch:
                    branch_metadata.fill("pypkg_main.entry")
                    branch_metadata.fill("pypkg_test.entry")
                version_info |= {
                    "python_versions": branch_metadata["pypkg_main.python.version.minors"],
                    "os_names": [os["name"] for os in branch_metadata["pypkg_main.os"].values()],
                    "package_managers": package_managers,
                    "python_api_names": [
                        script["name"] for script in branch_metadata.get("pypkg_main.entry.python", {}).values()
                    ],
                    "test_python_api_names": [
                        script["name"] for script in branch_metadata.get("pypkg_test.entry.python", {}).values()
                    ],
                    "cli_names": [
                        script["name"] for script in branch_metadata.get("pypkg_main.entry.cli", {}).values()
                    ],
                    "test_cli_names": [
                        script["name"] for script in branch_metadata.get("pypkg_test.entry.cli", {}).values()
                    ],
                    "gui_names": [
                        script["name"] for script in branch_metadata.get("pypkg_main.entry.gui", {}).values()
                    ],
                    "test_gui_names": [
                        script["name"] for script in branch_metadata.get("pypkg_test.entry.gui", {}).values()
                    ],
                    "api_names": [
                        script["name"]
                        for group in branch_metadata.get("pypkg_main.entry.api", {}).values()
                        for script in group["entry"].values()
                    ]
                }
            release_info[str(ver)] = version_info
        self._git.checkout(curr_branch)
        self._git.stash_pop()
        out = {"version": release_info, "versions": [], "branches": [], "interfaces": []}
        for version, version_info in release_info.items():
            out["versions"].append(version)
            out["branches"].append(version_info["branch"])
            for info_key, info in version_info.items():
                if info_key != "branch":
                    out.setdefault(info_key, []).extend(info)
        for key, val in out.items():
            if key != "version":
                out[key] = sorted(
                    set(val),
                    key=lambda x: x if key not in ("python_versions", "versions") else _ver.PEP440SemVer(f"{x}.0" if key == "python_versions" else x),
                    reverse=key in ("python_versions", "versions"),
                )
        for key, title in (
            ("python_api_names", "Python API"),
            ("api_names", "Plugin API"),
            ("gui_names", "GUI"),
            ("cli_names", "CLI"),
        ):
            if key in out:
                out["interfaces"].append(key.removesuffix("_names").upper())
                if key in ("gui_names", "cli_names"):
                    out["has_scripts"] = True
        self._data["project"] = out
        return

    def _repo_labels(self) -> None:
        for autogroup_name, release_key in (("version", "versions"), ("branch", "branches")):
            label_data = self._data[f"label.{autogroup_name}"]
            if not label_data:
                continue
            entries = self._data.get(f"project.{release_key}", [])
            labels = label_data["label"] = {}
            prefix = label_data['prefix']
            separator = label_data["separator"]
            for entry in entries:
                labels[entry] = {
                    "suffix": entry,
                    # "name": f"{prefix}{separator}{entry}",
                    "description": _jinja2.Template(label_data["description"]).render(
                        {autogroup_name: entry}
                    ),
                }
        return
