from collections import defaultdict

from tarsmav.mavlink.mavlink_config import mavutil


class MavLinkReceiver:
    def __init__(self):
        self._mav = mavutil.mavlink.MAVLink(None)
        self._subscribers = defaultdict(list)

        print("[mavlink][MavLinkReceiver][__init__] Initialized")

    def subscribe(self, message_type: str, callback) -> None:
        self._subscribers[message_type].append(callback)

        print(
            f"[mavlink][MavLinkReceiver][subscribe] "
            f"type={message_type} callbacks={len(self._subscribers[message_type])}"
        )

    def feed(self, data: bytes) -> None:
        for byte in data:
            message = self._mav.parse_char(bytes([byte]))

            if message is None:
                continue

            self._dispatch(message)

    def _dispatch(self, message) -> None:
        message_type = message.get_type()

        print(
            f"[mavlink][MavLinkReceiver][_dispatch] "
            f"type={message_type}"
        )

        callbacks = self._subscribers.get(message_type)

        if not callbacks:
            print(
                f"[mavlink][MavLinkReceiver][_dispatch] "
                f"No subscribers for type={message_type}"
            )
            return

        for callback in callbacks:
            callback(message)