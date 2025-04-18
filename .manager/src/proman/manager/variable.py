from __future__ import annotations as _annotations

import copy
from typing import TYPE_CHECKING as _TYPE_CHECKING

import pyserials as ps
from loggerman import logger

import controlman.exception as _exception
from controlman import data_validator
from proman import const

if _TYPE_CHECKING:
    from proman.manager import Manager


class VariableManager(ps.PropertyDict):
    def __init__(self, manager: Manager):
        self._manager = manager
        log_title = "Variables Load"
        self._filepath = self._manager.git.repo_path / const.FILEPATH_VARIABLES
        if self._filepath.exists():
            try:
                var = ps.read.json_from_file(self._filepath)
            except ps.exception.read.PySerialsReadException as e:
                raise _exception.load.ControlManInvalidMetadataError(
                    cause=e, filepath=self._filepath
                ) from None
            logger.success(
                log_title,
                f"Loaded variables from file '{const.FILEPATH_VARIABLES}':",
                logger.data_block(var),
            )
        else:
            var = {}
            logger.info(log_title, f"No variables file found at '{const.FILEPATH_VARIABLES}'.")
        self._read_var = copy.deepcopy(var)
        data_validator.validate(var, schema="variables")
        super().__init__(var)
        return

    def commit_changes(self, amend: bool = False) -> str | None:
        written = self.write_file()
        if not written:
            return None
        commit = self._manager.commit.create_auto(id="vars_sync")
        return self._manager.git.commit(message=str(commit.conv_msg), amend=amend)

    def write_file(self) -> bool:
        if self.as_dict == self._read_var:
            return False
        self._filepath.write_text(
            ps.write.to_json_string(self.as_dict, sort_keys=True, indent=3).strip() + "\n",
            newline="\n",
        )
        return True
