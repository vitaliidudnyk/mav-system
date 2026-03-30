from insmav.mavlink.mavlink_config import mavutil


class _UdpWriteAdapter:
    def __init__(self, udp_writer):
        self._udp_writer = udp_writer

    def write(self, data: bytes) -> int:
        self._udp_writer.send(data)
        return len(data)


class MavlinkSender:
    def __init__(
        self,
        udp_writer,
        system_id: int = 1,
        component_id: int = 1,
    ):
        self._udp_writer = udp_writer
        self._mav = mavutil.mavlink.MAVLink(
            _UdpWriteAdapter(udp_writer),
            srcSystem=system_id,
            srcComponent=component_id,
        )

    def send(self, message) -> None:
        self._mav.send(message)