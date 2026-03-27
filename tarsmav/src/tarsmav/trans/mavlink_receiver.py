from ..mavlink_config import mavutil


class MavLinkReceiver:
    def __init__(self, rpc_command_handler):
        self._mav = mavutil.mavlink.MAVLink(None)
        self._rpc_command_handler = rpc_command_handler
        print("[mavlink][MavLinkReceiver][__init__] Initialized")

    def feed(self, data: bytes) -> None:
        for byte in data:
            message = self._mav.parse_char(bytes([byte]))

            if message is None:
                continue

            self._handle_message(message)

    def _handle_message(self, message) -> None:
        print(f"[mavlink][MavLinkReceiver][_handle_message] type={message.get_type()}")
        if message.get_type() == "COMMAND_LONG":
            print("[mavlink][MavLinkReceiver][_handle_message] -> RPC COMMAND_LONG")
            self._rpc_command_handler.handle_command_long(message)