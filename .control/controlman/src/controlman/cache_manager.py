from pathlib import Path as _Path
import datetime as _datetime


from loggerman import logger as _logger
import pyserials as _ps
import mdit as _mdit

from controlman import exception as _exception, const as _const
from controlman import data_validator as _data_validator
from controlman import date

class CacheManager:

    def __init__(
        self,
        path_local_cache: _Path | str | None = None,
        retention_hours: dict[str, float] | None = None,
    ):

        def log_msg_new_cache(reason: str | None = None, traceback: bool = False):
            msg = _mdit.inline_container(
                "The provided filepath ",
                _mdit.element.code_span(str(self._path)),
                f" for control center cache {reason}. ",
                "Initialized a new cache.",
            ) if reason else "No filepath provided for control center cache. Initialized a new cache."
            log_content = [msg]
            if traceback:
                log_content.append(_logger.traceback())
            _logger.warning(log_title, *log_content, stack_up=1)
            return

        log_title = "Cache Initialization"

        self._cache = {}
        self._retention_hours = retention_hours or {}

        if path_local_cache:
            self._path = _Path(path_local_cache).resolve() / _const.DIRNAME_LOCAL_REPODYNAMICS / _const.FILENAME_METADATA_CACHE
            if not self._path.is_file():
                log_msg_new_cache("does not exist")
            else:
                try:
                    self._cache = _ps.read.yaml_from_file(path=self._path)
                except _ps.exception.read.PySerialsReadException as e:
                    log_msg_new_cache("is corrupted", traceback=True)
                try:
                    _data_validator.validate(
                        data=self._cache,
                        schema="cache",
                    )
                except _exception.ControlManException:
                    log_msg_new_cache("is invalid", traceback=True)
                else:
                    _logger.success(
                        log_title,
                        _mdit.inline_container(
                            "Loaded control center cache from ",
                            _mdit.element.code_span(str(self._path)),
                        )
                    )
        else:
            self._path = None
            log_msg_new_cache()
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
                    ". Skipped cache retrieval."
                )
            )
            return
        item = self._cache.get(typ, {}).get(key)
        if not item:
            _logger.info(log_title, "Item not found.")
            return
        timestamp = item.get("timestamp")
        if timestamp and self._is_expired(typ, timestamp):
            _logger.info(
                log_title,
                f"Item expired.\n- Timestamp: {timestamp}\n- Retention Hours: {self._retention_hours}"
            )
            return
        _logger.info(
            log_title,
            "Item found.",
            _mdit.element.code_block(_ps.write.to_yaml_string(item["data"]), language="yaml")
        )
        return item["data"]

    def set(self, typ: str, key: str, value: dict | list | str | int | float | bool):
        new_item = {
            "timestamp": date.to_iso(date.from_now()),
            "data": value,
        }
        self._cache.setdefault(typ, {})[key] = new_item
        _logger.info(
            _mdit.inline_container(
            "Cache Set for ",
                _mdit.element.code_span(f"{typ}.{key}")
            ),
            _mdit.element.code_block(_ps.write.to_yaml_string(value), language="yaml")
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
                )
            )
        else:
            _logger.warning(
                log_title,
                "No filepath provided for control center cache. Skipped saving cache."
            )
        return

    def _is_expired(self, typ: str, timestamp: str) -> bool:
        time_delta = _datetime.timedelta(hours=self._retention_hours[typ])
        if not time_delta:
            return False
        exp_date = date.from_iso(timestamp) + time_delta
        return exp_date <= _datetime.datetime.now(tz=_datetime.UTC)
