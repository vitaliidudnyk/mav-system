from collections import deque
from typing import Any

from insmav.domain.versioned_state import VersionedState


class TelemetryState(VersionedState):
    def __init__(self, limit: int = 300) -> None:
        super().__init__()
        self._telemetry = deque(maxlen=limit)

    def add_telemetry(self, message: Any) -> None:
        with self._lock:
            self._telemetry.append(message)
            self._mark_updated()

    def read_telemetry(self) -> list[Any]:
        with self._lock:
            return list(self._telemetry)

    def try_read_telemetry(self, reader_id: str) -> list[Any] | None:
        with self._lock:
            if self._is_fresh_for(reader_id):
                return None

            snapshot = list(self._telemetry)
            self._mark_read(reader_id)
            return snapshot