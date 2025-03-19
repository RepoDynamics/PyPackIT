from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
from pathlib import Path as _Path
from xml.etree import ElementTree as _ElementTree
import copy as _copy
import os as _os
import re as _re
import shlex as _shlex

from loggerman import logger
import pyserials as _ps
from licenseman.spdx import license_text as _license_text

from controlman.datatype import DynamicFile, DynamicFileType, DynamicFileChangeType
from controlman.file_gen import unit as _unit
from controlman import const as _const

if _TYPE_CHECKING:
    from typing import Literal

class ConfigFileGenerator:
    def __init__(
        self,
        data: _ps.NestedDict,
        data_before: _ps.NestedDict,
        repo_path: _Path,
    ):
        self._data = data
        self._data_before = data_before
        self._path_repo = repo_path
        return

    def generate(self) -> list[DynamicFile]:
        return (
            self._generate_license()
            + self.issue_template_chooser()
            + self.dynamic_files()
            + self.devcontainers()
            + self.devcontainer_features()
        )

    def _is_disabled(self, key: str) -> bool:
        return not (self._data[key] or self._data_before[key])

    def _generate_license(self) -> list[DynamicFile]:
        if self._is_disabled("license"):
            return []
        files = []
        for component_id, component_data in self._data["license.component"].items():
            for part in ("text", "header"):
                if component_data["type"] == "exception" and part == "header":
                    continue
                for output_type in ("plain", "md"):
                    text = component_data.get(f"{part}_{output_type}")
                    xml = component_data.get(f"{part}_xml")
                    path = component_data["path"].get(f"{part}_{output_type}")
                    if not (path and (text or xml)):
                        continue
                    if not text:
                        config_component = component_data.get(f"{part}_config", {}).get(output_type, {})
                        config_default = self._data[f"license.config.{part}.{output_type}"] or {}
                        _ps.update.recursive_update(
                            source=config_component,
                            addon=config_default,
                            type_mismatch="skip",
                        )
                        xml_elem = _ElementTree.fromstring(xml)
                        text = _license_text.SPDXLicenseTextPlain(xml_elem).generate(**config_component)
                    subtype_type = "license" if component_data["type"] == "license" else "license_exception"
                    subtype = f"{subtype_type}_{component_id}_{output_type}_{part}"
                    file = DynamicFile(
                        type=DynamicFileType.CONFIG,
                        subtype=(subtype, subtype_type.replace("_", " ").title()),
                        content=text,
                        path=path,
                        path_before=self._data_before.get(
                            "license.component", {}
                        ).get(component_id, {}).get("path", {}).get(f"{part}_{output_type}")
                    )
                    files.append(file)
        return files

    def issue_template_chooser(self) -> list[DynamicFile]:
        if self._is_disabled("issue"):
            return []
        generate_file = {
            "type": DynamicFileType.CONFIG,
            "subtype": ("issue_chooser", "Issue Template Chooser"),
            "path": _const.FILEPATH_ISSUES_CONFIG,
            "path_before": _const.FILEPATH_ISSUES_CONFIG,
        }
        issues = self._data["issue"]
        if not issues:
            return [DynamicFile(**generate_file)]
        config = {"blank_issues_enabled": issues["blank_enabled"]}
        if issues.get("contact_links"):
            config["contact_links"] = issues["contact_links"]
        file_content = _ps.write.to_yaml_string(data=config, end_of_file_newline=True) if config else ""
        return [DynamicFile(content=file_content, **generate_file)]

    def dynamic_file(self, key: str, file: dict, file_before: dict | None):
        file_info = {
            "type": DynamicFileType.CUSTOM,
            "subtype": (key, file.get("name", key)),
            "executable": file["type"] == "exec",
        }
        if file["status"] == "delete":
            file_info["path_before"] = file["path"]
            return DynamicFile(**file_info)
        if file["status"] == "inactive":
            file_info["path_before"] = file["path"]
            file_info["change"] = DynamicFileChangeType.INACTIVE
            return DynamicFile(**file_info)
        if file["type"] == "md":
            content = _unit.create_md_content(file, repo_path=self._path_repo)
        else:
            content_setting = file["content_setting"]
            file_setting = file["file_setting"]
            content = _unit.create_dynamic_file(
                file_type=file["type"],
                content=file["content"],
                filters=[
                    (filter_["jsonpath"], eval(filter_["function"]), filter_["inplace"])
                    for filter_ in content_setting.get("filter", {}).values()
                ],
                order=content_setting.get("order"),
                content_item_separator=content_setting["separator"],
                content_item_prefix=content_setting["prefix"],
                content_item_suffix=content_setting["suffix"],
                end_of_file_newline=file_setting["eof_newline"],
                sort_keys=file_setting["sort_keys"],
                indent=file_setting["json"]["indent"],
                mapping_indent=file_setting["yaml"]["mapping_indent"],
                sequence_indent=file_setting["yaml"]["sequence_indent"],
                sequence_indent_offset=file_setting["yaml"]["sequence_indent_offset"],
                block_string=file_setting["yaml"]["block_string"],
                remove_top_level_indent=file_setting["yaml"]["remove_top_level_indent"],
            )
        return DynamicFile(
            content=content,
            path=file["path"],
            path_before=file_before["path"] if file_before else None,
            **file_info,
        )

    def dynamic_files(self) -> list[DynamicFile]:
        out = []
        for key, value in self._data.items():
            if key.startswith("file_"):
                out.append(self.dynamic_file(key=key, file=value, file_before=self._data_before[key]))
            elif key.startswith("devcontainer_"):
                for file_key, file in value.get("file", {}).items():
                    out.append(
                        self.dynamic_file(
                            key=f"{key}_{file_key}",
                            file=file,
                            file_before=self._data_before.get(key, {}).get("file", {}).get(file_key),
                        )
                    )
                for env_key, env in value.get("environment", {}).items():
                    for file_key, file in env.get("file", {}).items():
                        out.append(
                            self.dynamic_file(
                                key=f"{key}_{env_key}_{file_key}",
                                file=file,
                                file_before=self._data_before.get(key, {}).get("environment", {}).get(env_key, {}).get("file", {}).get(file_key),
                            )
                        )
            elif key.startswith("pypkg_"):
                for file_key, file in value.get("file", {}).items():
                    out.append(
                        self.dynamic_file(
                            key=f"{key}_{file_key}",
                            file=file,
                            file_before=self._data_before.get(key, {}).get("file", {}).get(file_key),
                        )
                    )
        return out

    def devcontainers(self) -> list[DynamicFile]:

        def create_docker_compose():
            path_depth = len(docker_compose_path.split("/")) - 1
            path_to_root_from_compose_file = "../" * path_depth if path_depth else "."
            config = docker_compose_data["config"]
            services = config.setdefault("services", {})
            for container_id, container in devcontainers.items():
                service_name = container["container"]["service"]
                if service_name in services:
                    raise ValueError(f"Service '{service_name}' for devcontainer '{container_id}' already exists in docker-compose file.")
                service = container.get("service", {})
                # service["image"] = f"devcontainer_{container_id}"
                service.setdefault("build", {}).update(
                    {
                        "context": path_to_root_from_compose_file,
                        "dockerfile": container["path"]["dockerfile"],
                    }
                )
                services[service_name] = {
                    "container_name": service_name,
                    "volumes": [
                        # Mount the root folder that contains .git
                        f"{path_to_root_from_compose_file}:{container["container"]["workspaceFolder"]}:cached"
                    ],
                    # Override default command so things don't shut down after the process ends.
                    "command": "sleep infinity",
                } | service
            docker_compose_file = DynamicFile(
                type=DynamicFileType.CONFIG,
                subtype=("docker-compose", "Docker Compose"),
                content=_unit.create_dynamic_file(
                    file_type="yaml",
                    content=config,
                    **self._data["default"]["file_setting"]["yaml"],
                ) if services else "",
                path=docker_compose_path,
                path_before=self._data_before[f"devcontainer.docker-compose.path"],
            )
            out.append(docker_compose_file)
            return

        def quote_shell_arguments(args: list[str] | None) -> list[str]:
            """Quotes arguments safely for Bash while preserving special shell parameters."""
            return [
                f'"{arg}"' if unquoted_task_process_patterns.match(arg) else _shlex.quote(arg)
                for arg in (args or [])
            ]

        def resolve_task_settings(
            devcontainer: dict,
            typ: Literal["local", "global"],
            environment: dict | None = None
        ):
            typ2 = "environment" if environment else "root"
            jsonpath = f"default.task_setting.{typ}.{typ2}"
            settings = self._data.get(jsonpath, {})
            settings_filled = _unit.fill_jinja_templates(
                templates=settings,
                jsonpath=jsonpath,
                env_vars={"devcontainer": devcontainer, "environment": environment or {}}
            )
            out = _copy.deepcopy(devcontainer.get("task_setting", {}).get(typ, {}).get(typ2, {}))
            _ps.update.recursive_update(
                source=out,
                addon=settings_filled,
            )
            return out

        def create_task_function(
            task: dict,
            task_setting: dict,
        ) -> str:
            def add_lines(content: str):
                lines.extend([(f"{indent}{line}" if line else "") for line in content.splitlines()])
                return

            lines = [f"{task["alias"]}() {{"]
            indent = 4 * " "
            if "script" in task:
                settings = task_setting.get("script", {})
                add_lines(settings.get("prepend", ""))
                add_lines(task["script"])
                add_lines(settings.get("append", ""))
            else:
                settings = task_setting.get("process", {})
                cmd = settings.get("prepend", [])
                cmd.extend(task["process"])
                cmd.extend(settings.get("append", []))
                cmd_quoted = quote_shell_arguments(cmd)
                add_lines(" ".join(cmd_quoted))
            lines.append("}")
            return "\n".join(lines)

        unquoted_task_process_patterns = _re.compile(
            r'^\$(\d+|\*|@)$'  # Matches $1, $2, ..., $@, $*
            r'|^\$\{[^}]+\}$'  # Matches ${VAR}, ${ARRAY[@]}, ${1}, etc.
            r'|^\$\w+$'  # Matches $VAR
            r'|^\$\(.+\)$'  # Matches $(command)
        )

        out = []
        docker_compose_data = self._data["devcontainer.docker-compose"]
        docker_compose_path = docker_compose_data["path"]
        devcontainers = {
            k.removeprefix("devcontainer_"): v
            for k, v in self._data.items() if k.startswith("devcontainer_")
        }
        create_docker_compose()

        for container_id, container in devcontainers.items():
            container_before = self._data_before.get(f"devcontainer_{container_id}", {})
            dockerfile = DynamicFile(
                type=DynamicFileType.DEVCONTAINER_DOCKERFILE,
                subtype=(container_id, container["container"].get("name", container_id)),
                content=_unit.create_dynamic_file(
                    file_type="txt",
                    content=container["dockerfile"],
                ),
                path=f"{container["path"]["dockerfile"]}",
                path_before=f"{container_before.get("path", {}).get("dockerfile")}",
            )
            out.append(dockerfile)
            # devcontainer.json file
            container_path = f"{container["path"]["root"]}/devcontainer.json"
            container["container"].setdefault("dockerComposeFile", []).append(
                _os.path.relpath(docker_compose_path, _os.path.dirname(container_path))
            )
            dir_path_before = container_before.get("path", {}).get("root")
            container_file = DynamicFile(
                type=DynamicFileType.DEVCONTAINER_METADATA,
                subtype=(container_id, container.get("name", container_id)),
                content=_unit.create_dynamic_file(
                    file_type="json",
                    content=container["container"],
                    **self._data["default"]["file_setting"]["json"],
                ),
                path=container_path,
                path_before=f"{dir_path_before}/devcontainer.json" if dir_path_before else None,
            )
            out.append(container_file)
            # apt.txt file
            apt_file = DynamicFile(
                type=DynamicFileType.DEVCONTAINER_APT,
                subtype=(container_id, container.get("name", container_id)),
                content=_unit.create_dynamic_file(
                    file_type="txt",
                    content=[pkg["spec"]["full"] for pkg in container["apt"].values()],
                ) if container.get("apt") else None,
                path=f"{container["path"]["apt"]}",
                path_before=f"{container_before.get("path", {}).get("apt")}",
            )
            out.append(apt_file)
            # conda environment files
            for env_id, env in container.get("environment", {}).items():
                env_file = DynamicFile(
                    type=DynamicFileType.DEVCONTAINER_CONDA,
                    subtype=(env_id, env["name"]),
                    content=_unit.create_dynamic_file(
                        file_type="yaml",
                        content=_unit.create_env_file_conda(
                            packages=list(env.get("conda", {}).values()),
                            pip_packages=list(env.get("pip", {}).values()),
                            env_name=env["name"],
                            variables=list(env.get("variable", {}).values()),
                        ),
                        **self._data["default"]["file_setting"]["yaml"],
                    ),
                    path=env["path"],
                    path_before=container_before.get("environment", {}).get(env_id, {}).get("path"),
                )
                out.append(env_file)
            # bash task file
            tasks = {"local": [], "global": []}
            for task in container.get("task", {}).values():
                for typ in tasks.keys():
                    tasks[typ].append(
                        create_task_function(
                            task=task,
                            task_setting=resolve_task_settings(devcontainer=container, typ=typ),
                        )
                    )
            for environment in container.get("environment", {}).values():
                for task in environment.get("task", {}).values():
                    for typ in tasks.keys():
                        tasks[typ].append(
                            create_task_function(
                                task=task,
                                task_setting=resolve_task_settings(devcontainer=container, typ=typ, environment=environment),
                            )
                        )
            for typ in tasks.keys():
                task_file = DynamicFile(
                    type=DynamicFileType[f"DEVCONTAINER_TASK_{typ.upper()}"],
                    subtype=(container_id, container.get("name", container_id)),
                    content=_unit.create_dynamic_file(
                        file_type="txt",
                        content=tasks[typ],
                        content_item_separator="\n\n",
                    ) if tasks[typ] else None,
                    path=f"{container["path"][f"tasks_{typ}"]}",
                    path_before=f"{container_before.get("path", {}).get(f"tasks_{typ}")}",
                )
                out.append(task_file)
        return out

    def devcontainer_features(self) -> list[DynamicFile]:
        out = []
        for key, feat in self._data.items():
            if not key.startswith("devfeature_"):
                continue
            path = f".devcontainer/{feat["path"]}"
            feat_before = self._data_before.get(key, {})
            path_before = f".devcontainer/{feat_before["path"]}" if feat_before else None
            metadata = feat["feature"]
            feature_file = DynamicFile(
                type=DynamicFileType.DEVCONTAINER_FEATURE_METADATA,
                subtype=(metadata["id"], metadata["name"]),
                content=_unit.create_dynamic_file(
                    file_type="json",
                    content=metadata,
                    **self._data["default"]["file_setting"]["json"],
                ),
                path=f"{path}/devcontainer-feature.json",
                path_before=f"{path_before}/devcontainer-feature.json" if feat_before else None,
            )
            install_file = DynamicFile(
                type=DynamicFileType.DEVCONTAINER_FEATURE_INSTALL,
                subtype=(metadata["id"], metadata["name"]),
                content=_unit.create_dynamic_file(
                    file_type="txt",
                    content=feat["install"],
                ),
                path=f"{path}/install.sh",
                path_before=f"{path_before}/install.sh" if feat_before else None,
                executable=True,
            )
            out.extend([feature_file, install_file])
        return out
