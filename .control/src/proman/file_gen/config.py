from __future__ import annotations as _annotations

import copy as _copy
import os as _os
import re as _re
import shlex as _shlex
from pathlib import Path as _Path
from typing import TYPE_CHECKING as _TYPE_CHECKING
from xml.etree import ElementTree as _ElementTree

import pyserials as _ps
from licenseman.spdx import license_text as _license_text

from proman.file_gen import unit as _unit
from proman.file_gen import shell_script
from proman import const as _const
from proman.dtype import DynamicFile, DynamicFileChangeType, DynamicFileType

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
            + self.gitattributes()
            + self.gitignore()
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
                        config_component = component_data.get(f"{part}_config", {}).get(
                            output_type, {}
                        )
                        config_default = self._data[f"license.config.{part}.{output_type}"] or {}
                        _ps.update.recursive_update(
                            source=config_component,
                            addon=config_default,
                            type_mismatch="skip",
                        )
                        xml_elem = _ElementTree.fromstring(xml)
                        text = _license_text.SPDXLicenseTextPlain(xml_elem).generate(
                            **config_component
                        )
                    subtype_type = (
                        "license" if component_data["type"] == "license" else "license_exception"
                    )
                    subtype = f"{subtype_type}_{component_id}_{output_type}_{part}"
                    file = DynamicFile(
                        type=DynamicFileType.CONFIG,
                        subtype=(subtype, subtype_type.replace("_", " ").title()),
                        content=text,
                        path=path,
                        path_before=self._data_before.get("license.component", {})
                        .get(component_id, {})
                        .get("path", {})
                        .get(f"{part}_{output_type}"),
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
        file_content = (
            _ps.write.to_yaml_string(data=config, end_of_file_newline=True) if config else ""
        )
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
        elif file["type"] in ("shell_src", "shell_exec"):
            content = shell_script.create_script(
                name=file["name"],
                data=file["content"],
                script_type=file["type"],
                global_functions=self._data.get("devcontainer.function"),
            )
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
        for doc_key, doc in self._data.get("doc", {}).items():
            full_doc_key = f"doc.{doc_key}"
            out.append(
                self.dynamic_file(
                    key=full_doc_key,
                    file=doc,
                    file_before=self._data_before[full_doc_key]
                )
            )
        for feat_key, feat in self._data.get("devcontainer.feature", {}).items():
            for key, value in feat.items():
                if key not in ("path", "relpath"):
                    full_feat_key = f"{feat_key}.{key}"
                    out.append(
                        self.dynamic_file(
                            key=full_feat_key,
                            file=value,
                            file_before=self._data_before[full_feat_key]
                        )
                    )
        for key, value in self._data.items():
            if key.startswith("file_"):
                out.append(
                    self.dynamic_file(key=key, file=value, file_before=self._data_before[key])
                )
            elif key.startswith("devcontainer_"):
                for file_key, file in value.get("file", {}).items():
                    out.append(
                        self.dynamic_file(
                            key=f"{key}_{file_key}",
                            file=file,
                            file_before=self._data_before.get(key, {})
                            .get("file", {})
                            .get(file_key),
                        )
                    )
                for env_key, env in value.get("environment", {}).items():
                    for file_key, file in env.get("file", {}).items():
                        out.append(
                            self.dynamic_file(
                                key=f"{key}_{env_key}_{file_key}",
                                file=file,
                                file_before=self._data_before.get(key, {})
                                .get("environment", {})
                                .get(env_key, {})
                                .get("file", {})
                                .get(file_key),
                            )
                        )
                for vol_key, vol_file in value.get("volume", {}).items():
                    full_vol_key = f"{key}.volume.{vol_key}"
                    out.append(
                        self.dynamic_file(
                            key=full_vol_key,
                            file=vol_file,
                            file_before=self._data_before[full_vol_key]
                        )
                    )
            elif key.startswith("pypkg_"):
                for file_key, file in value.get("file", {}).items():
                    out.append(
                        self.dynamic_file(
                            key=f"{key}_{file_key}",
                            file=file,
                            file_before=self._data_before.get(key, {})
                            .get("file", {})
                            .get(file_key),
                        )
                    )
        return out

    def devcontainers(self) -> list[DynamicFile]:

        def create_dockerfile(dockerfile: list[dict]):

            def create_map(arg: dict) -> list[str]:
                """Create mapping (ARG, ENV) instruction for Dockerfile."""
                return [f'{key}="{value}"' if value else key for key, value in arg.items()]

            parts = []
            for part in dockerfile:
                instructions = []
                for instruction in part["instructions"]:
                    key = list(instruction.keys())[0].upper()
                    instructions_value = instruction[key]
                    if not instructions_value:
                        continue
                    if key in ("ARG", "ENV"):
                        instruction_lines = create_map(instructions_value)
                    else:
                        instruction_lines = [
                            line.rstrip() for line in instructions_value.strip().splitlines()
                            if line.strip() and not line.startswith("#")
                        ]
                    indent = (len(key) + 1) * " "
                    instruction_lines_full = [
                        f"{key} {instruction_lines[0]}{" \\" if len(instruction_lines) > 1 else ''}"
                    ] + [
                        f"{indent}{line} \\" for line in instruction_lines[1:-1]
                    ] + ([f"{indent}{instruction_lines[-1]}"] if len(instruction_lines) > 1 else [])
                    instructions.extend(instruction_lines_full)
                if instructions:
                    parts.append("\n".join(instructions))
            return "\n\n".join(parts)

        def create_docker_compose():
            path_depth = len(docker_compose_path.split("/")) - 1
            path_to_root_from_compose_file = "../" * path_depth if path_depth else "."
            config = docker_compose_data["config"]
            services = config.setdefault("services", {})
            for container_id, container in devcontainers.items():
                service_name = container["container"]["service"]
                if service_name in services:
                    raise ValueError(
                        f"Service '{service_name}' for devcontainer '{container_id}' already exists in docker-compose file."
                    )
                service = container.get("service", {})
                # service["image"] = f"devcontainer_{container_id}"
                service.setdefault("build", {}).update(
                    {
                        "context": path_to_root_from_compose_file,
                        "dockerfile": container["path"]["dockerfile"],
                    }
                )
                services[service_name] = {
                    "volumes": [
                        # Mount the root folder that contains .git
                        f"{path_to_root_from_compose_file}:{container['container']['workspaceFolder']}:cached"
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
                )
                if services
                else "",
                path=docker_compose_path,
                path_before=self._data_before["devcontainer.docker-compose.path"],
            )
            out.append(docker_compose_file)
            return

        out = []
        docker_compose_data = self._data["devcontainer.docker-compose"]
        docker_compose_path = docker_compose_data["path"]
        devcontainers = {
            k.removeprefix("devcontainer_"): v
            for k, v in self._data.items()
            if k.startswith("devcontainer_")
        }
        create_docker_compose()

        for container_id, container in devcontainers.items():
            container_before = self._data_before.get(f"devcontainer_{container_id}", {})
            container_dir_path_before = container_before.get("path", {}).get("root")

            # Dockerfile
            out.append(
                DynamicFile(
                    type=DynamicFileType.DEVCONTAINER_DOCKERFILE,
                    subtype=(container_id, container["container"].get("name", container_id)),
                    content=_unit.create_dynamic_file(
                        file_type="txt",
                        content=create_dockerfile(container["dockerfile"]),
                    ),
                    path=f"{container['path']['dockerfile']}",
                    path_before=f"{container_before.get('path', {}).get('dockerfile')}",
                )
            )

            # devcontainer.json
            devcontainer_json_path = f"{container['path']['root']}/devcontainer.json"
            container["container"].setdefault("dockerComposeFile", []).append(
                _os.path.relpath(docker_compose_path, _os.path.dirname(devcontainer_json_path))
            )
            out.append(
                DynamicFile(
                    type=DynamicFileType.DEVCONTAINER_METADATA,
                    subtype=(container_id, container.get("name", container_id)),
                    content=_unit.create_dynamic_file(
                        file_type="json",
                        content=container["container"],
                        **self._data["default"]["file_setting"]["json"],
                    ),
                    path=devcontainer_json_path,
                    path_before=f"{container_dir_path_before}/devcontainer.json" if container_dir_path_before else None,
                )
            )

            # APT files
            apt_group = {}
            for apt_package in container.get("apt", {}).values():
                apt_group.setdefault(apt_package["group"], []).append(apt_package)
            for apt_group_name, apt_group_pkgs in apt_group.items():
                apt_group_pkg_specs = []
                apt_group_repos = []
                apt_group_post_install = []
                for apt_group_pkg in apt_group_pkgs:
                    apt_group_pkg_specs.append(apt_group_pkg["spec"]["full"])
                    if "repo" in apt_group_pkg:
                        apt_group_repos.append(apt_group_pkg["repo"])
                    if "post_install" in apt_group_pkg:
                        apt_group_post_install.append(apt_group_pkg["post_install"])
                out.append(
                    DynamicFile(
                        type=DynamicFileType.DEVCONTAINER_APT,
                        subtype=(f"{container_id}_{apt_group_name}", f"{container.get("name", container_id)} {apt_group_name}"),
                        content=_unit.create_dynamic_file(
                            file_type="txt",
                            content=apt_group_pkg_specs,
                        ),
                        path=container['path']['apt'][apt_group_name]["packages"],
                        path_before=container_before['path']['apt'][apt_group_name]["packages"]
                        if container_before else None,
                    )
                )
                out.append(
                    DynamicFile(
                        type=DynamicFileType.DEVCONTAINER_APT_REPO,
                        subtype=(f"{container_id}_{apt_group_name}", f"{container.get("name", container_id)} {apt_group_name}"),
                        content=_unit.create_dynamic_file(
                            file_type="txt",
                            content=apt_group_repos,
                        ) if apt_group_repos else None,
                        path=container['path']['apt'][apt_group_name]["repos"],
                        path_before=container_before['path']['apt'][apt_group_name]["repos"]
                        if container_before else None,
                    )
                )
                out.append(
                    DynamicFile(
                        type=DynamicFileType.DEVCONTAINER_APT_POST,
                        subtype=(f"{container_id}_{apt_group_name}", f"{container.get("name", container_id)} {apt_group_name}"),
                        content=_unit.create_dynamic_file(
                            file_type="txt",
                            content=apt_group_post_install,
                        ) if apt_group_post_install else None,
                        path=container['path']['apt'][apt_group_name]["post_install"],
                        path_before=container_before['path']['apt'][apt_group_name]["post_install"]
                        if container_before else None,
                        executable=True,
                    )
                )

            # Conda environment files
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
        return out

    def gitattributes(self) -> list[DynamicFile]:
        """Process `.gitattributes` files defined at `$.repo.gitattributes`"""
        key = "repo.gitattributes"
        filetype = DynamicFileType.GITATTRIBUTES
        data = self._data.get(key, {})
        data_before = self._data_before.get(key, {})
        out = []
        for file_key, file_data in data.items():
            lines = []
            attributes = file_data["entries"]
            max_len_pattern = max([len(list(attribute.keys())[0]) for attribute in attributes])
            max_len_attr = max(
                [max(len(attr) for attr in list(attribute.values())[0]) for attribute in attributes]
            )
            for attribute in attributes:
                pattern = list(attribute.keys())[0]
                attrs = list(attribute.values())[0]
                attrs_str = "  ".join(f"{attr: <{max_len_attr}}" for attr in attrs).strip()
                lines.append(f"{pattern: <{max_len_pattern}}    {attrs_str}")
            file_content = "\n".join(lines)
            out.append(
                DynamicFile(
                    type=filetype,
                    subtype=(file_key, file_data["title"]),
                    content=file_content,
                    path=file_data["path"],
                    path_before=data_before.get(file_key, {}).get("path"),
                )
            )
        for old_file_key, old_file_data in data_before.get(key, {}).items():
            if old_file_key not in data:
                out.append(
                    DynamicFile(
                        type=filetype,
                        subtype=(old_file_key, old_file_data["title"]),
                        path_before=old_file_data["path"],
                    )
                )
        return out

    def gitignore(self) -> list[DynamicFile]:
        """Process `.gitignore` files defined at `$.repo.gitignore`"""
        key = "repo.gitignore"
        filetype = DynamicFileType.GITIGNORE
        data = self._data.get(key, {})
        data_before = self._data_before.get(key, {})
        out = []
        for file_key, file_data in data.items():
            file_content = "\n".join(file_data["entries"])
            out.append(
                DynamicFile(
                    type=filetype,
                    subtype=(file_key, file_data["title"]),
                    content=file_content,
                    path=file_data["path"],
                    path_before=data_before.get(file_key, {}).get("path"),
                )
            )
        for old_file_key, old_file_data in data_before.get(key, {}).items():
            if old_file_key not in data:
                out.append(
                    DynamicFile(
                        type=filetype,
                        subtype=(old_file_key, old_file_data["title"]),
                        path_before=old_file_data["path"],
                    )
                )
        return out

    def readthedocs(self) -> list[DynamicFile]:
        """Process `.readthedocs` file defined at `$.web.readthedocs.config_file`"""
        key = "web.readthedocs.config_file"
        filetype = DynamicFileType.WEB_CONFIG
        data = self._data.get(key, {})
        data_before = self._data_before.get(key, {})
        dynamic_file = {
            "type": filetype,
            "subtype": ("readthedocs", "ReadTheDocs"),
            "path": data.get("path"),
            "path_before": data_before.get("path"),
        }
        content = data.get("content")
        if content:
            content_str = _unit.create_dynamic_file(
                file_type="yaml",
                content=content,
                **self._data["default"]["file_setting"]["yaml"],
            )
            dynamic_file["content"] = content_str
        return [DynamicFile(**dynamic_file)]
