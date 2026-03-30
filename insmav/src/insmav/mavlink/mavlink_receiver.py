from collections import defaultdict

from insmav.mavlink.mavlink_config import mavutil


class MavlinkReceiver:
    def __init__(self):
        self._parser = mavutil.mavlink.MAVLink(None)
        self._subscribers = defaultdict(list)
        self._fallback_subscribers = []

        print("[mavlink][MavlinkReceiver][__init__] Initialized")

    def subscribe(self, message_type: str, callback) -> None:
        self._subscribers[message_type].append(callback)

        print(
            f"[mavlink][MavlinkReceiver][subscribe] "
            f"type={message_type} callbacks={len(self._subscribers[message_type])}"
        )

    def subscribe_fallback(self, callback) -> None:
        self._fallback_subscribers.append(callback)

        print(
            f"[mavlink][MavlinkReceiver][subscribe_fallback] "
            f"callbacks={len(self._fallback_subscribers)}"
        )

    def handle_bytes(self, data: bytes) -> None:
        for byte in data:
            message = self._parser.parse_char(bytes([byte]))

            if message is None:
                continue

            self._handle_message(message)

    def _handle_message(self, message) -> None:
        message_type = message.get_type()
        callbacks = self._subscribers.get(message_type)

        if callbacks:
            print(
                f"[mavlink][MavlinkReceiver][_handle_message] "
                f"type={message_type} subscribers={len(callbacks)}"
            )

            for callback in callbacks:
                callback(message)

            return

        if self._fallback_subscribers:
            print(
                f"[mavlink][MavlinkReceiver][_handle_message] "
                f"type={message_type} -> fallback subscribers={len(self._fallback_subscribers)}"
            )

            for callback in self._fallback_subscribers:
                callback(message)

            return

        print(
            f"[mavlink][MavlinkReceiver][_handle_message] "
            f"No subscribers for type={message_type}"
        )