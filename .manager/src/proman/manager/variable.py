from __future__ import annotations as _annotations

import copy
from typing import TYPE_CHECKING as _TYPE_CHECKING

import controlman
import pyserials as ps
from controlman import data_validator
from loggerman import logger

if _TYPE_CHECKING:
    from pathlib import Path

    from proman.manager import Manager


class BareVariableManager(ps.PropertyDict):
    def __init__(self, repo_path: Path):
        log_title = "Variables Load"
        self._filepath = repo_path / controlman.const.FILEPATH_VARIABLES
        if self._filepath.exists():
            var = ps.read.json_from_file(self._filepath)
            logger.success(
                log_title,
                f"Loaded variables from file '{controlman.const.FILEPATH_VARIABLES}':",
                logger.data_block(var),
            )
        else:
            var = {}
            logger.info(
                log_title, f"No variables file found at '{controlman.const.FILEPATH_VARIABLES}'."
            )
        self._read_var = copy.deepcopy(var)
        data_validator.validate(var, schema="variables")
        super().__init__(var)
        return

    def write_file(self) -> bool:
        if self.as_dict == self._read_var:
            return False
        self._filepath.write_text(
            ps.write.to_json_string(self.as_dict, sort_keys=True, indent=3).strip() + "\n",
            newline="\n",
        )
        return True


class VariableManager(BareVariableManager):
    def __init__(self, manager: Manager):
        self._manager = manager
        super().__init__(self._manager.git.repo_path)
        return

    def commit_changes(self, amend: bool = False) -> str | None:
        written = self.write_file()
        if not written:
            return None
        commit = self._manager.commit.create_auto(id="vars_sync")
        return self._manager.git.commit(message=str(commit.conv_msg), amend=amend)
