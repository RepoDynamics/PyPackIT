from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

import controlman as _controlman
from controlman import const as _const
from controlman import data_validator as _data_validator
from controlman.data_gen.main import MainDataGenerator as _MainDataGenerator
from controlman.data_gen.repo import RepoDataGenerator as _RepoDataGenerator

if _TYPE_CHECKING:
    from pyserials.nested_dict import NestedDict

    from proman.manager import Manager


def generate(
    data: NestedDict,
    manager: Manager,
    data_main: NestedDict,
    future_versions: dict[str, str],
) -> NestedDict:
    _MainDataGenerator(data=data, manager=manager).generate()
    if not data_main:
        curr_branch, other_branches = manager.git.get_all_branch_names()
        main_branch = data["repo.default_branch"]
        if curr_branch == main_branch:
            data_main = manager.data or data
        else:
            manager.git.fetch_remote_branches_by_name(main_branch)
            manager.git.stash()
            manager.git.checkout(main_branch)
            if (manager.git.repo_path / _const.FILEPATH_METADATA).is_file():
                data_main = _controlman.from_json_file(repo_path=manager.git.repo_path)
            else:
                data_main = manager.data or data
            manager.git.checkout(curr_branch)
            manager.git.stash_pop()
    _RepoDataGenerator(
        data=data,
        git_manager=manager.git,
        data_main=data_main,
        future_versions=future_versions,
    ).generate()
    return data


def validate_user_schema(data: NestedDict, before_substitution: bool):
    def validate_data(key: str, dynamic_data):
        if isinstance(dynamic_data, str) or "jsonschema" in dynamic_data:
            dynamic_data = data.fill(key)
        if "jsonschema" not in dynamic_data:
            return
        data_only = {k: v for k, v in dynamic_data.items() if k != "jsonschema"}
        fill = dynamic_data["jsonschema"].get("fill_defaults", False)
        _data_validator.validate_user_schema(
            data=data_only,
            schema=dynamic_data["jsonschema"]["schema"],
            before_substitution=before_substitution,
            fill_defaults=fill,
        )
        if fill:
            dynamic_data.update(data_only)
        return

    def validate_file_or_dep(key: str, dynamic_file):
        if isinstance(dynamic_file, str):
            dynamic_file = data.fill(key)
        if "data" in dynamic_file:
            validate_data(f"{key}.data", dynamic_file["data"])
        return

    def validate_files_or_deps(key: str, dynamic_files: str | dict):
        if isinstance(dynamic_files, str):
            dynamic_files = data.fill(key)
        for file_key, file in dynamic_files.items():
            validate_file_or_dep(f"{key}.{file_key}", file)
        return

    for k, v in data.items():
        if k.startswith("data_"):
            validate_data(k, v)
        elif k.startswith("file_"):
            validate_file_or_dep(k, v)
        elif k.startswith("devcontainer_"):
            if isinstance(v, str):
                data.fill(k)
            if "file" in v:
                validate_files_or_deps(f"{k}.file", v["file"])
            if "apt" in v:
                validate_files_or_deps(f"{k}.apt", v["apt"])
            if "task" in v:
                validate_files_or_deps(f"{k}.task", v["task"])
            if "environment" in v:
                envs = v["environment"]
                if isinstance(envs, str):
                    envs = data.fill(f"{k}.environment")
                for env_key, env in envs.items():
                    if isinstance(env, str):
                        env = data.fill(f"{k}.environment.{env_key}")
                    for key in ("conda", "pip", "file", "task"):
                        if key in env:
                            validate_files_or_deps(f"{k}.environment.{env_key}.{key}", env[key])
        elif k.startswith("pypkg_"):
            if isinstance(v, str):
                data.fill(k)
            if "file" in v:
                validate_files_or_deps(f"{k}.file", v["file"])
