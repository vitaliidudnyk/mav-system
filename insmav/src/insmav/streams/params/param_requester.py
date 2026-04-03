from insmav.mavlink.mavlink_config import mavutil
from insmav.streams.params.param_name import normalize_param_name


class ParamRequester:
    def __init__(
        self,
        mavlink_sender,
        pending_params,
    ):
        self._mavlink_sender = mavlink_sender
        self._pending_params = pending_params

    def request_all(self) -> None:
        self._pending_params.mark_request_all()

        message = mavutil.mavlink.MAVLink_param_request_list_message(
            target_system=1,
            target_component=1,
        )

        print("[params][ParamRequester][request_all] -> PARAM_REQUEST_LIST")
        self._mavlink_sender.send(message)

    def request_param(self, name: str) -> None:
        normalized_name = normalize_param_name(name)
        self._pending_params.add_read(normalized_name)

        message = mavutil.mavlink.MAVLink_param_request_read_message(
            target_system=1,
            target_component=1,
            param_id=normalized_name.encode("utf-8"),
            param_index=-1,
        )

        print(
            f"[params][ParamRequester][request_param] -> PARAM_REQUEST_READ "
            f"{normalized_name}"
        )
        self._mavlink_sender.send(message)

    def set_param(self, name: str, value: float, param_type: int) -> None:
        normalized_name = normalize_param_name(name)
        self._pending_params.add_set(normalized_name, value)

        message = mavutil.mavlink.MAVLink_param_set_message(
            target_system=1,
            target_component=1,
            param_id=normalized_name.encode("utf-8"),
            param_value=value,
            param_type=param_type,
        )

        print(
            f"[params][ParamRequester][set_param] -> PARAM_SET "
            f"{normalized_name}={value}"
        )
        self._mavlink_sender.send(message)