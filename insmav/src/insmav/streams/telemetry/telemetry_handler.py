from insmav.streams.shared.base_handler import BaseHandler


class TelemetryHandler(BaseHandler):
    def register(self, mavlink_receiver) -> None:
        mavlink_receiver.subscribe_fallback(self.handle)

        print(
            f"[handler][{self.__class__.__name__}][register] "
            f"Subscribed as fallback handler"
        )

    def handle(self, message) -> None:
        print(f"[Telemetry] {message}")