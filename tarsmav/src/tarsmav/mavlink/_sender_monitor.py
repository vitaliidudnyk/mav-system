import time
from collections import deque


class SenderMonitor:
    def __init__(
        self,
        max_messages_per_sec: int,
        max_bytes_per_sec: int,
        high_load_threshold_pct: float = 80.0,
        window_seconds: float = 10.0,
    ):
        self._max_messages_per_sec = max_messages_per_sec
        self._max_bytes_per_sec = max_bytes_per_sec
        self._high_load_threshold_pct = high_load_threshold_pct
        self._window_seconds = window_seconds

        self._sent_events: deque[tuple[float, int]] = deque()
        self._load_samples: deque[tuple[float, float]] = deque()

        self._dropped_logs_total = 0
        self._dropped_custom_total = 0

        self._last_warning_at = 0.0
        self._warning_interval_s = 1.0

    def register_sent(self, size_bytes: int) -> None:
        now = time.monotonic()

        self._cleanup(now)
        self._sent_events.append((now, size_bytes))
        self._load_samples.append((now, self._calculate_current_load_pct()))

    def register_drop(self, message_type: str) -> None:
        if message_type == "LOG_DATA":
            self._dropped_logs_total += 1
            return

        if message_type == "DEBUG_FLOAT_ARRAY":
            self._dropped_custom_total += 1

    def should_warn_high_load(self) -> bool:
        now = time.monotonic()

        self._cleanup(now)

        if self._calculate_current_load_pct() < self._high_load_threshold_pct:
            return False

        if now - self._last_warning_at < self._warning_interval_s:
            return False

        self._last_warning_at = now
        return True

    def get_dropped_logs_total(self) -> int:
        return self._dropped_logs_total

    def get_dropped_custom_total(self) -> int:
        return self._dropped_custom_total

    def get_avg_load_pct(self) -> float:
        now = time.monotonic()
        self._cleanup(now)

        if not self._load_samples:
            return 0.0

        total = sum(load_pct for _, load_pct in self._load_samples)
        return total / len(self._load_samples)

    def get_high_load_time_pct(self) -> float:
        now = time.monotonic()
        self._cleanup(now)

        if not self._load_samples:
            return 0.0

        high_load_samples = sum(
            1
            for _, load_pct in self._load_samples
            if load_pct >= self._high_load_threshold_pct
        )

        return high_load_samples / len(self._load_samples) * 100.0

    def get_sent_bytes_per_sec(self) -> float:
        now = time.monotonic()
        self._cleanup(now)

        sent_bytes = sum(size_bytes for _, size_bytes in self._sent_events)
        return sent_bytes / self._window_seconds

    def get_sent_messages_per_sec(self) -> float:
        now = time.monotonic()
        self._cleanup(now)

        sent_messages = len(self._sent_events)
        return sent_messages / self._window_seconds

    def get_current_messages_per_sec(self) -> int:
        now = time.monotonic()
        self._cleanup(now)
        return len(self._sent_events)

    def get_current_bytes_per_sec(self) -> int:
        now = time.monotonic()
        self._cleanup(now)
        return sum(size_bytes for _, size_bytes in self._sent_events)

    def _cleanup(self, now: float) -> None:
        sent_cutoff = now - 1.0
        while self._sent_events and self._sent_events[0][0] < sent_cutoff:
            self._sent_events.popleft()

        load_cutoff = now - self._window_seconds
        while self._load_samples and self._load_samples[0][0] < load_cutoff:
            self._load_samples.popleft()

    def _calculate_current_load_pct(self) -> float:
        current_messages = len(self._sent_events)
        current_bytes = sum(size_bytes for _, size_bytes in self._sent_events)

        messages_load_pct = (
            current_messages / self._max_messages_per_sec * 100.0
            if self._max_messages_per_sec > 0
            else 0.0
        )
        bytes_load_pct = (
            current_bytes / self._max_bytes_per_sec * 100.0
            if self._max_bytes_per_sec > 0
            else 0.0
        )

        return max(messages_load_pct, bytes_load_pct)