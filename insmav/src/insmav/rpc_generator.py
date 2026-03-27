import random
import threading
import time
from dataclasses import fields

from src.insmav.rpc.rpc_creator import RpcCreator
from src.insmav.rpc.rpc_events import (
    CalibrateImuEvent,
    SetModeEvent,
    StartMissionEvent,
)


class RpcGenerator:
    def __init__(self, rpc_creator: RpcCreator):
        self._rpc_creator = rpc_creator
        self._is_running = False

    def start(self) -> None:
        if self._is_running:
            return

        self._is_running = True
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self) -> None:
        while self._is_running:
            event = self._create_random_event()
            print(f"[RpcGenerator] Sending: {event}")
            self._rpc_creator.send(event)

            delay = random.randint(1, 5)
            time.sleep(delay)

    @staticmethod
    def _create_random_event():
        event_type = random.choice(
            [
                StartMissionEvent,
                SetModeEvent,
                CalibrateImuEvent,
            ]
        )

        # отримуємо кількість полів у dataclass
        field_count = len(fields(event_type))

        values = [
            random.uniform(0.0, 10.0)
            for _ in range(field_count)
        ]

        return event_type(*values)