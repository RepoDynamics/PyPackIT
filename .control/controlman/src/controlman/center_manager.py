from pathlib import Path as _Path
import shutil as _shutil
import functools as _functools
import re as _re
import stat as _stat

import controlman
from versionman.pep440_semver import PEP440SemVer as _PEP440SemVer
import pylinks as _pylinks
import pyserials as _ps
from gittidy import Git as _Git
from loggerman import logger as _logger

from controlman import data_gen as _data_gen
from controlman.hook_manager import HookManager as _HookManager
from controlman.datatype import (
    DynamicFileChangeType,
    DynamicDirType,
    DynamicFile as _GeneratedFile,
    DynamicDir as _DynamicDir,
)
from controlman import const
from controlman.exception import load as _load_exception
from controlman.cache_manager import CacheManager
from controlman import file_gen as _file_gen
from controlman import data_loader as _data_loader
from controlman import data_validator as _data_validator
from controlman.reporter import ControlCenterReporter as _ControlCenterReporter
from controlman.changelog_manager import ChangelogManager
from controlman import data_helper as _helper


class CenterManager:

    def __init__(
        self,
        git_manager: _Git,
        cc_path: _Path,
        data_before: _ps.NestedDict,
        data_main: _ps.NestedDict,
        github_token: str | None = None,
        future_versions: dict[str, str | _PEP440SemVer] | None = None,
    ):
        self._git: _Git = git_manager
        self._path_cc = cc_path
        self._data_before: _ps.NestedDict = data_before
        self._data_main: _ps.NestedDict = data_main
        self._github_token = github_token
        self._github_api = _pylinks.api.github(token=github_token)
        self._future_vers = future_versions or {}

        self._path_root = self._git.repo_path
        relpath_local_cache = self._data_before.get("local.cache.path")
        path_local_cache = None
        retention_hours = self._data_before.get("control.cache.retention_hours", {})
        if relpath_local_cache:
            path_local_cache = self._path_root / relpath_local_cache
            path_local_config = path_local_cache / const.FILENAME_LOCAL_CONFIG
            if path_local_config.is_file():
                with _logger.sectioning("Local Cache Configuration"):
                    try:
                        local_config = _ps.read.yaml_from_file(path=path_local_config, safe=True)
                    except _ps.exception.read.PySerialsInvalidDataError as e:
                        raise _load_exception.ControlManInvalidConfigFileDataError(cause=e) from None
                    _data_validator.validate(data=local_config, schema="local")
                    retention_hours = local_config.get("retention_hours", {})
        self._cache_manager: CacheManager = CacheManager(
            path_local_cache=path_local_cache,
            retention_hours=retention_hours,
        )
        self._hook_manager = _HookManager(
            dir_path=self._path_cc / const.DIRNAME_CC_HOOK,
            repo_path=self._git.repo_path,
            ccc=self._data_before,
            ccc_main=self._data_main,
            cache_manager=self._cache_manager,
            github_token=self._github_token,
        )
        with _logger.sectioning("CCA Initialization Hooks"):
            self._hook_manager.generate(const.FUNCNAME_CC_HOOK_INIT)
        self._data_raw: _ps.NestedDict | None = None
        self._data: _ps.NestedDict | None = None
        self._files: list[_GeneratedFile] = []
        self._dirs: list[_DynamicDir] = []
        self._dirs_to_apply: list[tuple[str, str, DynamicFileChangeType]] = []
        self._changes: list[tuple[str, DynamicFileChangeType]] = []
        return

    def load(self) -> _ps.NestedDict:
        if self._data_raw:
            return self._data_raw
        with _logger.sectioning("Config Files Load"):
            full_data = _data_loader.load(
                path_cc=self._path_cc,
                cache_manager=self._cache_manager,
            )
        with _logger.sectioning("CCA Load Hooks"):
            self._hook_manager.generate(const.FUNCNAME_CC_HOOK_LOAD, data=full_data)
        with _logger.sectioning("Post-Load Data Validation"):
            _data_validator.validate(data=full_data, source="source", before_substitution=True)
        with _logger.sectioning("CCA Load Validation Hooks"):
            self._hook_manager.generate(const.FUNCNAME_CC_HOOK_LOAD_VALID, data=full_data)
        changelog_manager = ChangelogManager(repo_path=self._git.repo_path)
        code_context_call = {
            "changelog": changelog_manager
        }
        full_data["changelogs"] = changelog_manager.changelogs
        full_data["contributor"] = changelog_manager.contributor
        inline_hooks = self._hook_manager.inline_hooks
        if inline_hooks:
            code_context_call["hook"] = inline_hooks.Hooks(
                repo_path=self._git.repo_path,
                ccc=self._data_before,
                ccc_main=self._data_main,
                cache_manager=self._cache_manager,
                github_token=self._github_token,
            )

        def get_prefix(get, prefix: str):
            return [get(key) for key in full_data.keys() if key.startswith(prefix)]

        self._data_raw = _ps.NestedDict(
            full_data,
            code_context={
                "repo_path": self._path_root,
                "ccc_main": self._data_main,
                "ccc": self._data_before,
                "cache_manager": self._cache_manager,
                "slugify": _pylinks.string.to_slug,
                "fill_entity": _functools.partial(
                    _helper.fill_entity,
                    github_api=self._github_api,
                    cache_manager=self._cache_manager,
                ),
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
            skip_key_func=_skip_key_func,
        )
        return self._data_raw

    def generate_data(self) -> _ps.NestedDict:
        if self._data:
            return self._data
        self.load()
        with _logger.sectioning("Dynamic Data Generation"):
            data = _data_gen.generate(
                git_manager=self._git,
                cache_manager=self._cache_manager,
                github_api=self._github_api,
                data=self._data_raw,
                data_before=self._data_before,
                data_main=self._data_main,
                future_versions=self._future_vers,
            )
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
        _data_gen.validate_user_schema(data, before_substitution=True)
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
        self._cache_manager.save()
        return self._data

    def generate_files(self) -> list[_GeneratedFile]:
        if self._files:
            return self._files
        self.generate_data()
        with _logger.sectioning("Dynamic File Generation"):
            self._files = _file_gen.generate(
                data=self._data,
                data_before=self._data_before,
                repo_path=self._path_root,
            )
        return self._files

    def compare(self):
        if self._changes and self._files and self._dirs:
            return self._changes, self._files, self._dirs
        files = self.generate_files()
        metadata_changes = _ps.compare.items(source=self._data(), target=self._data_before(), path="")
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
            filepath_before_abs = self._path_root / generated_file.path_before if generated_file.path_before else None
            if generated_file.change in (
                DynamicFileChangeType.REMOVED,
                DynamicFileChangeType.MOVED,
                DynamicFileChangeType.MOVED_MODIFIED
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
                    filepath_abs.chmod(filepath_abs.stat().st_mode | _stat.S_IXUSR | _stat.S_IXGRP | _stat.S_IXOTH)
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
                            self._path_root.joinpath(destination).joinpath(_Path(source).stem).unlink(missing_ok=True)
        for key, duplicate in self._data.items():
            if not key.startswith("copy_"):
                continue
            if "source" in duplicate:
                for destination in duplicate["destinations"]:
                    _shutil.copy2(self._path_root.joinpath(duplicate["source"]), self._path_root.joinpath(destination))
            else:
                for source_glob in duplicate["sources"]:
                    for source in self._path_root.glob(source_glob):
                        for destination in duplicate["destinations"]:
                            destination_path = self._path_root.joinpath(destination).joinpath(_Path(source).stem)
                            destination_path.parent.mkdir(parents=True, exist_ok=True)
                            _shutil.copy2(self._path_root.joinpath(source), destination_path)
        return

    def _compare_dirs(self):

        def compare_source(main_key: str, root_path: str, root_path_before: str):
            source_name, source_name_before = self._get_dirpath(f"{main_key}.path.source_rel")
            source_path = f"{root_path}/{source_name}" if root_path else None
            source_path_before_real = f"{root_path_before}/{source_name_before}" if root_path_before and source_name_before else None
            change = self._compare_dir_paths(source_path, source_path_before_real)
            source_path_before = f"{root_path}/{source_name_before}" if root_path and source_name_before else None
            return source_path, source_path_before, source_path_before_real, change

        def compare_import(main_key: str, source_path: str, source_path_before: str, source_path_before_real: str):
            import_name, import_name_before = self._get_dirpath(f"{main_key}.import_name")
            import_path = f"{source_path}/{import_name}" if source_path and import_name else None
            import_path_before_real = f"{source_path_before_real}/{import_name_before}" if source_path_before_real and import_name_before else None
            change = self._compare_dir_paths(import_path, import_path_before_real)
            import_path_before = f"{source_path}/{import_name_before}" if source_path and import_name_before else None
            return import_path, import_path_before, import_path_before_real, change

        if self._dirs:
            return self._dirs
        dirs = []
        to_apply = []
        for path_key in ("control", ):
            path, path_before, status = self._compare_dir(f"{path_key}.path")
            dirs.append(
                _DynamicDir(
                    type=DynamicDirType[path_key.upper()],
                    path=path,
                    path_before=path_before,
                    change=status
                )
            )
            to_apply.append((path, path_before, status))

        for path_key, value in self._data.items():
            if not path_key.startswith("pypkg_"):
                continue

            root_path, root_path_before, root_status = self._compare_dir(f"{path_key}.path.root")
            dirs.append(
                _DynamicDir(
                    type=DynamicDirType.PKG_ROOT,
                    path=root_path,
                    path_before=root_path_before,
                    change=root_status
                )
            )
            to_apply.append((root_path, root_path_before, root_status))

            source_path, source_path_before, source_path_before_real, source_change = compare_source(
                main_key=path_key, root_path=root_path, root_path_before=root_path_before
            )
            dirs.append(
                _DynamicDir(
                    type=DynamicDirType.PKG_SRC,
                    path=source_path,
                    path_before=source_path_before_real,
                    change=source_change
                )
            )
            to_apply.append((source_path, source_path_before, source_change))

            import_path, import_path_before, import_path_before_real, import_change = compare_import(
                main_key=path_key, source_path=source_path, source_path_before=source_path_before, source_path_before_real=source_path_before_real
            )
            dirs.append(
                _DynamicDir(
                    type=DynamicDirType.PKG_IMPORT,
                    path=import_path,
                    path_before=import_path_before_real,
                    change=import_change
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
            status = DynamicFileChangeType.UNCHANGED if path == path_before else DynamicFileChangeType.MOVED
        elif not path and not path_before_exists:
            status = DynamicFileChangeType.DISABLED
        elif path_before_exists:
            status = DynamicFileChangeType.REMOVED
        else:
            path_exists = (self._path_root / path).is_dir()
            status = DynamicFileChangeType.UNCHANGED if path_exists else DynamicFileChangeType.ADDED
        return status


def _skip_key_func(key_parts: list[str]) -> bool:
    if not key_parts:
        return False

    key_parts = list(reversed(key_parts))

    # Define valid prefixes as sequences of fields
    valid_prefixes = [
        [_re.compile(r"data_.*"), "jsonschema", "schema"],
        [_re.compile(r"file_.*"), "data", "jsonschema", "schema"],
        [_re.compile(r"devcontainer_.*"), "file", _re.compile(r".*"), "data", "jsonschema", "schema"],
        [_re.compile(r"devcontainer_.*"), "apt", _re.compile(r".*"), "data", "jsonschema", "schema"],
        [_re.compile(r"devcontainer_.*"), "environment", _re.compile(r".*"), _re.compile(r"conda|pip|file"),
         _re.compile(r".*"), "data", "jsonschema", "schema"],
        [_re.compile(r"pypkg_.*"), "file", _re.compile(r".*"), "data", "jsonschema", "schema"],
    ]

    # Check if the path matches any of the valid prefixes
    prefix_len = 0
    for prefix in valid_prefixes:
        if len(key_parts) >= len(prefix) and all(
            (isinstance(p, str) and p == key_parts[i]) or (isinstance(p, _re.Pattern) and p.match(key_parts[i]))
            for i, p in enumerate(prefix)
        ):
            prefix_len = len(prefix)
            break
    else:
        return False

    # Check if "default" appears but not immediately after "properties"
    for i in range(prefix_len, len(key_parts)):
        if key_parts[i] == "default" and key_parts[i - 1] != "properties":
            return True
    return False
