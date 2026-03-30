import threading
import time


class ParamRequestGenerator:
    def __init__(
        self,
        param_requester,
        interval_sec: float = 5.0,
    ) -> None:
        self._param_requester = param_requester
        self._interval_sec = interval_sec
        self._stop_event = threading.Event()

        self._step = 0

        # тестові дані (можеш замінити)
        self._param_name = "camera_pitch_deg"
        self._set_value = 20.0
        self._param_type = 9  # MAV_PARAM_TYPE_REAL32

    def start(self) -> None:
        print("[params][ParamRequestGenerator][start] Started")

        while not self._stop_event.is_set():
            try:
                self._tick()
            except Exception as error:
                print(
                    "[params][ParamRequestGenerator][start] "
                    f"Error: {error}"
                )

            self._stop_event.wait(self._interval_sec)

        print("[params][ParamRequestGenerator][start] Stopped")

    def stop(self) -> None:
        self._stop_event.set()

    # --- internal ---

    def _tick(self) -> None:
        if self._step == 0:
            print("[params][Generator] -> request_all")
            self._param_requester.request_all()

        elif self._step == 1:
            print(f"[params][Generator] -> request_param {self._param_name}")
            self._param_requester.request_param(self._param_name)

        elif self._step == 2:
            print(
                f"[params][Generator] -> set_param "
                f"{self._param_name}={self._set_value}"
            )
            self._param_requester.set_param(
                name=self._param_name,
                value=self._set_value,
                param_type=self._param_type,
            )

            self._set_value += 5

        # move to next step (0 → 1 → 2 → 0 ...)
        self._step = (self._step + 1) % 3