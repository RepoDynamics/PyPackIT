from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

from versionman.pep440_semver import PEP440SemVer

from proman.dstruct import Version, VersionTag
from proman.dtype import BranchType

if _TYPE_CHECKING:
    from proman.manager import Manager


class BinderReleaseManager:
    def __init__(self, manager: Manager):
        self._manager = manager
        self._job = self._manager.data.get("workflow.binder", {})

        self._image_tags: dict[str, str] = {}
        self._cache_image_tags: list[str] = []
        return

    def write_dockerfile(self) -> bool:
        binder_directory = self._job.get("path", {}).get("dockerfile")
        if not binder_directory:
            return False
        image_tag = self._image_tags.get(
            "version_major", self._image_tags.get("transient", self._image_tags.get("latest"))
        )
        content = f"FROM {self.image_name}:{image_tag}\n"
        dockerfile_path = self._manager.git.repo_path / binder_directory / "Dockerfile"
        if dockerfile_path.exists():
            with open(dockerfile_path) as f:
                old_content = f.read()
            if content.strip() == old_content.strip():
                return False
        dockerfile_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dockerfile_path, "w") as f:
            f.write(content)
        return True

    def commit_changes(self, amend: bool = False) -> str | None:
        written = self.write_dockerfile()
        if not written:
            return None
        commit = self._manager.commit.create_auto(id="dockerfile_sync")
        return self._manager.git.commit(message=str(commit.conv_msg), amend=amend)

    @property
    def image_name(self) -> str:
        return "/".join(
            self._job["index"][key] for key in ("registry", "namespace", "name")
        ).lower()

    @property
    def image_tags(self) -> list[str]:
        return list(self._image_tags.values())

    @property
    def cache_image_tags(self) -> list[str]:
        return self._cache_image_tags

    def set_image_tag(
        self,
        version: Version | VersionTag | PEP440SemVer,
        branch_type: BranchType,
        pr_number: int | str | None = None,
    ):
        pep_semver = (
            version.version
            if isinstance(version, VersionTag)
            else (version.public if isinstance(version, Version) else version)
        )
        tags = {}
        cache_tags = []
        if isinstance(version, VersionTag):
            # This is a tagged version; add full version tag
            tags["version_full"] = str(version.version)
        if branch_type in (BranchType.MAIN, BranchType.RELEASE):
            # For all release branches, add major version tag
            if str(pep_semver) != "0.0.0":
                major_version_tag = f"v{pep_semver.major}"
                tags["version_major"] = major_version_tag
                cache_tags.append(major_version_tag)
            if branch_type is BranchType.MAIN:
                # For the main branch, add an extra latest tag
                tags["latest"] = "latest"
        elif branch_type is BranchType.PRE:
            tag = f"pre-{pep_semver.pre[1]}"
            tags["transient"] = tag
            cache_tags.append(tag)
        elif branch_type is BranchType.DEV:
            pr_tag = f"pr-{pr_number}"
            tags["transient"] = pr_tag
            cache_tags.append(pr_tag)
        self._image_tags = tags
        self._cache_image_tags = cache_tags
        return tags, cache_tags
