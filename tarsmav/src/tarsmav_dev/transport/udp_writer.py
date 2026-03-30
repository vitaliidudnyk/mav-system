import socket


class UdpWriter:
    def __init__(self, host: str = "127.0.0.1", port: int = 14550):
        self._addr = (host, port)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"[udp][UdpWriter][__init__] Target={self._addr}")

    def __call__(self, data: bytes) -> None:
        print(f"[udp][UdpWriter][__call__] Sending {len(data)} bytes to {self._addr}")
        self._sock.sendto(data, self._addr)