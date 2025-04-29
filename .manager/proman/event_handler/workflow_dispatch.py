from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from loggerman import logger

from proman.dtype import InitCheckAction
from proman.manager.changelog import ChangelogManager

if TYPE_CHECKING:
    from github_contexts.github.payload import WorkflowDispatchPayload


class Input(Enum):
    CCA = "config"
    LINT = "lint"
    BUILD = "build"
    TEST = "test"
    WEBSITE = "website"
    RELEASE = "release"


def bool_from_json(json_bool: str) -> bool:
    if json_bool == "false":
        return False
    if json_bool == "true":
        return True
    raise ValueError(f"JSON boolean {json_bool} not recognized.")


_INPUT_TYPE = {
    Input.CCA: InitCheckAction,
    Input.LINT: InitCheckAction,
    Input.BUILD: bool_from_json,
    Input.TEST: bool_from_json,
    Input.WEBSITE: bool_from_json,
    Input.RELEASE: bool_from_json,
}


class WorkflowDispatchEventHandler:
    def __init__(self, **kwargs):
        self._payload: WorkflowDispatchPayload = self.gh_context.event
        self._inputs = {}
        for k, v in self._payload.inputs.items():
            input_type = Input(k)
            input_value = _INPUT_TYPE[input_type](v)
            self._inputs[input_type] = input_value
        if self.gh_context.ref_is_main:
            self.branch_manager = self.manager
        else:
            self.branch_manager = self.manager_from_metadata_file(repo="head")
        return

    @logger.sectioner("Issues Handler Execution")
    def run(self):
        logger.info(
            "User Inputs",
            logger.data_block(self._payload.inputs),
        )
        if Input.CCA in self._inputs:
            new_manager, commit_hash = self.run_cca(
                branch_manager=self.manager,
                action=InitCheckAction.COMMIT,
                future_versions={self.gh_context.ref_name: version},
            )

        if Input.RELEASE in self._inputs:
            if self.gh_context.ref_is_main:
                return self._release_first_major_version()
            logger.critical("Cannot create first major release: not on main branch")
            return None
        return self._action_default()

    def _action_default(self):
        return

    def _release_first_major_version(self):
        latest_ver, _ = self._get_latest_version(base=True)
        if latest_ver is None:
            logger.critical("Cannot create first major release: no previous version found")
            return
        if latest_ver.major != 0:
            logger.critical("Cannot create first major release: latest version's major is not 0")
            return
        cc_manager = self.get_cc_manager(future_versions={self.gh_context.ref_name: "1.0.0"})
        self._ccm_main = cc_manager.generate_data()
        hash_before = self._git_head.commit_hash_normal()
        self.run_cca(
            action=proman.dtype.InitCheckAction.COMMIT,
            cc_manager=cc_manager,
            base=False,
            branch=proman.dtype.Branch(
                type=proman.dtype.BranchType.MAIN, name=self.gh_context.ref_name
            ),
        )
        changelog_manager = ChangelogManager(
            changelog_metadata=self._ccm_main["changelog"],
            ver_dist="1.0.0",
            commit_type=self._ccm_main["commit"]["primary_action"]["release_major"]["type"],
            commit_title="Release public API",
            parent_commit_hash=hash_before,
            parent_commit_url=self._gh_link.commit(hash_before),
            path_root=self._path_head,
        )
        release_body = (
            "This is the first major release of the project, defining the stable public API. "
            "There has been no changes to the public API since the last release, i.e., "
            f"version {latest_ver}."
        )
        changelog_manager.add_entry(changelog_id="package_public", sections=release_body)
        changelog_manager.write_all_changelogs()
        hash_latest = self._git_head.push()
        tag = self._tag_version(ver="1.0.0", base=False)

        self._output_manager.set(
            data_branch=self._ccm_main,
            ref=hash_latest,
            ref_before=self.gh_context.hash_before,
            version="1.0.0",
            release_name=f"{self._ccm_main['name']} v1.0.0",
            release_tag=tag,
            release_body=release_body,
            website_deploy=True,
            package_publish_testpypi=True,
            package_publish_pypi=True,
            package_release=True,
            website_url=self._ccm_main["url"]["website"]["base"],
        )
        return
