from __future__ import annotations

from typing import TYPE_CHECKING

import mdit
import pyserials as ps
from loggerman import logger

from proman import const
from proman.dstruct import Version, VersionTag

if TYPE_CHECKING:
    from typing import Literal

    from versionman.pep440_semver import PEP440SemVer

    from proman.manager import Manager


class OutputManager:
    def __init__(self, manager: Manager):
        self._branch_manager = manager
        self._main_manager = manager.main

        self._repository: str = ""
        self._ref: str = ""
        self._ref_name: str = ""
        self._ref_before: str = ""
        self._version: VersionTag | Version | None = None
        self._jinja_env_vars = {}
        self._out_web: list[dict] = []
        self._out_lint: list[dict] = []
        self._out_test: list[dict] = []
        self._out_build: list[dict] = []
        self._out_binder: list[dict] = []
        self._out_publish_testpypi: dict = {}
        self._out_publish_anaconda: dict = {}
        self._out_publish_pypi: dict = {}
        self._out_release: dict = {}
        return

    def set(
        self,
        version: VersionTag | Version | PEP440SemVer,
        repository: str,
        ref: str | None = None,
        ref_name: str | None = None,
        ref_before: str | None = None,
        website_build: bool = False,
        website_deploy: bool = False,
        package_lint: bool = False,
        test_lint: bool = False,
        package_test: bool = False,
        package_test_source: Literal["github", "pypi", "testpypi"] = "github",
        package_build: bool = False,
        binder_build: bool = False,
        binder_deploy: bool = False,
        package_publish_testpypi: bool = False,
        package_publish_pypi: bool = False,
        package_publish_anaconda: bool = False,
        github_release_config: dict | None = None,
        zenodo_config: dict | None = None,
        zenodo_sandbox_config: dict | None = None,
    ):
        logger.info("Output Set", logger.pretty(locals()))
        self._version = version
        self._repository = repository or self._branch_manager.gh_context.target_repo_fullname
        self._ref = ref or self._branch_manager.git.commit_hash_normal()
        self._ref_name = ref_name or self._branch_manager.git.current_branch_name()
        self._ref_before = ref_before or self._branch_manager.gh_context.hash_before
        self._jinja_env_vars = {
            "version": version.version if isinstance(version, VersionTag) else version,
            "branch": self._ref_name,
            "commit": self._ref,
        }
        if website_build or website_deploy:
            self._set_web(deploy=website_deploy)
        if package_lint or test_lint:
            self._set_lint("pkg")
        if package_test:
            for key, val in self._branch_manager.data.items():
                if key.startswith("pypkg_") and "test" in val:
                    test_out = self._create_output_package_test(
                        pkg_id=key, source=package_test_source
                    )
                    self._out_test.append(test_out)
        if binder_build or binder_deploy:
            self._set_binder(deploy=binder_deploy)
        if (
            package_build
            or package_test
            or package_publish_testpypi
            or package_publish_pypi
            or package_publish_anaconda
        ):
            self.set_package_build_and_publish(
                publish_testpypi=package_publish_testpypi,
                publish_pypi=package_publish_pypi,
                publish_anaconda=package_publish_anaconda,
            )
        if github_release_config or zenodo_config or zenodo_sandbox_config:
            self.set_release(
                config_github=github_release_config,
                config_zenodo=zenodo_config,
                config_zenodo_sandbox=zenodo_sandbox_config,
            )
        return

    def generate(self, failed: bool | None = None) -> dict:
        failed = failed if failed is not None else self._branch_manager.reporter.failed
        if failed:
            # Just to be safe, disable publish/deploy/release jobs if fail is True
            for web_config in self._out_web:
                web_config["job"]["deploy"] = False
            self._out_publish_testpypi = False
            self._out_publish_anaconda = False
            self._out_publish_pypi = False
            self._out_release = False
        output = {
            "fail": failed,
            "web": self._out_web or False,
            "lint": self._out_lint or False,
            "test": self._out_test or False,
            "build": self._out_build or False,
            "binder": self._out_binder or False,
            "publish-testpypi": self._out_publish_testpypi or False,
            "publish-anaconda": self._out_publish_anaconda or False,
            "publish-pypi": self._out_publish_pypi or False,
            "release": self._out_release or False,
            "cm-anaconda": False,
        }
        output_yaml = ps.write.to_yaml_string(output)
        logger.info(
            "Action Outputs",
            mdit.element.code_block(output_yaml, language="yaml"),
        )
        return output

    @property
    def version(self) -> str:
        if isinstance(self._version, VersionTag):
            return str(self._version.version)
        return str(self._version)

    def _set_web(self, deploy: bool):
        job_config = self._main_manager.data["workflow.web"]
        if not job_config or (not deploy and job_config["action"]["build"] == "disabled"):
            return
        out = {
            "name": self._fill_jinja(job_config["name"]),
            "job": {
                "repository": self._repository,
                "ref": self._ref,
                "container": self._process_devcontainer(job_config["container"]),
                "artifact": self._create_workflow_artifact_config(job_config["artifact"]),
                "deploy": deploy,
                "env": job_config["env"],
            },
        }
        self._out_web.append(out)
        return

    def _set_lint(self, component: Literal["pkg", "test"]):
        # if component not in self._branch_manager.data:
        #     return
        job_config = self._main_manager.data["workflow.lint"]
        if not job_config or job_config["action"] == "disabled":
            return
        out = {
            "job": {
                "repository": self._repository,
                "ref-name": self._ref_name,
                "ref": self._ref,
                "ref-before": self._ref_before,
                # "os": list(self._branch_manager.data[f"{component}.os"].values()),
                # "pkg": self._branch_manager.data[component],
                # "pkg2": self._branch_manager.data["pkg" if component == "test" else "test"],
                # "python-max": self._branch_manager.data[f"{component}.python.version.minors"][-1],
                # "tool": self._branch_manager.data["tool"],
                # "type": component,
                "version": self.version,
            }
        }
        out["name"] = "Lint"
        # out["name"] = self._fill_jinja(
        #     job_config["name"],
        #     env_vars=out["job"] | self._jinja_env_vars,
        # )
        self._out_lint.append(out)
        return

    def _set_binder(self, deploy: bool):
        job_config = self._main_manager.data["workflow.binder"]
        if (
            not job_config
            or (not deploy and job_config["action"]["build"] == "disabled")
            or (
                deploy
                and job_config["action"]["deploy"] == "disabled"
                and job_config["action"]["build"] == "disabled"
            )
        ):
            return
        args = []
        for label_name, label_value in job_config.get("image", {}).get("label", {}).items():
            args.append(f'--label "{label_name}={self._fill_jinja(label_value)}"')
        out = {
            "name": self._fill_jinja(job_config["name"]),
            "job": {
                "name": "Build & Deploy" if deploy else "Build",
                "repository": self._repository,
                "ref": self._ref,
                "env": job_config["env"],
                "path-config": job_config["path"]["config"],
                "path-dockerfile": job_config["path"].get("dockerfile", ""),
                "registry": job_config["index"]["registry"],
                "username": job_config["index"]["username"],
                "artifact": self._create_workflow_artifact_config(job_config["artifact"]),
                "image-name": self._branch_manager.release.binder.image_name,
                "image-tags": " ".join(self._branch_manager.release.binder.image_tags),
                "tag-sha": "true" if isinstance(self._version, VersionTag) else "",
                "cache-image-tags": " ".join(self._branch_manager.release.binder.cache_image_tags),
                "repo2docker-args": " ".join(args),
                "dockerfile-append": "",
                "test-script": job_config.get("image", {}).get("test_script", ""),
                "push": str(deploy and job_config["action"]["deploy"] != "disabled"),
                "attest": isinstance(self._version, VersionTag),
            },
        }
        self._out_binder.append(out)
        return

    def set_package_build_and_publish(
        self,
        publish_testpypi: bool = False,
        publish_pypi: bool = False,
        publish_anaconda: bool = False,
        anaconda_label: str = "dev",
    ):
        def ci_builds(pkg: dict) -> list[dict]:
            builds = []
            for os in pkg["os"].values():
                ci_build = os.get("builds")
                if not ci_build:
                    continue
                for cibw_platform in ci_build:
                    for py_ver in pkg["python"]["version"]["minors"]:
                        cibw_py_ver = f"cp{py_ver.replace('.', '')}"
                        out = {
                            "runner": os["runner"],
                            "platform": cibw_platform,
                            "python": cibw_py_ver,
                        }
                        out["artifact"] = {
                            "wheel": self._create_workflow_artifact_config_single(
                                self._main_manager.data["workflow.build.artifact.wheel"],
                                jinja_env_vars=out | os,
                            )
                        }
                        builds.append(out)
            return builds

        def conda_builds(pkg: dict) -> list[dict]:
            def get_noarch_os():
                for runner_prefix in ("ubuntu", "macos", "windows"):
                    for os in pkg["os"].values():
                        if os["runner"].startswith(runner_prefix):
                            return os
                return None

            if pkg["python"]["pure"]:
                noarch_build = {
                    "os": get_noarch_os(),
                    "python": pkg["python"]["version"]["minors"][-1],
                }
                noarch_build["artifact"] = self._create_workflow_artifact_config_single(
                    self._main_manager.data["workflow.build.artifact.conda"],
                    jinja_env_vars=noarch_build | {"pkg": pkg, "platform": "any", "python": "3"},
                )
                return [noarch_build]
            builds = []
            for os in pkg["os"].values():
                for python_ver in pkg["python"]["version"]["minors"]:
                    out = {
                        "os": os,
                        "python": python_ver,
                    }
                    out["artifact"] = {
                        "conda": self._create_workflow_artifact_config_single(
                            self._main_manager.data["workflow.build.artifact.conda"],
                            jinja_env_vars=out | {"pkg": pkg},
                        )
                    }
                    builds.append(out)
            return builds

        build_jobs = {}
        build_config = self._main_manager.data["workflow.build"]
        # for typ in ("pkg", "test"):
        project_command_alias = self._branch_manager.data[
            "devcontainer_main.environment.pypackit.task.project.alias"
        ]
        for pkg_id in ("main", "test"):
            if (
                not (publish_pypi or publish_testpypi or publish_anaconda)
                and build_config["action"] == "disabled"
            ):
                continue
            key = f"pypkg_{pkg_id}"
            value = self._branch_manager.data[key]
            pure_python = value["python"]["pure"]
            build_job = {
                "repository": self._repository,
                "ref": self._ref_name,
                "pkg_id": pkg_id,
                "pure_python": pure_python,
                "build_command": f"{project_command_alias} build python --pkg {pkg_id} {'--sdist' if not pure_python else ''}",
                "build_command_conda": f"{project_command_alias} build conda --pkg {pkg_id}",
                "readme_command": f"{project_command_alias} render pypi --pkg {pkg_id}"
                if value["pyproject"]["project"].get("readme")
                else "",
                "pkg_path": value["path"]["root"],
                "ci-builds": ci_builds(value) or False,
                "conda-builds": conda_builds(value),
            }
            build_job["artifact"] = self._create_workflow_artifact_config(
                build_config["artifact"],
                jinja_env_vars=build_job | {"platform": "any", "python": "3", "pkg": value},
                include_merge=True,
            )
            out = {
                "name": self._fill_jinja(
                    build_config["name"],
                    env_vars=build_job | {"pkg": value},
                ),
                "job": build_job,
            }
            self._out_build.append(out)
            build_jobs[key] = build_job

        for (
            target,
            do_publish,
        ) in (
            ("testpypi", publish_testpypi),
            ("pypi", publish_pypi),
            ("anaconda", publish_anaconda),
        ):
            if not do_publish:
                continue
            job_config = self._main_manager.data[f"workflow.publish.{target}"]
            if not job_config:
                continue
            publish_out = {
                "name": self._fill_jinja(job_config["name"]),
                "job": {
                    "publish": [],
                    "test": self._create_output_package_test(source=target, flatten_name=True)
                    if self._branch_manager.data["test"]
                    else False,
                },
            }
            for typ, build in build_jobs.items():
                # TODO: Move toggle to pypkg objects
                # if job_config["action"][typ] == "disabled":
                #     continue
                publish_job = {
                    "name": self._fill_jinja(
                        job_config["task_name"],
                        env_vars=build | {"pkg": value},
                    ),
                    "env": {
                        "name": self._fill_jinja(
                            job_config["env"]["name"], env_vars=build | {"pkg": value}
                        ),
                        "url": self._fill_jinja(
                            job_config["env"]["url"],
                            env_vars=build | {"pkg": value},
                        ),
                    },
                    "artifact": build["artifact"],
                }
                if target != "anaconda":
                    publish_job["index-url"] = self._branch_manager.fill_jinja_template(
                        job_config["index"]["url"]["upload"],
                        env_vars=self._jinja_env_vars,
                    )
                else:
                    channel = job_config["index"]["channel"]
                    publish_job["user"] = channel
                    publish_job["version"] = self.version
                    pkg_name = self._branch_manager.data[f"{typ}.name"].lower()
                    publish_out["job"].setdefault("finalize", []).append(
                        {
                            "label": anaconda_label,
                            "spec": f"{channel}/{pkg_name}/{self.version or '0.0.0'}",
                        }
                    )
                publish_out["job"]["publish"].append(publish_job)
            if publish_out["job"]["publish"]:
                setattr(self, f"_out_publish_{target}", publish_out)
        return

    def set_release(
        self,
        config_github: dict | None = None,
        config_zenodo: dict | None = None,
        config_zenodo_sandbox: dict | None = None,
    ):
        for config, key, has_token in (
            (config_github, "github", True),
            (config_zenodo, "zenodo", bool(self._branch_manager.token.zenodo)),
            (
                config_zenodo_sandbox,
                "zenodo_sandbox",
                bool(self._branch_manager.token.zenodo_sandbox),
            ),
        ):
            job_config = self._branch_manager.data[f"workflow.publish.{key}"]
            if not job_config or job_config["action"] == "disabled" or not has_token:
                continue
            out = self._out_release or {
                "name": job_config["name"],
                "job": {
                    "ref": self._ref,
                    "repo-path": const.OUTPUT_RELEASE_REPO_PATH,
                    "artifact-path": const.OUTPUT_RELEASE_ARTIFACT_PATH,
                    "tasks": [],
                },
            }
            out["job"]["tasks"].append(
                {
                    "name": job_config["task_name"],
                    "env": job_config["env"],
                    "github": config if key == "github" else {},
                    "zenodo": config if key == "zenodo" else {},
                    "zenodo-sandbox": config if key == "zenodo_sandbox" else {},
                }
            )
            self._out_release = out
        return

    def __create_output_package_test(
        self,
        pkg_id: str,
        source: Literal["github", "pypi", "testpypi", "anaconda"] = "github",
        pyargs: list[str] | None = None,
        args: list[str] | None = None,
        overrides: dict[str, str] | None = None,
        flatten_name: bool = False,
    ) -> dict:
        source = source.lower()
        env_vars = {
            "source": {
                "github": "GitHub",
                "pypi": "PyPI",
                "testpypi": "TestPyPI",
                "anaconda": "Anaconda",
            }[source]
        }
        job_config = self._main_manager.data["workflow.test"]
        job_name = self._fill_jinja(job_config["name"], env_vars)
        out = {
            "name": job_name,
            "job": {
                "repository": self._repository,
                "ref": self._ref_name,
                "test-src": source,
                "test-path": self._branch_manager.data["test.path.root"],
                "test-name": self._branch_manager.data["test.import_name"],
                "test-version": self.version,
                "test-req-path": self._branch_manager.data["test.dependency.env.pip.path"]
                if source == "testpypi"
                else "",
                "pkg-src": source,
                "pkg-path": self._branch_manager.data["pkg.path.root"],
                "pkg-name": self._branch_manager.data["pkg.name"],
                "pkg-version": self.version,
                "pkg-req-path": self._branch_manager.data["pkg.dependency.env.pip.path"]
                if source == "testpypi"
                else "",
                "pyargs": ps.write.to_json_string(pyargs) if pyargs else "",
                "args": ps.write.to_json_string(args) if args else "",
                "overrides": ps.write.to_json_string(overrides) if overrides else "",
                "codecov-yml-path": self._branch_manager.data["tool.codecov.config.file.path"],
                "upload-codecov": True,
                "artifact": self._create_workflow_artifact_merge_config(
                    job_config["artifact"], env_vars
                ),
                "retries": "60",
                "retry-sleep-seconds": "15",
                "tasks": [],
            },
        }
        for os in self._branch_manager.data["pkg.os"].values():
            for python_version in self._branch_manager.data["pkg.python.version.minors"]:
                task = {
                    "runner": os["runner"],
                    "python": python_version,
                }
                task_env_vars = env_vars | task | {"os": os["name"]}
                task_name = self._fill_jinja(job_config["task_name"], task_env_vars)
                if flatten_name:
                    task_name = f"{job_name}: {task_name}"
                task |= {
                    "name": task_name,
                    "artifact": self._create_workflow_artifact_config(
                        job_config["artifact"], task_env_vars
                    ),
                }
                out["job"]["tasks"].append(task)
        return out

    def _create_output_package_test(
        self,
        pkg_id: str,
        source: Literal["github", "pypi", "testpypi", "anaconda"] = "github",
        flatten_name: bool = False,
    ) -> dict:
        pkg = self._branch_manager.data[pkg_id]
        source = source.lower()
        env_vars = {
            "source": {
                "github": "GitHub",
                "pypi": "PyPI",
                "testpypi": "TestPyPI",
                "anaconda": "Anaconda",
            }[source],
            "pkg": pkg,
        }
        job_config = self._main_manager.data["workflow.test"]
        job_name = self._fill_jinja(job_config["name"], env_vars)
        out = {
            "name": job_name,
            "job": {
                "artifact": self._create_workflow_artifact_merge_config(
                    job_config["artifact"], env_vars
                ),
                "codecov": job_config.get("codecov", False),
                "tasks": [],
            },
        }
        report_artifact_name_prefix = job_config["artifact"]["report"]["name"]
        for test in self._branch_manager.data[pkg_id]["test"].values():
            job_config["artifact"]["report"]["name"] = (
                report_artifact_name_prefix + test["artifact_name_suffix"]
            )
            task = {
                "name": test["name"],
                "runner": test["runner"],
                "repository": self._repository,
                "ref": self._ref_name,
                "conda_env": test["conda_env"],
                "script": test["script"],
                "codecov": test.get("codecov", {}),
                "artifact": self._create_workflow_artifact_config(job_config["artifact"], env_vars),
            }
            out["job"]["tasks"].append(task)
        return out

    def _create_workflow_artifact_config(
        self,
        artifact: dict,
        jinja_env_vars: dict | None = None,
        include_merge: bool = False,
    ) -> dict:
        return {
            k: self._create_workflow_artifact_config_single(v, jinja_env_vars, include_merge)
            for k, v in artifact.items()
        }

    def _create_workflow_artifact_merge_config(
        self, artifact: dict, jinja_env_vars: dict | None = None
    ) -> dict | bool:
        return {
            k: self._create_workflow_artifact_merge_config_single(v, jinja_env_vars)
            for k, v in artifact.items()
        }

    def _create_workflow_artifact_config_single(
        self, artifact: dict, jinja_env_vars: dict | None = None, include_merge: bool = False
    ) -> dict:
        out = {
            "name": self._fill_jinja(artifact["name"], jinja_env_vars),
            "retention_days": str(artifact.get("retention_days", "")),
            "include_hidden": str(artifact.get("include_hidden", "false")),
            "path": artifact.get("path"),
        }
        if include_merge:
            out["merge"] = self._create_merge(artifact, jinja_env_vars)
        return out

    def _create_workflow_artifact_merge_config_single(
        self, artifact: dict, jinja_env_vars: dict
    ) -> dict | bool:
        return {
            "merge": self._create_merge(artifact, jinja_env_vars),
            "include_hidden": str(artifact.get("include_hidden", "false")),
            "retention_days": str(artifact.get("retention_days", "")),
        }

    def _create_merge(self, artifact: dict, jinja_env_vars: dict) -> dict | bool:
        return (
            {
                "name": self._fill_jinja(artifact["merge"]["name"], jinja_env_vars),
                "pattern": self._fill_jinja(artifact["merge"]["pattern"], jinja_env_vars),
            }
            if "merge" in artifact
            else False
        )

    def _fill_jinja(self, template: str, env_vars: dict | None = None) -> str:
        return self._branch_manager.fill_jinja_template(
            template, env_vars=self._jinja_env_vars | (env_vars or {})
        )

    def _process_devcontainer(self, container: dict):
        devcontainer = self._main_manager.data[f"devcontainer_{container['id']}"]
        devcontainer_path = devcontainer["path"]
        workspace_path = devcontainer["container"]["workspaceFolder"]
        tasks_script_path = f"{workspace_path}/{devcontainer_path['tasks_local']}"
        return {
            k.replace("_", "-"): v
            for k, v in container.items()
            if k in ("name", "env", "inherit_env", "ref")
        } | {
            "path": f"{devcontainer_path['root']}/devcontainer.json",
            # The bashrc file is not executed in non-interactive shells,
            # so we need to source the tasks script again.
            # - https://stackoverflow.com/questions/55206227/why-bashrc-is-not-executed-when-run-docker-container
            # - https://stackoverflow.com/questions/6063618/bash-env-or-sourcing-a-file-in-a-non-interactive-non-login-shell
            # - https://github.com/microsoft/vscode-remote-release/issues/8436
            "command": f"source {tasks_script_path}\n{container['command']}",
            "env-names": "\n".join(list(container["env"].keys())),
        }
