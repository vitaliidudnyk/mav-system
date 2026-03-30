from dataclasses import fields

from pymavlink import mavutil

from tarsmav.streams.rpc.rpc_mapping import RPC_EVENT_MAPPING


class RpcCommandHandler:
    def __init__(self, mavlink_transmitter):
        self._subscribers = []
        self._mavlink_transmitter = mavlink_transmitter

    def register(self, mavlink_receiver) -> None:
        mavlink_receiver.subscribe("COMMAND_LONG", self.handle_command_long)

        print("[rpc][RpcCommandHandler][register] Subscribed to COMMAND_LONG")

    def subscribe(self, callback) -> None:
        self._subscribers.append(callback)

    def handle_command_long(self, message) -> None:
        print("[rpc][RpcCommandHandler][handle_command_long] -> COMMAND_LONG")

        command = message.command
        event_class = RPC_EVENT_MAPPING.get(command)

        if event_class is None:
            print(
                f"[rpc][RpcCommandHandler][handle_command_long] "
                f"Unsupported command={command}"
            )
            self._send_ack(command, mavutil.mavlink.MAV_RESULT_UNSUPPORTED)
            return

        try:
            all_params = [
                message.param1,
                message.param2,
                message.param3,
                message.param4,
                message.param5,
                message.param6,
                message.param7,
            ]

            field_count = len(fields(event_class))
            event = event_class(*all_params[:field_count])

            self._emit(command, event)

            self._send_ack(command, mavutil.mavlink.MAV_RESULT_ACCEPTED)

        except Exception as error:
            print(
                f"[rpc][RpcCommandHandler][handle_command_long] "
                f"Failed to handle command={command}: {error}"
            )
            self._send_ack(command, mavutil.mavlink.MAV_RESULT_FAILED)

    def _emit(self, command: int, event) -> None:
        for callback in self._subscribers:
            callback(command, event)

    def _send_ack(self, command: int, result: int) -> None:
        ack = mavutil.mavlink.MAVLink_command_ack_message(
            command=command,
            result=result,
        )

        self._mavlink_transmitter.send(ack)