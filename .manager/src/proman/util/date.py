import datetime as _dt

OUTPUT_FORMAT = "%Y-%m-%d"
OUTPUT_FORMAT_FULL = "%Y-%m-%d--%H-%M-%S"


def from_now() -> _dt.datetime:
    return _dt.datetime.now(tz=_dt.UTC)


def from_internal(date: str) -> _dt.datetime:
    for fmt in [OUTPUT_FORMAT, OUTPUT_FORMAT_FULL]:
        try:
            return _dt.datetime.strptime(date, fmt).astimezone(_dt.UTC)
        except ValueError:
            continue
    raise ValueError(f"Input '{date}' does not match supported formats.")


def from_iso(date: str) -> _dt.datetime:
    return _dt.datetime.fromisoformat(date).astimezone(_dt.UTC)


def from_github(date: str) -> _dt.datetime:
    return _dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").astimezone(_dt.UTC)


def to_internal(date: _dt.datetime, time: bool = False) -> str:
    return date.astimezone(_dt.UTC).strftime(OUTPUT_FORMAT_FULL if time else OUTPUT_FORMAT)


def to_iso(date: _dt.datetime) -> str:
    return date.isoformat()


def to_posix(date: _dt.datetime) -> int:
    return int(date.timestamp())


def from_github_to_internal(date: str) -> str:
    return to_internal(from_github(date))


def from_now_to_internal(time: bool = False) -> str:
    return to_internal(date=from_now(), time=time)
