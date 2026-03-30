from abc import ABC, abstractmethod


class BaseHandler(ABC):
    @property
    def message_type(self) -> str:
        pass

    def register(self, mavlink_receiver) -> None:
        mavlink_receiver.subscribe(self.message_type, self.handle)

        print(
            f"[handler][{self.__class__.__name__}][register] "
            f"Subscribed to {self.message_type}"
        )

    @abstractmethod
    def handle(self, message) -> None:
        pass