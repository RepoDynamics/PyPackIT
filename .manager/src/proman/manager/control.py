from __future__ import annotations

import copy
import functools as _functools
import shutil as _shutil
import stat as _stat
from pathlib import Path as _Path
from typing import TYPE_CHECKING

import mdit as _mdit
import pylinks
import pyserials as _ps
from loggerman import logger as _logger
from pylinks.exception.api import WebAPIError as _WebAPIError

from controlman import data_helper as _helper
from controlman import data_validator as _data_validator
from controlman import file_gen as _file_gen
from controlman.changelog_manager import ChangelogManager
from controlman.data_generator import DataGenerator
from controlman.exception import load as _exception
from controlman.hook_manager import HookManager as _HookManager
from controlman.reporter import ControlCenterReporter as _ControlCenterReporter
from proman import const
from proman.dtype import DynamicDir, DynamicDirType, DynamicFileChangeType, DynamicFile

if TYPE_CHECKING:
    import ruamel.yaml
    from versionman.pep440_semver import PEP440SemVer

    from proman.manager import Manager
    from proman.manager.cache import CacheManager


class ControlCenterManager:
    def __init__(
        self,
        manager: Manager,
        cc_path: _Path,
        future_versions: dict[str, str | PEP440SemVer] | None = None,
        clean_state: bool = False,
    ):
        self._manager = manager
        self._git = self._manager.git

        self._path_cc = cc_path
        self._data_before: _ps.NestedDict = _ps.NestedDict() if clean_state else self._manager.data
        self._github_token = self._manager.token.github.get()
        self._github_api = self._manager.gh_api_bare
        self._future_vers = future_versions or {}

        self._path_root = self._git.repo_path

        self._hook_manager = _HookManager(
            dir_path=self._path_cc / const.DIRNAME_CC_HOOK,
            repo_path=self._git.repo_path,
            ccc=self._data_before,
            ccc_main=self._manager.main.data,
            cache_manager=self._manager.cache,
            github_token=self._github_token,
        )
        with _logger.sectioning("CCA Initialization Hooks"):
            self._hook_manager.generate(const.FUNCNAME_CC_HOOK_INIT)
        self._data_raw: _ps.NestedDict | None = None
        self._data: _ps.NestedDict | None = None
        self._files: list[DynamicFile] = []
        self._dirs: list[DynamicDir] = []
        self._dirs_to_apply: list[tuple[str, str, DynamicFileChangeType]] = []
        self._changes: list[tuple[str, DynamicFileChangeType]] = []
        return

    def load(self) -> _ps.NestedDict:
        def _load_file(filepath: _Path):
            file_content = filepath.read_text().strip()
            if not file_content:
                _logger.notice(
                    "Empty Configuration File",
                    _mdit.inline_container(
                        "The control center configuration file at ",
                        _mdit.element.code_span(str(filepath)),
                        " is empty.",
                    ),
                )
                return
            try:
                data = _ps.read.yaml_from_file(
                    path=filepath,
                    safe=True,
                    constructors={
                        const.CC_EXTENSION_TAG: self._create_external_tag_constructor(
                            tag_name=const.CC_EXTENSION_TAG,
                            cache_manager=self._manager.cache,
                            filepath=filepath,
                            file_content=file_content,
                        )
                    },
                )
            except _ps.exception.read.PySerialsInvalidDataError as e:
                raise _exception.ControlManInvalidConfigFileDataError(cause=e) from None
            try:
                log = _ps.update.recursive_update(
                    source=self._data_raw,
                    addon=data,
                )
            except _ps.exception.update.PySerialsUpdateRecursiveDataError as e:
                raise _exception.ControlManDuplicateConfigFileDataError(
                    filepath=filepath, cause=e
                ) from None
            # log_admonitions = []
            # for key, title in (
            #     ("added", "Added"),
            #     ("list_appended", "Appended List"),
            #     ("skipped", "Skipped"),
            # ):
            #     if not log[key]:
            #         continue
            #     key_list = _mdit.element.unordered_list(
            #         [_mdit.element.code_span(item) for item in sorted(log[key])]
            #     )
            #     log_admonitions.append(
            #         _mdit.element.admonition(
            #             title=f"{title} Keys",
            #             body=key_list,
            #             dropdown=True,
            #         )
            #     )
            _logger.success(
                "Loaded Configurations",
                _logger.data_block({k: [str(v) for v in value] for k, value in log.items()}),
                # _mdit.block_container(*log_admonitions),
            )
            return

        if self._data_raw:
            return self._data_raw
        with _logger.sectioning("Config Files Load"):
            self._data_raw = {}
            hook_dir = self._path_cc / const.DIRNAME_CC_HOOK
            for path in sorted(self._path_cc.rglob("*"), key=lambda p: (p.parts, p)):
                if (
                    hook_dir not in path.parents
                    and path.is_file()
                    and path.suffix.lower() in [".yaml", ".yml"]
                ):
                    with _logger.sectioning(
                        _mdit.element.code_span(str(path.relative_to(self._path_cc)))
                    ):
                        _load_file(filepath=path)
        with _logger.sectioning("CCA Load Hooks"):
            self._hook_manager.generate(const.FUNCNAME_CC_HOOK_LOAD, data=self._data_raw)
        with _logger.sectioning("Post-Load Data Validation"):
            _data_validator.validate(data=self._data_raw, source="source", before_substitution=True)
        with _logger.sectioning("CCA Load Validation Hooks"):
            self._hook_manager.generate(const.FUNCNAME_CC_HOOK_LOAD_VALID, data=self._data_raw)
        return self._data_raw

    def generate_data(self) -> _ps.NestedDict:
        if self._data:
            return self._data
        self.load()
        data = copy.deepcopy(self._data_raw)
        changelog_manager = ChangelogManager(manager=self._manager)
        code_context_call = {"changelog": changelog_manager}
        data["changelogs"] = changelog_manager.changelogs
        data["contributor"] = changelog_manager.contributor.as_dict
        inline_hooks = self._hook_manager.inline_hooks
        if inline_hooks:
            code_context_call["hook"] = inline_hooks.Hooks(manager=self._manager)

        def get_prefix(get, prefix: str):
            return [get(key) for key in data.keys() if key.startswith(prefix)]

        data = _ps.NestedDict(
            data,
            code_context={
                "manager": self._manager,
                "repo_path": self._path_root,
                "ccc_main": self._manager.main.data,
                "ccc": self._data_before,
                "cache_manager": self._manager.cache,
                "slugify": pylinks.string.to_slug,
            },
            code_context_partial={
                "team_members_with_role_types": _helper.team_members_with_role_types,
                "team_members_without_role_types": _helper.team_members_without_role_types,
                "team_members_with_role_ids": _helper.team_members_with_role_ids,
                "get_prefix": get_prefix,
            },
            code_context_call=code_context_call,
            relative_template_keys=const.RELATIVE_TEMPLATE_KEYS,
            relative_key_key="__key__",
        )

        with _logger.sectioning("Dynamic Data Generation"):
            DataGenerator(
                data=data,
                manager=self._manager,
                data_main=self._manager.main.data,
                future_versions=self._future_vers,
            ).generate()
        with _logger.sectioning("CCA Augmentation Hooks"):
            self._hook_manager.generate(
                const.FUNCNAME_CC_HOOK_AUGMENT,
                data,
            )
        with _logger.sectioning("Post-Generation Data Validation"):
            # Validate again to fill default values that depend on generated data
            # Example: A key may be referencing `team.owner.email.url`, which has a default
            # value based on `team.owner.email.id`. But since `team.owner` is generated
            # dynamically, the default value for `team.owner.email.url` is not set in the initial validation.
            _data_validator.validate(data=data(), source="source", before_substitution=True)
        with _logger.sectioning("CCA Augmentation Validation Hooks"):
            self._hook_manager.generate(
                const.FUNCNAME_CC_HOOK_AUGMENT_VALID,
                data,
            )
        with _logger.sectioning("Template Resolution"):
            data.fill()
            _logger.success(
                "Filled Data",
                "All template variables have been successfully resolved.",
            )
            data.pop("var")
            data.pop("changelogs")
            data.pop("contributor")
        with _logger.sectioning("CCA Templating Hooks"):
            self._hook_manager.generate(
                const.FUNCNAME_CC_HOOK_TEMPLATE,
                data,
            )
        data = _ps.NestedDict(_ps.update.remove_keys(data(), const.RELATIVE_TEMPLATE_KEYS))
        with _logger.sectioning("Final Data Validation"):
            _data_validator.validate(data=data(), source="source")
        with _logger.sectioning("CCA Templating Validation Hooks"):
            self._hook_manager.generate(
                const.FUNCNAME_CC_HOOK_TEMPLATE_VALID,
                data,
            )
        self._data = data
        self._manager.cache.save()
        return self._data

    def generate_files(self) -> list[DynamicFile]:
        if self._files:
            return self._files
        self.generate_data()
        with _logger.sectioning("Dynamic File Generation"):
            self._files = _file_gen.generate(
                manager=self._manager,
                data=self._data,
                data_before=self._data_before,
                repo_path=self._path_root,
            )
        return self._files

    def compare(self):
        if self._changes and self._files and self._dirs:
            return self._changes, self._files, self._dirs
        files = self.generate_files()
        metadata_changes = _ps.compare.items(
            source=self._data(), target=self._data_before(), path=""
        )
        all_paths = []
        for change_type in ("removed", "added", "modified"):
            for changed_key in metadata_changes[change_type]:
                all_paths.append((changed_key, DynamicFileChangeType[change_type.upper()]))
        self._changes = all_paths
        dirs = self._compare_dirs()
        with _logger.sectioning("CCA Output Generation Hooks"):
            self._hook_manager.generate(
                const.FUNCNAME_CC_HOOK_OUTPUT,
                data=self._data,
                files=self._files,
                dirs=dirs,
            )
        return self._changes, files, dirs

    def report(self) -> _ControlCenterReporter:
        self.compare()
        return _ControlCenterReporter(
            metadata=self._changes,
            files=self._files,
            dirs=self._dirs,
        )

    def apply_changes(self) -> None:
        """Apply changes to dynamic repository files."""
        generated_files = self.generate_files()
        self._compare_dirs()
        for dir_path, dir_path_before, status in self._dirs_to_apply:
            dir_path_abs = self._path_root / dir_path if dir_path else None
            dir_path_before_abs = self._path_root / dir_path_before if dir_path_before else None
            if status is DynamicFileChangeType.REMOVED:
                _shutil.rmtree(dir_path_before_abs)
            elif status is DynamicFileChangeType.MOVED:
                _shutil.move(dir_path_before_abs, dir_path_abs)
            elif status is DynamicFileChangeType.ADDED:
                dir_path_abs.mkdir(parents=True, exist_ok=True)
        for generated_file in generated_files:
            filepath_abs = self._path_root / generated_file.path if generated_file.path else None
            filepath_before_abs = (
                self._path_root / generated_file.path_before if generated_file.path_before else None
            )
            if generated_file.change in (
                DynamicFileChangeType.REMOVED,
                DynamicFileChangeType.MOVED,
                DynamicFileChangeType.MOVED_MODIFIED,
            ):
                filepath_before_abs.unlink(missing_ok=True)
            if generated_file.change in (
                DynamicFileChangeType.ADDED,
                DynamicFileChangeType.MODIFIED,
                DynamicFileChangeType.MOVED_MODIFIED,
                DynamicFileChangeType.MOVED,
            ):
                filepath_abs.parent.mkdir(parents=True, exist_ok=True)
                with open(filepath_abs, "w") as f:
                    f.write(f"{generated_file.content.strip()}\n")
                if generated_file.executable:
                    filepath_abs.chmod(
                        filepath_abs.stat().st_mode | _stat.S_IXUSR | _stat.S_IXGRP | _stat.S_IXOTH
                    )
        self._apply_duplicates()
        with _logger.sectioning("CCA Synchronization Hooks"):
            self._hook_manager.generate(const.FUNCNAME_CC_HOOK_SYNC)
        return

    def _apply_duplicates(self):
        for key, duplicate in self._data_before.items():
            if not key.startswith("copy_"):
                continue
            if "source" in duplicate:
                for destination in duplicate["destinations"]:
                    self._path_root.joinpath(destination).unlink(missing_ok=True)
            else:
                for source_glob in duplicate["sources"]:
                    for source in self._path_root.glob(source_glob):
                        for destination in duplicate["destinations"]:
                            self._path_root.joinpath(destination).joinpath(
                                _Path(source).stem
                            ).unlink(missing_ok=True)
        for key, duplicate in self._data.items():
            if not key.startswith("copy_"):
                continue
            if "source" in duplicate:
                for destination in duplicate["destinations"]:
                    _shutil.copy2(
                        self._path_root.joinpath(duplicate["source"]),
                        self._path_root.joinpath(destination),
                    )
            else:
                for source_glob in duplicate["sources"]:
                    for source in self._path_root.glob(source_glob):
                        for destination in duplicate["destinations"]:
                            destination_path = self._path_root.joinpath(destination).joinpath(
                                _Path(source).stem
                            )
                            destination_path.parent.mkdir(parents=True, exist_ok=True)
                            _shutil.copy2(self._path_root.joinpath(source), destination_path)
        return

    def _compare_dirs(self):
        def compare_source(main_key: str, root_path: str, root_path_before: str):
            source_name, source_name_before = self._get_dirpath(f"{main_key}.path.source_rel")
            source_path = f"{root_path}/{source_name}" if root_path else None
            source_path_before_real = (
                f"{root_path_before}/{source_name_before}"
                if root_path_before and source_name_before
                else None
            )
            change = self._compare_dir_paths(source_path, source_path_before_real)
            source_path_before = (
                f"{root_path}/{source_name_before}" if root_path and source_name_before else None
            )
            return source_path, source_path_before, source_path_before_real, change

        def compare_import(
            main_key: str, source_path: str, source_path_before: str, source_path_before_real: str
        ):
            import_name, import_name_before = self._get_dirpath(f"{main_key}.import_name")
            import_path = f"{source_path}/{import_name}" if source_path and import_name else None
            import_path_before_real = (
                f"{source_path_before_real}/{import_name_before}"
                if source_path_before_real and import_name_before
                else None
            )
            change = self._compare_dir_paths(import_path, import_path_before_real)
            import_path_before = (
                f"{source_path}/{import_name_before}"
                if source_path and import_name_before
                else None
            )
            return import_path, import_path_before, import_path_before_real, change

        if self._dirs:
            return self._dirs
        dirs = []
        to_apply = []
        for path_key in ("control",):
            path, path_before, status = self._compare_dir(f"{path_key}.path")
            dirs.append(
                DynamicDir(
                    type=DynamicDirType[path_key.upper()],
                    path=path,
                    path_before=path_before,
                    change=status,
                )
            )
            to_apply.append((path, path_before, status))

        for path_key, value in self._data.items():
            if not path_key.startswith("pypkg_"):
                continue

            root_path, root_path_before, root_status = self._compare_dir(f"{path_key}.path.root")
            dirs.append(
                DynamicDir(
                    type=DynamicDirType.PKG_ROOT,
                    path=root_path,
                    path_before=root_path_before,
                    change=root_status,
                )
            )
            to_apply.append((root_path, root_path_before, root_status))

            source_path, source_path_before, source_path_before_real, source_change = (
                compare_source(
                    main_key=path_key, root_path=root_path, root_path_before=root_path_before
                )
            )
            dirs.append(
                DynamicDir(
                    type=DynamicDirType.PKG_SRC,
                    path=source_path,
                    path_before=source_path_before_real,
                    change=source_change,
                )
            )
            to_apply.append((source_path, source_path_before, source_change))

            import_path, import_path_before, import_path_before_real, import_change = (
                compare_import(
                    main_key=path_key,
                    source_path=source_path,
                    source_path_before=source_path_before,
                    source_path_before_real=source_path_before_real,
                )
            )
            dirs.append(
                DynamicDir(
                    type=DynamicDirType.PKG_IMPORT,
                    path=import_path,
                    path_before=import_path_before_real,
                    change=import_change,
                )
            )
            to_apply.append((import_path, import_path_before, import_change))
        self._dirs = dirs
        self._dirs_to_apply = to_apply
        return self._dirs

    def _compare_dir(self, path_key: str) -> tuple[str, str, DynamicFileChangeType]:
        path, path_before = self._get_dirpath(path_key)
        return path, path_before, self._compare_dir_paths(path, path_before)

    def _get_dirpath(self, path_key: str) -> tuple[str, str]:
        path = self._data[path_key]
        path_before = self._data_before[path_key]
        return path, path_before

    def _compare_dir_paths(self, path, path_before) -> DynamicFileChangeType:
        path_before_exists = (self._path_root / path_before).is_dir() if path_before else False
        if path and path_before_exists:
            status = (
                DynamicFileChangeType.UNCHANGED
                if path == path_before
                else DynamicFileChangeType.MOVED
            )
        elif not path and not path_before_exists:
            status = DynamicFileChangeType.DISABLED
        elif path_before_exists:
            status = DynamicFileChangeType.REMOVED
        else:
            path_exists = (self._path_root / path).is_dir()
            status = DynamicFileChangeType.UNCHANGED if path_exists else DynamicFileChangeType.ADDED
        return status

    @staticmethod
    def _create_external_tag_constructor(
        filepath: _Path,
        file_content: str,
        tag_name: str = "!ext",
        cache_manager: CacheManager | None = None,
    ):
        def load_external_data(loader: ruamel.yaml.SafeConstructor, node: ruamel.yaml.ScalarNode):
            tag_value = loader.construct_scalar(node)
            if not tag_value:
                raise _exception.ControlManEmptyTagInConfigFileError(
                    filepath=filepath,
                    data=file_content,
                    node=node,
                )
            if cache_manager:
                cached_data = cache_manager.get(typ="extension", key=tag_value)
                if cached_data:
                    return cached_data
            url, *jsonpath_expr = tag_value.split(" ", 1)
            file_ext = url.split(".")[-1].lower()
            try:
                data_raw_whole = pylinks.http.request(
                    url=url,
                    verb="GET",
                    response_type="str",
                )
            except _WebAPIError as e:
                raise _exception.ControlManUnreachableTagInConfigFileError(
                    filepath=filepath,
                    data=file_content,
                    node=node,
                    url=url,
                    cause=e,
                ) from None
            if file_ext == "json":
                data = _ps.read.json_from_string(data=data_raw_whole, strict=False)
            elif file_ext in ("yaml", "yml"):
                data = _ps.read.yaml_from_string(
                    data=data_raw_whole,
                    safe=True,
                    constructors={tag_name: load_external_data},
                )
            elif file_ext == "toml":
                data = _ps.read.toml_from_string(data=data_raw_whole, as_dict=True)
            else:
                raise ValueError(f"Invalid file extension {file_ext} for URL {url}")
            if jsonpath_expr:
                try:
                    data = _ps.update.TemplateFiller().fill(
                        data=data,
                        template=jsonpath_expr,
                    )
                except Exception:
                    raise ValueError(
                        f"No match found for JSONPath '{jsonpath_expr}' in the JSON data from '{url}'"
                    )
            if cache_manager:
                cache_manager.set(typ="extension", key=tag_value, value=data)
            return data

        return load_external_data
