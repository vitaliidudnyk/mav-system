from src.insmav.handlers.base_handler import BaseHandler


class DatasetHandler(BaseHandler):
    def handle(self, message) -> None:
        print(f"[Dataset] {message}")