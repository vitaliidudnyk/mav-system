import socket


class UdpWriter:
    def __init__(self, target_host: str, target_port: int):
        self._target = (target_host, target_port)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"[udp][UdpWriter][__init__] Target={self._target}")

    def send(self, data: bytes) -> None:
        print(f"[udp][UdpWriter][send] Sending {len(data)} bytes to {self._target}")
        self._sock.sendto(data, self._target)

    def close(self) -> None:
        self._sock.close()