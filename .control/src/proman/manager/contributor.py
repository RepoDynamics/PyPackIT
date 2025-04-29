from __future__ import annotations as _annotations

import copy
from typing import TYPE_CHECKING as _TYPE_CHECKING

import pyserials as ps
from loggerman import logger

if _TYPE_CHECKING:
    from proman.dstruct import User
    from proman.manager import Manager


class ContributorManager(ps.PropertyDict):
    def __init__(self, manager: Manager):
        self._manager = manager
        self._filepath = self._manager.git.repo_path / self._manager.data[f"control.contributor.path"]
        contributors = self._manager.data["contributor"]
        super().__init__(contributors)
        self._read = copy.deepcopy(contributors)
        return

    def add(self, user: User) -> dict:
        contributor_id = (
            user.get("github", {}).get("rest_id") or f"{user.name.full}_{user.email.id}"
        )
        contributor_entry = self.setdefault(contributor_id, {})
        ps.update.recursive_update(contributor_entry, user.as_dict)
        return contributor_entry

    def commit_changes(self, amend: bool = False) -> str | None:
        written = self.write_file()
        if not written:
            return None
        commit = self._manager.commit.create_auto(id="contrib_sync")
        return self._manager.git.commit(message=str(commit.conv_msg), amend=amend)

    def write_file(self) -> bool:
        if self.as_dict == self._read:
            return False
        self._filepath.write_text(
            ps.write.to_json_string(self.as_dict, sort_keys=True, indent=3).strip() + "\n",
            newline="\n",
        )
        return True
