from dataclasses import astuple

from pymavlink import mavutil

from insmav.streams.rpc.rpc_events import RpcEvent


class RpcCreator:
    _PARAMS_COUNT = 7

    def __init__(
        self,
        mavlink_sender,
        rpc_event_mapping: dict[int, type[RpcEvent]],
        target_system: int = 1,
        target_component: int = 1,
        confirmation: int = 0,
    ):
        self._mavlink_sender = mavlink_sender
        self._rpc_event_mapping = rpc_event_mapping
        self._target_system = target_system
        self._target_component = target_component
        self._confirmation = confirmation

    def send(self, event: RpcEvent) -> None:
        command = self._find_command(event)
        params = list(self._extract_params(event))

        while len(params) < self._PARAMS_COUNT:
            params.append(0.0)

        message = mavutil.mavlink.MAVLink_command_long_message(
            target_system=self._target_system,
            target_component=self._target_component,
            command=command,
            confirmation=self._confirmation,
            param1=params[0],
            param2=params[1],
            param3=params[2],
            param4=params[3],
            param5=params[4],
            param6=params[5],
            param7=params[6],
        )

        self._mavlink_sender.send(message)

    def _find_command(self, event: RpcEvent) -> int:
        event_type = type(event)

        for command, mapped_event_type in self._rpc_event_mapping.items():
            if mapped_event_type is event_type:
                return command

        raise ValueError(
            f"No RPC command mapping found for event type: {event_type.__name__}"
        )

    def _extract_params(self, event: RpcEvent) -> tuple[float, ...]:
        params = astuple(event)

        if len(params) > self._PARAMS_COUNT:
            raise ValueError(
                f"{type(event).__name__} has too many params: {len(params)}"
            )

        return params