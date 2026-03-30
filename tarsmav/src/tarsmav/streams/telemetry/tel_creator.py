import time

from tarsmav.mavlink.mavlink_sender import MavLinkSender
from tarsmav.streams.telemetry.tel_data import TelData
from tarsmav.streams.telemetry.tel_message_factory import TelMessageFactory
from tarsmav.streams.telemetry.tel_message_type import TelMessageType
from tarsmav.streams.telemetry.tel_rates import DEFAULT_TEL_RATES_HZ


class TelCreator:
    def __init__(self, transmitter: MavLinkSender):
        self.data = TelData()
        self._transmitter = transmitter

        self._rates_hz = dict(DEFAULT_TEL_RATES_HZ)

        self._last_sent_at = {
            message_type: 0.0
            for message_type in self._rates_hz
        }

    def tick(self) -> None:
        now = time.monotonic()

        for message_type, rate_hz in self._rates_hz.items():
            period_s = 1.0 / rate_hz

            if now - self._last_sent_at[message_type] < period_s:
                continue

            message = TelMessageFactory.create_message(message_type, self.data)
            self._transmitter.send(message)
            self._last_sent_at[message_type] = now

    def set_rate(self, message_type: TelMessageType, rate_hz: float) -> None:
        if rate_hz <= 0:
            raise ValueError("rate_hz must be > 0")

        self._rates_hz[message_type] = rate_hz

        if message_type not in self._last_sent_at:
            self._last_sent_at[message_type] = 0.0