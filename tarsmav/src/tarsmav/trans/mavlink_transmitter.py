from ..mavlink_config import mavutil


class MavlinkTransmitter:
    def __init__(self, writer):
        self._mav = mavutil.mavlink.MAVLink(None)
        self._writer = writer
        print("[mavlink][MavlinkTransmitter][__init__] Initialized")

    def send(self, message) -> None:
        data = message.pack(self._mav)
        self._writer(data)