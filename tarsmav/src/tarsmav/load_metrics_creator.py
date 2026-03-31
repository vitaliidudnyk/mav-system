import time

from tarsmav.streams.custom_data.custom_data_creator import CustomDataCreator
from tarsmav.mavlink.sender_monitor import SenderMonitor
from tarsmav.streams.custom_data.custom_data_sets import SenderSnapshot


class LoadMetricsCreator:
    def __init__(
        self,
        custom_data_creator: CustomDataCreator,
        sender_monitor: SenderMonitor,
        rate_hz: float = 1.0,
    ):
        self._custom_data_creator = custom_data_creator
        self._monitor = sender_monitor
        self._rate_hz = rate_hz
        self._last_sent_at = 0.0

    def tick(self) -> None:
        now = time.monotonic()
        period_s = 1.0 / self._rate_hz

        if now - self._last_sent_at < period_s:
            return

        snapshot = SenderSnapshot(
            dropped_logs_total=self._monitor.get_dropped_logs_total(),
            dropped_custom_total=self._monitor.get_dropped_custom_total(),
            avg_load_pct=self._monitor.get_avg_load_pct(),
            high_load_time_pct=self._monitor.get_high_load_time_pct(),
            sent_bytes_per_sec=self._monitor.get_sent_bytes_per_sec(),
            sent_messages_per_sec=self._monitor.get_sent_messages_per_sec(),
        )

        self._custom_data_creator.send(snapshot)
        self._last_sent_at = now