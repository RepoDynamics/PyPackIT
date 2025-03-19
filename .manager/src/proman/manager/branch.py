from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

from loggerman import logger

from proman.dstruct import Branch
from proman.dtype import BranchType

if _TYPE_CHECKING:
    from typing import Literal

    from github_contexts.github.payload.object.head_base import HeadBase

    from proman.manager import Manager


class BranchManager:
    def __init__(self, manager: Manager):
        self._manager = manager
        self._current_auto_base_branch: Branch | None = None
        self._remote_data = {
            branch["name"]: branch for branch in self._manager.gh_api_actions.branches
        }
        return

    def _make(self, type: BranchType, prefix: str, name: str | None = None, **kwargs):
        remote = self._remote_data.get(name, {})
        return Branch(
            type=type,
            prefix=prefix,
            sha=remote.get("commit", {}).get("sha"),
            protected=remote.get("protected"),
            protection=remote.get("protection"),
            linker=self._manager.gh_link,
            **kwargs,
        )

    def from_current_git_branch(self):
        return self.from_name(self._manager.git.current_branch_name())

    def from_pull_request_branch(self, branch: HeadBase | dict):
        b = self.from_name(branch["ref"])
        return Branch(
            type=b.type,
            prefix=b.prefix,
            linker=b.linker,
            version=b.version,
            issue=b.issue,
            target=b.target,
            auto_type=b.auto_type,
            separator=b.separator,
            sha=branch["sha"],
            protected=b.protected,
            protection=b.protection,
        )

    def from_name(self, branch_name: str | None = None) -> Branch:
        if not branch_name:
            branch_name = self._manager.git.current_branch_name()
        if branch_name == self._manager.gh_context.event.repository.default_branch:
            return self._make(type=BranchType.MAIN, prefix=branch_name, name=branch_name)
        for branch_type, branch_data in self._manager.data["branch"].items():
            if branch_name.startswith(branch_data["name"]):
                branch_type = BranchType(branch_type)
                args = {
                    "type": branch_type,
                    "prefix": branch_data["name"],
                    "separator": branch_data["name_separator"],
                }
                suffix_raw = branch_name.removeprefix(branch_data["name"])
                if branch_type is BranchType.RELEASE:
                    args["version"] = int(suffix_raw)
                elif branch_type is BranchType.PRE:
                    args["issue"] = int(suffix_raw)
                elif branch_type is BranchType.DEV:
                    issue_num, target_branch = suffix_raw.split(branch_data["name_separator"], 1)
                    args |= {"issue": int(issue_num), "target": self.from_name(target_branch)}
                else:
                    auto_type, target_branch = suffix_raw.split(branch_data["name_separator"], 1)
                    args |= {"auto_type": auto_type, "target": self.from_name(target_branch)}
                return self._make(**args, name=branch_name)
        return self._make(type=BranchType.OTHER, prefix=branch_name, name=branch_name)

    def from_version(self, version: str) -> Branch:
        return self.from_name(self._manager.data["project.version"][version]["branch"])

    def new_release(self, major_version: int) -> Branch:
        """Generate the name of the release branch for a given major version."""
        data = self._manager.data["branch.release"]
        return self._make(
            type=BranchType.RELEASE,
            prefix=data["name"],
            version=major_version,
            separator=data["name_separator"],
        )

    def new_pre(self, pull_nr: int) -> Branch:
        """Generate the name of the pre-release branch for a given version."""
        data = self._manager.data["branch.pre"]
        return self._make(
            type=BranchType.PRE,
            prefix=data["name"],
            issue=pull_nr,
            separator=data["name_separator"],
        )

    def new_dev(self, issue_nr: int, target: str | Branch) -> Branch:
        """Generate the name of the development branch for a given issue number and base branch."""
        data = self._manager.data["branch.dev"]
        if isinstance(target, str):
            target = self.from_name(target)
        return self._make(
            type=BranchType.DEV,
            prefix=data["name"],
            issue=issue_nr,
            target=target,
            separator=data["name_separator"],
        )

    def new_auto(
        self, auto_type: Literal["refactor", "config_sync"], target: str | Branch | None = None
    ) -> Branch:
        """Generate the name of the auto-update branch for a given type and base branch."""
        if not isinstance(target, Branch):
            target = self.from_name(target)
        data = self._manager.data["branch.auto"]
        return self._make(
            type=BranchType.AUTO,
            prefix=data["name"],
            auto_type=self._manager.data["commit.auto"][auto_type]["type"],
            target=target,
            separator=data["name_separator"],
        )

    def checkout_to_auto(self, branch: Branch) -> None:
        self._current_auto_base_branch = branch.target
        self._manager.git.stash()
        self._manager.git.checkout(branch=branch.name, reset=True)
        logger.info(
            "Auto-Update Branch",
            f"Switched to branch '{branch.name}' and reset it to '{branch.target.name}'.",
        )
        return

    def checkout_from_auto(self) -> None:
        if self._current_auto_base_branch:
            self._manager.git.checkout(branch=self._current_auto_base_branch.name)
            self._manager.git.stash_pop()
            logger.info(
                "Auto-Update Branch",
                f"Switched back to branch '{self._current_auto_base_branch.name}'.",
            )
            self._current_auto_base_branch = None
        return
