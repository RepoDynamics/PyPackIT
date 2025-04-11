from __future__ import annotations

from typing import TYPE_CHECKING
import datetime as _datetime

import mdit as _mdit
import pyserials as _ps
from loggerman import logger as _logger

from proman import const as _const
from controlman import data_validator as _data_validator
from proman.util import date
from controlman import exception as _exception

if TYPE_CHECKING:
    from proman.manager import Manager


class CacheManager:
    def __init__(self, manager: Manager):
        def log_msg_new_cache(reason: str | None = None, traceback: bool = False):
            msg = (
                _mdit.inline_container(
                    "The provided filepath ",
                    _mdit.element.code_span(str(self._path)),
                    f" for control center cache {reason}. ",
                    "Initialized a new cache.",
                )
                if reason
                else "No filepath provided for control center cache. Initialized a new cache."
            )
            log_content = [msg]
            if traceback:
                log_content.append(_logger.traceback())
            _logger.warning(log_title, *log_content, stack_up=1)
            return

        self._manager = manager
        self._path = None
        self._cache = {}
        self._retention_hours = self._manager.data.get("control.cache.retention_hours", {})

        log_title = "Cache Initialization"
        relpath_local_cache = self._manager.data.get("local.cache.path")
        if not relpath_local_cache:
            log_msg_new_cache("is not defined")
            return
        path_local_cache = self._manager.git.repo_path / relpath_local_cache

        self._path = (
            path_local_cache / _const.DIRNAME_LOCAL_REPODYNAMICS / _const.FILENAME_METADATA_CACHE
        )
        if not self._path.is_file():
            log_msg_new_cache("does not exist")
            return
        try:
            self._cache = _ps.read.yaml_from_file(path=self._path)
        except _ps.exception.read.PySerialsReadException:
            log_msg_new_cache("is corrupted", traceback=True)
        try:
            _data_validator.validate(
                data=self._cache,
                schema="cache",
            )
        except _exception.ControlManException:
            log_msg_new_cache("is invalid", traceback=True)
            return

        _logger.success(
            log_title,
            _mdit.inline_container(
                "Loaded control center cache from ",
                _mdit.element.code_span(str(self._path)),
            ),
        )

        path_local_config = path_local_cache / _const.FILENAME_LOCAL_CONFIG
        if path_local_config.is_file():
            with _logger.sectioning("Local Cache Configuration"):
                try:
                    local_config = _ps.read.yaml_from_file(path=path_local_config, safe=True)
                except _ps.exception.read.PySerialsInvalidDataError as e:
                    raise _exception.load.ControlManInvalidConfigFileDataError(cause=e) from None
                _data_validator.validate(data=local_config, schema="local")
                self._retention_hours = local_config.get("retention_hours", self._retention_hours)
        return

    def get(self, typ: str, key: str):
        log_title = _mdit.inline_container(
            "Cache Retrieval for ", _mdit.element.code_span(f"{typ}.{key}")
        )
        if typ not in self._retention_hours:
            _logger.warning(
                log_title,
                _mdit.inline_container(
                    "Retention hours not defined for cache type ",
                    _mdit.element.code_span(typ),
                    ". Skipped cache retrieval.",
                ),
            )
            return None
        item = self._cache.get(typ, {}).get(key)
        if not item:
            _logger.info(log_title, "Item not found.")
            return None
        timestamp = item.get("timestamp")
        if timestamp and self._is_expired(typ, timestamp):
            _logger.info(
                log_title,
                f"Item expired.\n- Timestamp: {timestamp}\n- Retention Hours: {self._retention_hours}",
            )
            return None
        _logger.info(
            log_title,
            "Item found.",
            _mdit.element.code_block(_ps.write.to_yaml_string(item["data"]), language="yaml"),
        )
        return item["data"]

    def set(self, typ: str, key: str, value: dict | list | str | float | bool):
        new_item = {
            "timestamp": date.to_iso(date.from_now()),
            "data": value,
        }
        self._cache.setdefault(typ, {})[key] = new_item
        _logger.info(
            _mdit.inline_container("Cache Set for ", _mdit.element.code_span(f"{typ}.{key}")),
            _mdit.element.code_block(_ps.write.to_yaml_string(value), language="yaml"),
        )
        return

    def save(self):
        log_title = "Cache Save"
        if self._path:
            _ps.write.to_yaml_file(
                data=self._cache,
                path=self._path,
                make_dirs=True,
            )
            _logger.success(
                log_title,
                _mdit.inline_container(
                    "Saved control center cache to ",
                    _mdit.element.code_span(str(self._path)),
                ),
            )
        else:
            _logger.warning(
                log_title, "No filepath provided for control center cache. Skipped saving cache."
            )
        return

    def _is_expired(self, typ: str, timestamp: str) -> bool:
        time_delta = _datetime.timedelta(hours=self._retention_hours[typ])
        if not time_delta:
            return False
        exp_date = date.from_iso(timestamp) + time_delta
        return exp_date <= _datetime.datetime.now(tz=_datetime.UTC)
