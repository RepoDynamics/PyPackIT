from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

from loggerman import logger
from versionman.pep440_semver import PEP440SemVer, latest_version_from_tags

from proman.dstruct import Version, VersionTag
from proman.dtype import IssueStatus, ReleaseAction
from proman.manager.release.binder import BinderReleaseManager
from proman.manager.release.github import GitHubReleaseManager
from proman.manager.release.zenodo import ZenodoManager

if _TYPE_CHECKING:
    from typing import Literal

    from gittidy import Git
    from versionman.pep440_semver import PEP440SemVer

    from proman.dstruct import Branch
    from proman.manager import Manager


class ReleaseManager:
    def __init__(self, manager: Manager):
        self._manager = manager
        self._binder = BinderReleaseManager(manager=self._manager)
        self._github = GitHubReleaseManager(manager=self._manager)
        self._zenodo = ZenodoManager(manager=self._manager)
        return

    @property
    def binder(self) -> BinderReleaseManager:
        return self._binder

    @property
    def github(self) -> GitHubReleaseManager:
        return self._github

    @property
    def zenodo(self) -> ZenodoManager:
        return self._zenodo

    def next_version(
        self,
        base_version: Version,
        issue_num: int | str,
        deploy_type: IssueStatus,
        action: ReleaseAction | None,
        first_public_release: bool = False,
    ) -> Version:
        if not action:
            # Internal changes; return next local version
            return Version(
                public=base_version.public,
                distance=base_version.distance + 1,
            )
        if base_version.public.pre:
            ver_base_pre_phase = base_version.public.pre[0]
            if ver_base_pre_phase == "rc":
                # Can only be the next post
                return Version(public=ver_base.public.next_post)
            if (
                deploy_type is IssueStatus.DEPLOY_FINAL
                or deploy_type.prerelease_type > ver_base_pre_phase
            ):
                # Next pre-release phase
                new_pre_phase = self._next_prerelease_phase(ver_base_pre_phase)
                new_ver = f"{ver_base.public.base}{new_pre_phase}{ver_base.public.pre[1]}"
                return Version(public=PEP440SemVer(new_ver))
            return Version(public=ver_base.public.next_post)
        next_final_ver = self._next_final_version(
            version=base_version.public, action=action, first_public_release=first_public_release
        )
        if action is ReleaseAction.POST or deploy_type is IssueStatus.DEPLOY_FINAL:
            return Version(public=next_final_ver)
        version = f"{next_final_ver.base}{deploy_type.prerelease_type}{issue_num}"
        return Version(public=PEP440SemVer(version))

    def next_dev_version_tag(
        self,
        version_base: PEP440SemVer,
        issue_num: int | str,
        action: ReleaseAction,
        version_head: PEP440SemVer | None = None,
    ) -> VersionTag:
        if version_base.pre:
            # The base branch is a pre-release branch
            next_ver = version_base.next_post
            if (
                version_head
                and version_head.release == next_ver.release
                and version_head.pre == next_ver.pre
                and version_head.dev is not None
            ):
                dev = version_head.dev + 1
            else:
                dev = 0
            return self.create_version_tag(PEP440SemVer(f"{next_ver}.dev{dev}"))
        next_ver = self._next_final_version(
            version=version_base, action=action, first_public_release=False
        )
        next_ver_str = str(next_ver)
        if action is not ReleaseAction.POST:
            next_ver_str += f".a{issue_num}"
        if not version_head:
            dev = 0
        elif action is ReleaseAction.POST:
            if version_head.post is not None and version_head.post == next_ver.post:
                dev = version_head.dev + 1
            else:
                dev = 0
        elif version_head.pre is not None and version_head.pre == ("a", int(issue_num)):
            dev = version_head.dev + 1
        else:
            dev = 0
        return self.create_version_tag(PEP440SemVer(f"{next_ver_str}.dev{dev}"))

    def latest_version(
        self,
        git: Git | None = None,
        branch: Branch | str | None = None,
        dev_only: bool = False,
    ) -> Version | None:

        git = git or self._manager.git
        ver_tag_prefix = self._manager.data["tag.version.prefix"]
        if branch:
            git.stash()
            curr_branch = git.current_branch_name()
            branch_name = branch if isinstance(branch, str) else branch.name
            git.checkout(branch=branch_name)
        latest_version = latest_version_from_tags(
            tags=git.get_tags(),
            version_tag_prefix=ver_tag_prefix,
            release_types=("dev",) if dev_only else ("final", "pre", "post", "dev"),
        )
        if branch:
            git.checkout(branch=curr_branch)
            git.stash_pop()
        if not latest_version:
            if not dev_only:
                logger.error(f"No matching version tags found with prefix '{ver_tag_prefix}'.")
            return None
        distance = git.get_distance(ref_start=f"refs/tags/{ver_tag_prefix}{latest_version.input}")
        return Version(
            public=latest_version,
            distance=distance,
            sha=git.commit_hash_normal(),
            date=git.commit_date_latest(),
        )

    def tag_next_dev_version(
        self,
        issue_num: int | str,
        git_base: Git,
        git_head: Git,
        action: ReleaseAction,
    ) -> VersionTag:
        version_head = self.latest_version(git=git_head, dev_only=True)
        next_dev_version_tag = self.next_dev_version_tag(
            version_base=self.latest_version(git=git_base, dev_only=False).public,
            version_head=version_head.public if version_head else None,
            issue_num=issue_num,
            action=action,
        )
        return self.tag_version(next_dev_version_tag, git=git_head)

    def tag_version(
        self,
        version: VersionTag | PEP440SemVer,
        env_vars: dict | None = None,
        git: Git | None = None,
    ) -> VersionTag:
        version_tag = (
            self.create_version_tag(version=version)
            if not isinstance(version, VersionTag)
            else version
        )
        major = str(version_tag.version.major)
        if major == "0":
            major = f"0.{version_tag.version.minor}"
        final_env_vars = {"version": version, "release": major} | (env_vars or {})
        msg = self._manager.fill_jinja_template(
            self._manager.data["tag.version.message"],
            env_vars=final_env_vars,
        )
        git = git or self._manager.git
        git.create_tag(tag=str(version_tag), message=msg)
        release_tag_config = self._manager.data["tag.release"]
        if release_tag_config:
            release_tag = f"{release_tag_config['prefix']}{major}"
            git.delete_tag(
                tag=release_tag,
                push_target="origin",
                raise_nonexistent=False,
            )
            release_tag_msg = self._manager.fill_jinja_template(
                release_tag_config["message"], env_vars=final_env_vars
            )
            git.create_tag(tag=release_tag, message=release_tag_msg)
        return version_tag

    def create_version_tag(self, version: PEP440SemVer) -> VersionTag:
        return VersionTag(tag_prefix=self._manager.data["tag.version.prefix"], version=version)

    @staticmethod
    def next_local_version(base_version: Version):
        return Version(public=base_version.public, distance=base_version.distance + 1)

    @staticmethod
    def _next_prerelease_phase(current_phase: Literal["a", "b", "rc"]) -> Literal["a", "b", "rc"]:
        return {
            "rc": "rc",
            "b": "rc",
            "a": "b",
        }[current_phase]

    @staticmethod
    def _next_final_version(
        version: PEP440SemVer, action: ReleaseAction, first_public_release: bool
    ) -> PEP440SemVer:
        if first_public_release and version.major == 0:
            return PEP440SemVer("1.0.0")
        if action is ReleaseAction.MAJOR:
            if version.major == 0:
                return version.next_minor
            return version.next_major
        if action == ReleaseAction.MINOR:
            if version.major == 0:
                return version.next_patch
            return version.next_minor
        if action == ReleaseAction.PATCH:
            return version.next_patch
        if action == ReleaseAction.POST:
            return version.next_post
        return version

    # def get_current_dirty_version(self):
    #     version = versioningit.get_version(
    #         project_dir=repo_path / data_branch["pkg.path.root"],
    #         config=data_branch["pkg.build.tool.versioningit"],
    #     )
