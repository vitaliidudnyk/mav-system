class PendingParams:
    def __init__(self):
        self._request_all_pending = False
        self._pending_reads = set()
        self._pending_sets = {}

    def mark_request_all(self) -> None:
        self._request_all_pending = True

    def clear_request_all(self) -> None:
        self._request_all_pending = False

    def is_request_all_pending(self) -> bool:
        return self._request_all_pending

    def add_read(self, name: str) -> None:
        self._pending_reads.add(name)

    def confirm_read(self, name: str) -> bool:
        if name not in self._pending_reads:
            return False

        self._pending_reads.remove(name)
        return True

    def add_set(self, name: str, value: float) -> None:
        self._pending_sets[name] = value

    def confirm_set(self, name: str, value: float) -> bool:
        if name not in self._pending_sets:
            return False

        expected_value = self._pending_sets[name]

        if expected_value != value:
            return False

        del self._pending_sets[name]
        return True