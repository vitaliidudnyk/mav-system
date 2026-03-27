import socket


class UdpReader:
    def __init__(self, host: str = "0.0.0.0", port: int = 14550, buffer_size: int = 4096):
        self._host = host
        self._port = port
        self._buffer_size = buffer_size

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind((self._host, self._port))
        print(f"[udp][UdpReader][__init__] Listening on {self._host}:{self._port}")
        self._socket.setblocking(False)

    def read(self) -> bytes | None:
        try:
            data, addr = self._socket.recvfrom(self._buffer_size)
            print(f"[udp][UdpReader][read] Received {len(data)} bytes from {addr}")
            return data
        except BlockingIOError:
            return None

    def close(self) -> None:
        self._socket.close()