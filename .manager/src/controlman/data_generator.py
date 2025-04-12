from __future__ import annotations as _annotations

import re as _re
from typing import TYPE_CHECKING as _TYPE_CHECKING

import jinja2 as _jinja2
import mdit as _mdit
import pyserials as _ps
from licenseman import spdx as _spdx
from loggerman import logger as _logger
from packaging import specifiers as _specifiers
from versionman import pep440_semver as _ver

from controlman import exception as _exception
from proman.util import date

if _TYPE_CHECKING:
    from pyserials.nested_dict import NestedDict
    from versionman.pep440_semver import PEP440SemVer

    from proman.manager import Manager


class DataGenerator:
    def __init__(
        self,
        data: NestedDict,
        manager: Manager,
        data_main: _ps.NestedDict,
        future_versions: dict[str, str | PEP440SemVer] | None = None,
    ):
        self._manager = manager
        self._data = data
        self._data_main = data_main
        self._git = self._manager.git
        self._future_versions = future_versions or {}
        return

    def generate(self) -> None:
        self._repo()
        self._team()
        self._license()
        self._discussion_categories()
        self._package_python_versions()
        self._vars()
        self._package_releases()
        self._repo_labels()
        return

    def _repo(self) -> None:
        repo_info = self._manager.gh_api_actions.info
        repo_fullname = (
            f"{self._manager.gh_api_actions.username}/{self._manager.gh_api_actions.name}"
        )
        log_info = _mdit.inline_container(
            "Retrieved data for repository ",
            _mdit.element.code_span(repo_fullname),
            ".",
        )
        if "source" in repo_info:
            repo_info = repo_info["source"]
            log_info.extend(
                "The repository is a fork and thus the target is set to ",
                _mdit.element.code_span(repo_info["full_name"]),
            )
        repo_info_code_block = _mdit.element.code_block(
            content=_ps.write.to_yaml_string(repo_info),
            language="yaml",
            caption="GitHub API Response",
        )
        _logger.info(
            "Repository Data",
            log_info,
            repo_info_code_block,
        )
        repo_info["created_at"] = date.to_internal(date.from_github(repo_info["created_at"]))
        ccm_repo = self._data.setdefault("repo", {})
        ccm_repo["owner"] = repo_info["owner"]["login"]
        ccm_repo.update(
            {
                k: repo_info[k]
                for k in ("id", "node_id", "name", "full_name", "created_at", "default_branch")
            }
        )
        ccm_repo.setdefault("url", {})["home"] = repo_info["html_url"]
        self._data["team.owner.github"] = {
            "id": repo_info["owner"]["login"],
            "rest_id": repo_info["owner"]["id"],
        }
        return

    def _team(self) -> None:
        self._data.fill("team")
        for person_id in self._data["team"].keys():
            self._manager.user.fill_entity(
                entity=self._data[f"team.{person_id}"],
                github_api=self._manager.gh_api_bare,
                cache_manager=self._manager.cache,
            )
        return

    def _license(self):
        if not self._data["license"]:
            return
        expression = self._data.fill("license.expression")
        license_ids, license_ids_custom = _spdx.expression.license_ids(expression)
        exception_ids, exception_ids_custom = _spdx.expression.exception_ids(expression)
        for custom_ids, spdx_typ in (
            (license_ids_custom, "license"),
            (exception_ids_custom, "exception"),
        ):
            for custom_id in custom_ids:
                if custom_id not in self._data["license.component"]:
                    raise _exception.load.ControlManSchemaValidationError(
                        source="source",
                        problem=f"Custom {spdx_typ} '{custom_id}' not found at `$.license.component`.",
                        json_path="license.expression",
                        data=self._data(),
                    )
        all_ids = license_ids + exception_ids + license_ids_custom + exception_ids_custom
        for component_id, component_data in self._data.get("license.component", {}).items():
            if component_id not in all_ids:
                raise _exception.load.ControlManSchemaValidationError(
                    source="source",
                    problem=(
                        f"License component '{component_id}' defined at `$.license.component` "
                        f"is not part of the license expression at `$.license.expression`."
                    ),
                    json_path=f"license.component.{component_id}",
                    data=self._data(),
                )
        for custom_ids, spdx_typ in (
            (license_ids_custom, "license"),
            (exception_ids_custom, "exception"),
        ):
            for custom_id in custom_ids:
                user_data = self._data.setdefault("license.component", {}).setdefault(custom_id, {})
                user_data_path = user_data.setdefault("path", {})
                out_data = {
                    "type": spdx_typ,
                    "custom": True,
                    "id": custom_id,
                    "path": {
                        "text_plain": normalize_license_filename(
                            user_data_path.get("text_plain", f"LICENSE-{custom_id}.md")
                        ),
                        "header_plain": normalize_license_filename(
                            user_data_path.get("header_plain", f"COPYRIGHT-{custom_id}.md")
                        ),
                    },
                }
                user_data.update(out_data)
        for spdx_ids, spdx_typ in ((license_ids, "license"), (exception_ids, "exception")):
            func = _spdx.license if spdx_typ == "license" else _spdx.exception
            class_ = _spdx.SPDXLicense if spdx_typ == "license" else _spdx.SPDXLicenseException
            for spdx_id in spdx_ids:
                user_data = self._data.setdefault("license.component", {}).setdefault(spdx_id, {})
                user_data_path = user_data.setdefault("path", {})
                path_text = normalize_license_filename(
                    user_data_path.get("text_plain", f"LICENSE-{spdx_id}.md")
                )
                path_header = normalize_license_filename(
                    user_data_path.get("header_plain", f"COPYRIGHT-{spdx_id}.md")
                )
                source_data = self._manager.cache.get("license", spdx_id)
                if source_data:
                    licence = class_(source_data)
                else:
                    licence = func(spdx_id)
                    self._manager.cache.set("license", spdx_id, licence.raw_data)
                header_xml = (licence.header_xml_str or "") if spdx_typ == "license" else ""
                out_data = {
                    "type": spdx_typ,
                    "custom": False,
                    "id": licence.id,
                    "name": licence.name,
                    "reference_num": licence.reference_number,
                    "osi_approved": getattr(licence, "osi_approved", False),
                    "fsf_libre": getattr(licence, "fsf_libre", False),
                    "url": {
                        "reference": licence.url_reference,
                        "json": licence.url_json,
                        "cross_refs": licence.url_cross_refs,
                        "repo_text_plain": f"{self._data['repo.url.blob']}/{path_text}",
                        "repo_header_plain": f"{self._data['repo.url.blob']}/{path_header}"
                        if header_xml
                        else "",
                    },
                    "version_added": licence.version_added or "",
                    "deprecated": licence.deprecated,
                    "version_deprecated": licence.version_deprecated or "",
                    "obsoleted_by": licence.obsoleted_by or [],
                    "alts": licence.alts or {},
                    "optionals": licence.optionals_xml_str or [],
                    "comments": licence.comments or "",
                    "trove_classifier": _spdx.trove_classifier(licence.id) or "",
                    "text_xml": licence.text_xml_str,
                    "header_xml": header_xml,
                }
                user_data_path |= {  # Overwrite with normalized paths
                    "text_plain": path_text,
                    "header_plain": path_header if header_xml else "",
                }
                _ps.update.recursive_update(
                    source=user_data,
                    addon=out_data,
                )
        return

    def _discussion_categories(self):
        discussions_info = self._manager.cache.get("repo", "discussion_categories")
        if not discussions_info:
            if not self._manager.gh_api_bare.authenticated:
                _logger.notice(
                    "GitHub Discussion Categories",
                    "GitHub token not provided. Cannot get discussions categories.",
                )
                return
            discussions_info = self._manager.gh_api_actions.discussion_categories()
            self._manager.cache.set("repo", "discussion_categories", discussions_info)
        discussion = self._data.setdefault("discussion.category", {})
        for category in discussions_info:
            category_obj = discussion.setdefault(category["slug"], {})
            category_obj["id"] = category["id"]
            category_obj["name"] = category["name"]
            category_obj["emoji"] = (
                category["emojiHTML"].removeprefix("<div>").removesuffix("</div>").strip()
            )
            category_obj["created_at"] = date.to_internal(date.from_github(category["createdAt"]))
            category_obj["updated_at"] = date.to_internal(date.from_github(category["updatedAt"]))
            category_obj["is_answerable"] = category["isAnswerable"]
            category_obj["description"] = category["description"]
        return

    def _package_python_versions(self) -> None:
        def get_python_releases():
            release_versions = self._manager.cache.get("python", "releases")
            if release_versions:
                return release_versions
            release_versions = (
                self._manager.gh_api_bare.user("python")
                .repo("cpython")
                .semantic_versions(tag_prefix="v")
            )
            live_versions = []
            for version in release_versions:
                version_tuple = tuple(map(int, version.split(".")))
                if version_tuple[0] < 2:
                    continue
                if version_tuple[0] == 2 and version_tuple[1] < 3:
                    continue
                live_versions.append(version)
            live_versions = sorted(live_versions, key=lambda x: tuple(map(int, x.split("."))))
            self._manager.cache.set("python", "releases", live_versions)
            return live_versions

        current_python_versions = get_python_releases()

        for pkg_key, pkg in self._data.items():
            if not pkg_key.startswith("pypkg_"):
                continue
            python_ver_key = f"{pkg_key}.python.version"
            version_spec_key = f"{python_ver_key}.spec"
            spec_str = self._data.fill(version_spec_key)
            if not spec_str:
                _exception.load.ControlManSchemaValidationError(
                    source="source",
                    before_substitution=True,
                    problem="The package has not specified a Python version specifier.",
                    json_path=version_spec_key,
                    data=self._data(),
                )
            try:
                spec = _specifiers.SpecifierSet(spec_str)
            except _specifiers.InvalidSpecifier:
                raise _exception.load.ControlManSchemaValidationError(
                    source="source",
                    before_substitution=True,
                    problem=f"Invalid Python version specifier '{spec_str}'.",
                    json_path=version_spec_key,
                    data=self._data(),
                ) from None

            micro_str = []
            minor_str = []
            for compat_ver_micro_str in spec.filter(current_python_versions):
                micro_str.append(compat_ver_micro_str)
                compat_ver_micro_int = tuple(map(int, compat_ver_micro_str.split(".")))
                compat_ver_minor_str = ".".join(map(str, compat_ver_micro_int[:2]))
                if compat_ver_minor_str in minor_str:
                    continue
                minor_str.append(compat_ver_minor_str)

            if len(micro_str) == 0:
                raise _exception.load.ControlManSchemaValidationError(
                    source="source",
                    before_substitution=True,
                    problem=f"The Python version specifier '{spec_str}' does not match any "
                    f"released Python version: '{current_python_versions}'.",
                    json_path=version_spec_key,
                    data=self._data(),
                )
            output = {
                "micros": sorted(micro_str, key=lambda x: tuple(map(int, x.split(".")))),
                "minors": sorted(minor_str, key=lambda x: tuple(map(int, x.split(".")))),
            }
            self._data[python_ver_key].update(output)
        return

    def _vars(self):
        var = self._manager.variable
        zenodo = self._data["zenodo"]
        if zenodo:
            if not zenodo.get("concept"):
                concept_doi = var["zenodo"]["concept"]["doi"]
                if concept_doi:
                    zenodo["concept"] = {"doi": concept_doi, "id": var["zenodo"]["concept"]["id"]}
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
        try:
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
                    if branch == main_branch:
                        ver = _ver.PEP440SemVer("0.0.0")
                    else:
                        _logger.warning(
                            f"Failed to get latest version from branch '{branch}'; skipping branch."
                        )
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
                        _logger.warning(
                            f"Failed to read metadata from branch '{branch}'; skipping branch."
                        )
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
                        package_man_name
                        for platform_name, package_man_name in (("pypi", "pip"), ("conda", "conda"))
                        if platform_name in pkg_info
                    ]
                    if branch == curr_branch:
                        branch_metadata.fill("pypkg_main.entry")
                        branch_metadata.fill("pypkg_test.entry")
                    version_info |= {
                        "python_versions": branch_metadata["pypkg_main.python.version.minors"],
                        "os_names": [
                            os["name"] for os in branch_metadata["pypkg_main.os"].values()
                        ],
                        "package_managers": package_managers,
                        "python_api_names": [
                            script["name"]
                            for script in branch_metadata.get(
                                "pypkg_main.entry.python", {}
                            ).values()
                        ],
                        "test_python_api_names": [
                            script["name"]
                            for script in branch_metadata.get(
                                "pypkg_test.entry.python", {}
                            ).values()
                        ],
                        "cli_names": [
                            script["name"]
                            for script in branch_metadata.get("pypkg_main.entry.cli", {}).values()
                        ],
                        "test_cli_names": [
                            script["name"]
                            for script in branch_metadata.get("pypkg_test.entry.cli", {}).values()
                        ],
                        "gui_names": [
                            script["name"]
                            for script in branch_metadata.get("pypkg_main.entry.gui", {}).values()
                        ],
                        "test_gui_names": [
                            script["name"]
                            for script in branch_metadata.get("pypkg_test.entry.gui", {}).values()
                        ],
                        "api_names": [
                            script["name"]
                            for group in branch_metadata.get("pypkg_main.entry.api", {}).values()
                            for script in group["entry"].values()
                        ],
                    }
                release_info[str(ver)] = version_info
        finally:
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
                    key=lambda x: x
                    if key not in ("python_versions", "versions")
                    else _ver.PEP440SemVer(f"{x}.0" if key == "python_versions" else x),
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
            prefix = label_data["prefix"]
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


def normalize_license_filename(filename: str) -> str:
    """Normalize a license filename.

    Check whether the filename has more than one period,
    and if it does, replace all but the last period with a hyphen.
    This is done because GitHub doesn't recognize license files that have more than one period.
    """
    parts = filename.split(".")
    if len(parts) <= 2:
        return filename
    return f"{'-'.join(parts[:-1])}.{parts[-1]}"
