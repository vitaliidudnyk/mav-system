from insmav.streams.shared.base_handler import BaseHandler


class ParamHandler(BaseHandler):
    def __init__(self, pending_params, state):
        self._pending_params = pending_params
        self._state = state

    @property
    def message_type(self) -> str:
        return "PARAM_VALUE"

    def handle(self, message) -> None:
        name = self._extract_param_name(message)
        value = message.param_value
        param_type = getattr(message, "param_type", None)

        if self._pending_params.confirm_set(name, value):
            print(
                f"[params][ParamHandler][handle] -> SET_CONFIRMED "
                f"{name}={value}"
            )

            self._state.set_param(
                name=name,
                value=value,
                status="confirmed",
                param_type=param_type,
            )
            return

        if self._pending_params.confirm_read(name):
            print(
                f"[params][ParamHandler][handle] -> VALUE_RECEIVED "
                f"{name}={value}"
            )

            self._state.set_param(
                name=name,
                value=value,
                status="idle",
                param_type=param_type,
            )
            return

        if self._pending_params.is_request_all_pending():
            print(
                f"[params][ParamHandler][handle] -> ALL_VALUE_RECEIVED "
                f"{name}={value}"
            )

            self._state.set_param(
                name=name,
                value=value,
                status="idle",
                param_type=param_type,
            )

            if getattr(message, "param_index", -1) == getattr(message, "param_count", -2) - 1:
                self._pending_params.clear_request_all()
                print("[params][ParamHandler][handle] -> REQUEST_ALL_COMPLETED")

            return

        print(f"[params][ParamHandler][handle] -> PARAM_VALUE {name}={value}")

        self._state.set_param(
            name=name,
            value=value,
            status="idle",
            param_type=param_type,
        )

    @staticmethod
    def _extract_param_name(message) -> str:
        raw_name = message.param_id

        if isinstance(raw_name, bytes):
            return raw_name.decode("utf-8", errors="ignore").rstrip("\x00")

        return str(raw_name).rstrip("\x00")