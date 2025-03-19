import datetime as _dt


OUTPUT_FORMAT = "%Y-%m-%d"


def from_now() -> _dt.datetime:
    return _dt.datetime.now(tz=_dt.UTC)


def from_internal(date: str) -> _dt.datetime:
    return _dt.datetime.strptime(date, OUTPUT_FORMAT).astimezone(_dt.UTC)

def from_iso(date: str) -> _dt.datetime:
    return _dt.datetime.fromisoformat(date).astimezone(_dt.UTC)

def from_github(date: str) -> _dt.datetime:
    return _dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").astimezone(_dt.UTC)


def to_internal(date: _dt.datetime) -> str:
    return date.astimezone(_dt.UTC).strftime(OUTPUT_FORMAT)


def to_iso_8601(date: _dt.datetime) -> str:
    return date.strftime("%Y-%m-%d")


def to_iso(date: _dt.datetime) -> str:
    return date.isoformat()


def to_posix(date: _dt.datetime) -> int:
    return int(date.timestamp())
