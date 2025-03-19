from __future__ import annotations

from typing import TYPE_CHECKING

import pyserials as _ps

import controlman
from controlman import const
from controlman import exception as _exception


if TYPE_CHECKING:
    from typing import Callable, Sequence
    from pathlib import Path


class ChangelogManager:

    def __init__(self, repo_path: Path):
        self._get_metadata = None
        self._path_changelog = repo_path / const.FILEPATH_CHANGELOG
        self._changelogs = controlman.read_changelog(repo_path=repo_path)
        self._contrib = controlman.read_contributors(repo_path=repo_path)
        return

    def __call__(self, get_metadata: Callable):
        self._get_metadata = get_metadata
        return self

    @property
    def contributor(self):
        return self._contrib

    @property
    def changelogs(self) -> list[dict]:
        return self._changelogs

    @property
    def current_public(self) -> Changelog:
        for changelog in self._changelogs:
            if changelog["type"] != "local":
                return Changelog(changelog, contrib=self._contrib, get_metadata=self._get_metadata)
        return Changelog({}, contrib=self._contrib, get_metadata=self._get_metadata)

    @property
    def last_public(self) -> Changelog:
        seen_public = False
        for changelog in self._changelogs:
            if changelog["type"] != "local":
                if seen_public:
                    return Changelog(changelog, contrib=self._contrib, get_metadata=self._get_metadata)
                seen_public = True
        return Changelog({}, contrib=self._contrib, get_metadata=self._get_metadata)


class Changelog(_ps.PropertyDict):

    def __init__(self, changelog: dict, get_metadata: Callable, contrib: dict | None):
        super().__init__(data=changelog)
        self._get_metadata = get_metadata
        self._contrib = contrib or {}
        return

    def contributors_with_role_types(
        self,
        role_types: str | Sequence[str],
        member: bool | None = None
    ) -> list[dict]:
        contrib = self._data.get("contributor")
        if not contrib:
            return []
        team_data = self._get_metadata("team")
        role_data = self._get_metadata("role")
        if isinstance(role_types, str):
            role_types = [role_types]
        out = []
        if member:
            types = ["member"]
        elif member is False:
            types = ["collaborator"]
        else:
            types = ["member", "collaborator"]
        for contributor_type in types:
            contributors = contrib.get(contributor_type)
            for contributor_id, contributor_data in contributors.items():
                max_priority = -1
                for role_type in role_types:
                    for role_id, priority in contributor_data["role"].items():
                        role = role_data[role_id]
                        if role["type"] == role_type:
                            max_priority = max(max_priority, priority)
                if max_priority >= 0:
                    is_member = contributor_type == "member"
                    if is_member:
                        entity = team_data[contributor_id]
                    else:
                        entity = self._contrib[contributor_id]
                    out.append(
                        (
                            entity | {"id": contributor_id, "member": is_member},
                            max_priority,
                            entity["name"]["full_inverted"]
                        )
                    )
        return [entity for entity, _, _ in sorted(out, key=lambda i: (i[1], i[2]), reverse=True)]
