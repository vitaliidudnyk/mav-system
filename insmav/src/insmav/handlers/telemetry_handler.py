from src.insmav.handlers.base_handler import BaseHandler


class TelemetryHandler(BaseHandler):
    def handle(self, message) -> None:
        print(f"[Telemetry] {message}")