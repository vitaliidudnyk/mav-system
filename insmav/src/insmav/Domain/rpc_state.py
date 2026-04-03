import time
from collections import deque
from typing import Any

from insmav.domain.versioned_state import VersionedState


class RpcState(VersionedState):
    def __init__(self, limit: int = 100) -> None:
        super().__init__()
        self._rpc_history = deque(maxlen=limit)
        self._rpc_ack_history = deque(maxlen=limit)
        self._rpc_statuses: dict[int, dict[str, Any]] = {}
        self._rpc_sequence = 0

    def add_rpc_request(
        self,
        command: int,
        command_name: str,
        event_name: str,
        params: list[float],
        status: str = "pending",
    ) -> int:
        with self._lock:
            self._rpc_sequence += 1
            rpc_id = self._rpc_sequence
            now = time.time()

            entry = {
                "rpc_id": rpc_id,
                "command": command,
                "command_name": command_name,
                "event_name": event_name,
                "params": list(params),
                "status": status,
                "created_at": now,
                "updated_at": now,
                "ack_result": None,
            }

            self._rpc_history.append(entry)
            self._rpc_statuses[rpc_id] = dict(entry)
            self._mark_updated()

            return rpc_id

    def set_rpc_status(
        self,
        rpc_id: int,
        status: str,
        ack_result: int | None = None,
    ) -> None:
        with self._lock:
            existing = self._rpc_statuses.get(rpc_id)

            if existing is None:
                return

            existing["status"] = status
            existing["ack_result"] = ack_result
            existing["updated_at"] = time.time()

            for item in reversed(self._rpc_history):
                if item["rpc_id"] == rpc_id:
                    item["status"] = status
                    item["ack_result"] = ack_result
                    item["updated_at"] = existing["updated_at"]
                    break

            self._mark_updated()

    def add_rpc_ack(self, message: Any) -> None:
        with self._lock:
            now = time.time()

            entry = {
                "command": message.command,
                "result": getattr(message, "result", None),
                "created_at": now,
            }

            self._rpc_ack_history.append(entry)

            for rpc_id in sorted(self._rpc_statuses.keys(), reverse=True):
                rpc_entry = self._rpc_statuses[rpc_id]

                if rpc_entry["command"] != message.command:
                    continue

                if rpc_entry["status"] != "pending":
                    continue

                rpc_entry["status"] = "acked"
                rpc_entry["ack_result"] = getattr(message, "result", None)
                rpc_entry["updated_at"] = now

                for item in reversed(self._rpc_history):
                    if item["rpc_id"] == rpc_id:
                        item["status"] = rpc_entry["status"]
                        item["ack_result"] = rpc_entry["ack_result"]
                        item["updated_at"] = rpc_entry["updated_at"]
                        break

                break

            self._mark_updated()

    def read_rpc_history(self) -> list[dict[str, Any]]:
        with self._lock:
            return [dict(item) for item in self._rpc_history]

    def read_rpc_ack_history(self) -> list[dict[str, Any]]:
        with self._lock:
            return [dict(item) for item in self._rpc_ack_history]

    def read_rpc_statuses(self) -> dict[int, dict[str, Any]]:
        with self._lock:
            return {
                key: dict(value)
                for key, value in self._rpc_statuses.items()
            }

    def try_read_rpc_history(self, reader_id: str) -> list[dict[str, Any]] | None:
        scoped_reader_id = f"{reader_id}:history"

        with self._lock:
            if self._is_fresh_for(scoped_reader_id):
                return None

            snapshot = [dict(item) for item in self._rpc_history]
            self._mark_read(scoped_reader_id)
            return snapshot

    def try_read_rpc_ack_history(
        self,
        reader_id: str,
    ) -> list[dict[str, Any]] | None:
        scoped_reader_id = f"{reader_id}:ack_history"

        with self._lock:
            if self._is_fresh_for(scoped_reader_id):
                return None

            snapshot = [dict(item) for item in self._rpc_ack_history]
            self._mark_read(scoped_reader_id)
            return snapshot

    def try_read_rpc_statuses(
        self,
        reader_id: str,
    ) -> dict[int, dict[str, Any]] | None:
        scoped_reader_id = f"{reader_id}:statuses"

        with self._lock:
            if self._is_fresh_for(scoped_reader_id):
                return None

            snapshot = {
                key: dict(value)
                for key, value in self._rpc_statuses.items()
            }
            self._mark_read(scoped_reader_id)
            return snapshot