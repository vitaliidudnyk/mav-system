from dataclasses import dataclass
from threading import Event, Lock
from typing import Optional


@dataclass
class PendingCommand:
    command: int
    event: Event
    ack_message: object | None = None


class PendingCommands:
    def __init__(self):
        self._commands: dict[int, PendingCommand] = {}
        self._lock = Lock()

    def register(self, command: int) -> None:
        with self._lock:
            if command in self._commands:
                raise ValueError(f"Command {command} is already pending")

            self._commands[command] = PendingCommand(
                command=command,
                event=Event(),
            )

    def resolve(self, command: int, ack_message) -> bool:
        with self._lock:
            pending = self._commands.get(command)

            if pending is None:
                return False

            pending.ack_message = ack_message
            pending.event.set()
            return True

    def wait_for_ack(self, command: int, timeout: float) -> object | None:
        with self._lock:
            pending = self._commands.get(command)

            if pending is None:
                raise ValueError(f"Command {command} is not pending")

            wait_event = pending.event

        is_set = wait_event.wait(timeout)

        if not is_set:
            return None

        with self._lock:
            pending = self._commands.get(command)

            if pending is None:
                return None

            return pending.ack_message

    def clear(self, command: int) -> None:
        with self._lock:
            self._commands.pop(command, None)