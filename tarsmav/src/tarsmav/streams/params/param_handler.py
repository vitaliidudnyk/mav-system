from tarsmav.mavlink.mavlink_config import mavutil


class ParamHandler:
    def __init__(self, mavlink_sender, param_store):
        self._mavlink_transmitter = mavlink_sender
        self._param_store = param_store

        print("[params][ParamHandler][__init__] Initialized")

    def register(self, mavlink_receiver) -> None:
        mavlink_receiver.subscribe("PARAM_REQUEST_LIST", self.handle_request_list)
        mavlink_receiver.subscribe("PARAM_REQUEST_READ", self.handle_request_read)
        mavlink_receiver.subscribe("PARAM_SET", self.handle_set)

        print("[params][ParamHandler][register] Subscribed to PARAM_* messages")

    def handle_request_list(self, _message) -> None:
        print("[params][ParamHandler][handle_request_list] -> PARAM_REQUEST_LIST")

        params = self._param_store.get_all()
        param_count = len(params)

        for index, param in enumerate(params):
            self._send_param_value(
                name=param["name"],
                value=param["value"],
                param_type=param["type"],
                param_count=param_count,
                param_index=index,
            )

    def handle_request_read(self, message) -> None:
        print("[params][ParamHandler][handle_request_read] -> PARAM_REQUEST_READ")

        name = self._extract_param_name(message)
        param = self._param_store.get_by_name(name)

        if param is None:
            print(
                f"[params][ParamHandler][handle_request_read] "
                f"Param not found: {name}"
            )
            return

        params = self._param_store.get_all()
        param_index = self._param_store.get_index_by_name(name)

        self._send_param_value(
            name=param["name"],
            value=param["value"],
            param_type=param["type"],
            param_count=len(params),
            param_index=param_index,
        )

    def handle_set(self, message) -> None:
        print("[params][ParamHandler][handle_set] -> PARAM_SET")

        name = self._extract_param_name(message)
        new_value = message.param_value

        old_param = self._param_store.get_by_name(name)
        old_value = old_param["value"] if old_param else None

        param = self._param_store.update(name, new_value)

        if param is None:
            print(f"[params][ParamHandler][handle_set] Param not found: {name}")
            return

        print(
            f"[params][ParamHandler][handle_set] UPDATED "
            f"{name}: {old_value} -> {param['value']}"
        )

        params = self._param_store.get_all()
        param_index = self._param_store.get_index_by_name(name)

        self._send_param_value(
            name=param["name"],
            value=param["value"],
            param_type=param["type"],
            param_count=len(params),
            param_index=param_index,
        )

    def _send_param_value(
        self,
        name: str,
        value: float,
        param_type: int,
        param_count: int,
        param_index: int,
    ) -> None:
        message = mavutil.mavlink.MAVLink_param_value_message(
            param_id=name.encode("utf-8"),
            param_value=value,
            param_type=param_type,
            param_count=param_count,
            param_index=param_index,
        )

        print(
            f"[params][ParamHandler][_send_param_value] "
            f"{name}={value} index={param_index}/{param_count}"
        )
        self._mavlink_transmitter.send(message)

    @staticmethod
    def _extract_param_name(message) -> str:
        raw_name = message.param_id

        if isinstance(raw_name, bytes):
            return raw_name.decode("utf-8", errors="ignore").rstrip("\x00")

        return str(raw_name).rstrip("\x00")