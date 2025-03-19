from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

from packaging import specifiers as _specifiers
from licenseman import spdx as _spdx
from loggerman import logger as _logger
import mdit as _mdit
import pyserials as _ps

import controlman
from controlman import data_helper as _helper
from controlman import exception as _exception
from controlman import date

if _TYPE_CHECKING:
    from gittidy import Git
    from pylinks.api import GitHub
    from pyserials.nested_dict import NestedDict
    from controlman.cache_manager import CacheManager


class MainDataGenerator:

    def __init__(
        self,
        data: NestedDict,
        cache_manager: CacheManager,
        git_manager: Git,
        github_api: GitHub,
    ):
        self._data = data
        self._git = git_manager
        self._cache = cache_manager
        self._gh_api = github_api
        self._gh_api_repo = None
        return

    def generate(self) -> None:
        self._repo()
        self._team()
        self._license()
        self._discussion_categories()
        self._package_python_versions()
        self._vars()
        return

    def _repo(self) -> None:
        repo_address = self._git.get_remote_repo_name(
            remote_name="origin",
            remote_purpose="push",
            fallback_name=False,
            fallback_purpose=False
        )
        if not repo_address:
            raise _exception.data_gen.RemoteGitHubRepoNotFoundError(
                repo_path=self._git.repo_path,
                remotes=self._git.get_remotes(),
            )
        username, repo_name = repo_address
        self._gh_api_repo = self._gh_api.user(username).repo(repo_name)
        repo_info = self._gh_api.user(username).repo(repo_name).info
        log_info = _mdit.inline_container(
            "Retrieved data for repository ",
            _mdit.element.code_span(f'{username}/{repo_name}'),
            "."
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
            f"Repository Data",
            log_info,
            repo_info_code_block,
        )
        repo_info["created_at"] = date.to_internal(date.from_github(repo_info["created_at"]))
        ccm_repo = self._data.setdefault("repo", {})
        ccm_repo["owner"] = repo_info["owner"]["login"]
        ccm_repo.update(
            {k: repo_info[k] for k in ("id", "node_id", "name", "full_name", "created_at", "default_branch")}
        )
        ccm_repo.setdefault("url", {})["home"] = repo_info["html_url"]
        self._data["team.owner.github"] = {"id": repo_info["owner"]["login"], "rest_id": repo_info["owner"]["id"]}
        return

    def _team(self) -> None:
        self._data.fill("team")
        for person_id in self._data["team"].keys():
            _helper.fill_entity(
                entity=self._data[f"team.{person_id}"],
                github_api=self._gh_api,
                cache_manager=self._cache,
            )
        return

    def _license(self):
        if not self._data["license"]:
            return
        expression = self._data.fill("license.expression")
        license_ids, license_ids_custom = _spdx.expression.license_ids(expression)
        exception_ids, exception_ids_custom = _spdx.expression.exception_ids(expression)
        for custom_ids, spdx_typ in ((license_ids_custom, "license"), (exception_ids_custom, "exception")):
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
        for custom_ids, spdx_typ in ((license_ids_custom, "license"), (exception_ids_custom, "exception")):
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
                    }
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
                source_data = self._cache.get("license", spdx_id)
                if source_data:
                    licence = class_(source_data)
                else:
                    licence = func(spdx_id)
                    self._cache.set("license", spdx_id, licence.raw_data)
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
                        "repo_text_plain": f"{self._data["repo.url.blob"]}/{path_text}",
                        "repo_header_plain": f"{self._data["repo.url.blob"]}/{path_header}" if header_xml else "",
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
        discussions_info = self._cache.get("repo", f"discussion_categories")
        if discussions_info:
            return
        if not self._gh_api.authenticated:
            _logger.notice(
                "GitHub Discussion Categories",
                "GitHub token not provided. Cannot get discussions categories."
            )
            return
        discussions_info = self._gh_api_repo.discussion_categories()
        self._cache.set("repo", f"discussions_categories", discussions_info)
        discussion = self._data.setdefault("discussion.category", {})
        for category in discussions_info:
            category_obj = discussion.setdefault(category["slug"], {})
            category_obj["id"] = category["id"]
            category_obj["name"] = category["name"]
            category_obj["emoji"] = category["emojiHTML"].removeprefix("<div>").removesuffix("</div>").strip()
            category_obj["created_at"] = date.to_internal(date.from_github(category["createdAt"]))
            category_obj["updated_at"] = date.to_internal(date.from_github(category["updatedAt"]))
            category_obj["is_answerable"] = category["isAnswerable"]
            category_obj["description"] = category["description"]
        return

    def _package_python_versions(self) -> None:

        def get_python_releases():
            release_versions = self._cache.get("python", "releases")
            if release_versions:
                return release_versions
            release_versions = self._gh_api.user("python").repo("cpython").semantic_versions(tag_prefix="v")
            live_versions = []
            for version in release_versions:
                version_tuple = tuple(map(int, version.split(".")))
                if version_tuple[0] < 2:
                    continue
                if version_tuple[0] == 2 and version_tuple[1] < 3:
                    continue
                live_versions.append(version)
            live_versions = sorted(live_versions, key=lambda x: tuple(map(int, x.split("."))))
            self._cache.set("python", "releases", live_versions)
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
            except _specifiers.InvalidSpecifier as e:
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
        var = controlman.read_variables(repo_path=self._git.repo_path)
        zenodo = self._data["zenodo"]
        if zenodo:
            if not zenodo.get("concept"):
                concept_doi = var["zenodo"]["concept"]["doi"]
                if concept_doi:
                    zenodo["concept"] = {"doi": concept_doi, "id": var["zenodo"]["concept"]["id"]}
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
    return f"{"-".join(parts[:-1])}.{parts[-1]}"
