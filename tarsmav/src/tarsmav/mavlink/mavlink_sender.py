import threading

from tarsmav.mavlink.interfaces import ISenderMonitor
from tarsmav.mavlink.mavlink_config import mavutil
from tarsmav.mavlink._sender_monitor import SenderMonitor
from tarsmav.mavlink.sender_policy import MessagePriority
from tarsmav.mavlink.sender_policy import SenderPolicy


class MavLinkSender:
    def __init__(self, writer, policy: SenderPolicy | None = None):
        self._mav = mavutil.mavlink.MAVLink(None)
        self._writer = writer
        self._policy = policy or SenderPolicy()
        self._monitor = SenderMonitor(
            max_messages_per_sec=self._policy.max_messages_per_sec,
            max_bytes_per_sec=self._policy.max_bytes_per_sec,
        )
        self._lock = threading.Lock()

        print("[mavlink][MavLinkSender][__init__] Initialized")

    @property
    def monitor(self) -> ISenderMonitor:
        return self._monitor

    def send(self, message) -> bool:
        with self._lock:
            message_type = message.get_type()
            priority = self._policy.get_priority(message_type)

            data = message.pack(self._mav)
            size_bytes = len(data)

            if self._should_drop(priority=priority, size_bytes=size_bytes):
                self._monitor.register_drop(message_type)

                print(
                    f"[mavlink][MavLinkSender][send][warning] "
                    f"Dropped message type={message_type} "
                    f"priority={priority.name} size={size_bytes}"
                )
                return False

            self._writer(data)
            self._monitor.register_sent(size_bytes)

            if self._monitor.should_warn_high_load():
                print(
                    f"[mavlink][MavLinkSender][send][warning] "
                    f"High load detected: "
                    f"avg_load_pct={self._monitor.get_avg_load_pct():.1f}, "
                    f"high_load_time_pct={self._monitor.get_high_load_time_pct():.1f}, "
                    f"sent_bytes_per_sec={self._monitor.get_sent_bytes_per_sec():.1f}, "
                    f"sent_messages_per_sec={self._monitor.get_sent_messages_per_sec():.1f}"
                )

            return True

    def _should_drop(self, priority: MessagePriority, size_bytes: int) -> bool:
        if priority == MessagePriority.CRITICAL:
            return False

        current_messages = self._monitor.get_current_messages_per_sec()
        current_bytes = self._monitor.get_current_bytes_per_sec()

        exceeds_messages_limit = (
            current_messages >= self._policy.max_messages_per_sec
        )
        exceeds_bytes_limit = (
            current_bytes + size_bytes > self._policy.max_bytes_per_sec
        )

        if priority == MessagePriority.LOW:
            return exceeds_messages_limit or exceeds_bytes_limit

        return False