from typing import Any

from insmav.domain.versioned_state import VersionedState


class ParamsState(VersionedState):
    def __init__(self) -> None:
        super().__init__()
        self._params: dict[str, dict[str, Any]] = {}

    def set_param(
        self,
        name: str,
        value: float,
        status: str = "idle",
        param_type: int | None = None,
    ) -> None:
        with self._lock:
            existing = self._params.get(name, {})

            self._params[name] = {
                "name": name,
                "value": value,
                "status": status,
                "type": param_type if param_type is not None else existing.get("type"),
            }
            self._mark_updated()

    def set_param_status(self, name: str, status: str) -> None:
        with self._lock:
            existing = self._params.get(name)

            if existing is None:
                self._params[name] = {
                    "name": name,
                    "value": None,
                    "status": status,
                    "type": None,
                }
            else:
                existing["status"] = status

            self._mark_updated()

    def read_params(self) -> dict[str, dict[str, Any]]:
        with self._lock:
            return {
                key: dict(value)
                for key, value in self._params.items()
            }

    def try_read_params(self, reader_id: str) -> dict[str, dict[str, Any]] | None:
        with self._lock:
            if self._is_fresh_for(reader_id):
                return None

            snapshot = {
                key: dict(value)
                for key, value in self._params.items()
            }
            self._mark_read(reader_id)
            return snapshot