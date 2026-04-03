from collections import deque

from insmav.domain.versioned_state import VersionedState


class LogsState(VersionedState):
    def __init__(self, limit: int = 100) -> None:
        super().__init__()
        self._logs = deque(maxlen=limit)

    def add_log(self, text: str) -> None:
        with self._lock:
            self._logs.append(text)
            self._mark_updated()

    def read_logs(self) -> list[str]:
        with self._lock:
            return list(self._logs)

    def try_read_logs(self, reader_id: str) -> list[str] | None:
        with self._lock:
            if self._is_fresh_for(reader_id):
                return None

            snapshot = list(self._logs)
            self._mark_read(reader_id)
            return snapshot