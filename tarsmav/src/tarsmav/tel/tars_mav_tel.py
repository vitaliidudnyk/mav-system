import time

from tarsmav.tel.mav_data import MavData
from tarsmav.tel.mav_message_factory import MavMessageFactory
from tarsmav.tel.mav_message_type import MavMessageType
from tarsmav.trans.mav_transmitter import MavTransmitter


class TarsMavTel:
    def __init__(self, transmitter: MavTransmitter):
        self.data = MavData()
        self._transmitter = transmitter

        self._rates_hz = {
            MavMessageType.HEARTBEAT: 1.0,
            MavMessageType.ATTITUDE: 10.0,
            MavMessageType.SYS_STATUS: 2.0,
        }

        self._last_sent_at = {
            MavMessageType.HEARTBEAT: 0.0,
            MavMessageType.ATTITUDE: 0.0,
            MavMessageType.SYS_STATUS: 0.0,
        }

    def tick(self) -> None:
        now = time.monotonic()

        for message_type, rate_hz in self._rates_hz.items():
            period_s = 1.0 / rate_hz

            if now - self._last_sent_at[message_type] < period_s:
                continue

            message = MavMessageFactory.create_message(message_type, self.data)
            self._transmitter.send(message)
            self._last_sent_at[message_type] = now

    def set_rate(self, message_type: MavMessageType, rate_hz: float) -> None:
        if rate_hz <= 0:
            raise ValueError("rate_hz must be > 0")

        self._rates_hz[message_type] = rate_hz