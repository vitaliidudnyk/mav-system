from ..mavlink_config import mavutil


class MavlinkReceiver:
    def __init__(
        self,
        telemetry_handler,
        dataset_handler,
        log_handler,
        ack_handler,
    ):
        self._telemetry_handler = telemetry_handler
        self._dataset_handler = dataset_handler
        self._log_handler = log_handler
        self._ack_handler = ack_handler
        self._parser = mavutil.mavlink.MAVLink(None)

        print("[mavlink][MavlinkReceiver][__init__] Initialized")

    def handle_bytes(self, data: bytes) -> None:
        for byte in data:
            message = self._parser.parse_char(bytes([byte]))

            if message is None:
                continue

            self._handle_message(message)

    def _handle_message(self, message) -> None:
        message_type = message.get_type()

        if message_type == "COMMAND_ACK":
            print("[mavlink][MavlinkReceiver][_handle_message] -> ACK")
            self._ack_handler.handle(message)
            return

        if message_type == "DEBUG_FLOAT_ARRAY":
            print("[mavlink][MavlinkReceiver][_handle_message] -> DATASET")
            self._dataset_handler.handle(message)
            return

        if message_type == "LOG_DATA":
            print("[mavlink][MavlinkReceiver][_handle_message] -> LOG")
            self._log_handler.handle(message)
            return

        print("[mavlink][MavlinkReceiver][_handle_message] -> TELEMETRY")
        self._telemetry_handler.handle(message)