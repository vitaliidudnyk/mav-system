from insmav.streams.params.param_name import normalize_param_name


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
        normalized_name = normalize_param_name(name)
        self._pending_reads.add(normalized_name)

    def confirm_read(self, name: str) -> bool:
        normalized_name = normalize_param_name(name)

        if normalized_name not in self._pending_reads:
            return False

        self._pending_reads.remove(normalized_name)
        return True

    def add_set(self, name: str, value: float) -> None:
        normalized_name = normalize_param_name(name)
        self._pending_sets[normalized_name] = value

    def confirm_set(self, name: str, value: float) -> bool:
        normalized_name = normalize_param_name(name)

        if normalized_name not in self._pending_sets:
            return False

        expected_value = self._pending_sets[normalized_name]

        if expected_value != value:
            return False

        del self._pending_sets[normalized_name]
        return True