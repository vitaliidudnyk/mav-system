import time

from tarsmav.mavlink.mavlink_config import mavutil
from tarsmav.mavlink.mavlink_sender import MavLinkSender
from tarsmav.streams.custom_data.custom_data_sets import DebugFloatDataset


class CustomDataCreator:
    _MAX_DATASET_LENGTH = 58
    _NAME_LENGTH = 10

    def __init__(self, transmitter: MavLinkSender):
        self._transmitter = transmitter
        self._next_array_id = 1

    def send(self, dataset: DebugFloatDataset) -> None:
        data = dataset.to_array()
        dataset_name = dataset.dataset_type.value

        if len(data) > self._MAX_DATASET_LENGTH:
            raise ValueError(
                f"Dataset '{dataset_name}' is too large: "
                f"{len(data)} > {self._MAX_DATASET_LENGTH}"
            )

        padded_data = data + [0.0] * (self._MAX_DATASET_LENGTH - len(data))

        message = mavutil.mavlink.MAVLink_debug_float_array_message(
            self._time_usec(),
            self._encode_name(dataset_name),
            self._next_id(),
            padded_data,
        )

        self._transmitter.send(message)

    def _next_id(self) -> int:
        current_id = self._next_array_id
        self._next_array_id += 1
        return current_id

    @staticmethod
    def _time_usec() -> int:
        return int(time.time() * 1_000_000)

    def _encode_name(self, name: str) -> bytes:
        encoded = name.encode("ascii", errors="ignore")[: self._NAME_LENGTH]
        return encoded.ljust(self._NAME_LENGTH, b"\x00")