from __future__ import annotations as _annotations

import copy
from typing import TYPE_CHECKING as _TYPE_CHECKING

import controlman
from controlman import exception as _exception
from controlman import data_validator
import pyserials as ps
from loggerman import logger

from proman import const

if _TYPE_CHECKING:
    from pathlib import Path

    from proman.dstruct import User
    from proman.manager import Manager


class ContributorManager(ps.PropertyDict):
    def __init__(self, manager: Manager):
        self._manager = manager
        log_title = "Contributors Load"
        self._filepath = self._manager.git.repo_path / const.FILEPATH_CONTRIBUTORS
        if self._filepath.exists():
            try:
                contributors = ps.read.json_from_file(self._filepath)
            except ps.exception.read.PySerialsReadException as e:
                raise _exception.load.ControlManInvalidMetadataError(
                    cause=e, filepath=self._filepath
                ) from None
            logger.success(
                log_title,
                f"Loaded contributors from file '{const.FILEPATH_CONTRIBUTORS}':",
                logger.data_block(contributors),
            )
        else:
            contributors = {}
            logger.info(
                log_title,
                f"No contributors file found at '{const.FILEPATH_CONTRIBUTORS}'.",
            )
        super().__init__(contributors)
        self._read = copy.deepcopy(contributors)
        data_validator.validate(data=contributors, schema="contributors")
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
