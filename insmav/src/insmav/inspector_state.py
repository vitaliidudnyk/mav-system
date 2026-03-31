import threading
import time
from collections import deque
from typing import Any, Dict, List


class InspectorState:
    def __init__(
        self,
        telemetry_limit: int = 300,
        dataset_limit: int = 300,
        logs_limit: int = 100,
        rpc_limit: int = 100,
    ):
        self._lock = threading.Lock()

        # --- telemetry ---
        self._telemetry = deque(maxlen=telemetry_limit)

        # --- datasets ---
        self._datasets: Dict[str, deque] = {}
        self._dataset_limit = dataset_limit

        # --- params ---
        self._params: Dict[str, Dict[str, Any]] = {}

        # --- logs ---
        self._logs = deque(maxlen=logs_limit)

        # --- rpc ---
        self._rpc_history = deque(maxlen=rpc_limit)
        self._rpc_ack_history = deque(maxlen=rpc_limit)
        self._rpc_statuses: Dict[int, Dict[str, Any]] = {}
        self._rpc_sequence = 0

    # =========================
    # WRITE API
    # =========================

    def add_telemetry(self, message: Any) -> None:
        with self._lock:
            self._telemetry.append(message)

    def add_dataset(self, dataset_type: str, dataset: Any) -> None:
        with self._lock:
            if dataset_type not in self._datasets:
                self._datasets[dataset_type] = deque(maxlen=self._dataset_limit)

            self._datasets[dataset_type].append(dataset)

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
                return

            existing["status"] = status

    def add_log(self, text: str) -> None:
        with self._lock:
            self._logs.append(text)

    def add_rpc_request(
        self,
        command: int,
        command_name: str,
        event_name: str,
        params: List[float],
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

    # =========================
    # READ API (snapshots)
    # =========================

    def get_telemetry(self) -> List[Any]:
        with self._lock:
            return list(self._telemetry)

    def get_datasets(self) -> Dict[str, List[Any]]:
        with self._lock:
            return {
                key: list(value)
                for key, value in self._datasets.items()
            }

    def get_params(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            return {
                key: dict(value)
                for key, value in self._params.items()
            }

    def get_logs(self) -> List[str]:
        with self._lock:
            return list(self._logs)

    def get_rpc_history(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [dict(item) for item in self._rpc_history]

    def get_rpc_ack_history(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [dict(item) for item in self._rpc_ack_history]

    def get_rpc_statuses(self) -> Dict[int, Dict[str, Any]]:
        with self._lock:
            return {
                key: dict(value)
                for key, value in self._rpc_statuses.items()
            }