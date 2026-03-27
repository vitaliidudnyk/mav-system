from src.insmav.handlers.base_handler import BaseHandler


class LogHandler(BaseHandler):
    def handle(self, message) -> None:
        print(f"[Log] {message}")