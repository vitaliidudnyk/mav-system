from collections import deque
from typing import Any

from insmav.domain.versioned_state import VersionedState


class DatasetsState(VersionedState):
    def __init__(self, dataset_limit: int = 300) -> None:
        super().__init__()
        self._datasets: dict[str, deque] = {}
        self._dataset_limit = dataset_limit

    def add_dataset(self, dataset_type: str, dataset: Any) -> None:
        with self._lock:
            if dataset_type not in self._datasets:
                self._datasets[dataset_type] = deque(maxlen=self._dataset_limit)

            self._datasets[dataset_type].append(dataset)
            self._mark_updated()

    def read_datasets(self) -> dict[str, list[Any]]:
        with self._lock:
            return {
                key: list(value)
                for key, value in self._datasets.items()
            }

    def try_read_datasets(self, reader_id: str) -> dict[str, list[Any]] | None:
        with self._lock:
            if self._is_fresh_for(reader_id):
                return None

            snapshot = {
                key: list(value)
                for key, value in self._datasets.items()
            }
            self._mark_read(reader_id)
            return snapshot