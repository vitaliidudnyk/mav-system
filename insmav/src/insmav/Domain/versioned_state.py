import threading


class VersionedState:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._version = 0
        self._reader_versions: dict[str, int] = {}

    def _mark_updated(self) -> None:
        self._version += 1

    def _is_fresh_for(self, reader_id: str) -> bool:
        return self._reader_versions.get(reader_id) == self._version

    def _mark_read(self, reader_id: str) -> None:
        self._reader_versions[reader_id] = self._version