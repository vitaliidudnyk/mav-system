import socket
import time


class UdpReader:
    def __init__(
        self,
        host: str,
        port: int,
        buffer_size: int = 4096,
    ):
        self._on_data = None
        self._host = host
        self._port = port
        self._buffer_size = buffer_size

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind((self._host, self._port))
        self._socket.setblocking(False)

        print(f"[udp][UdpReader][__init__] Listening on {self._host}:{self._port}")

    def set_on_data_callback(self, callback) -> None:
        self._on_data = callback
        
    def start(self) -> None:
        while True:
            try:
                data, addr = self._socket.recvfrom(self._buffer_size)

                print(
                    f"[udp][UdpReader][start] "
                    f"Received {len(data)} bytes from {addr}"
                )

                self._on_data(data)

            except BlockingIOError:
                time.sleep(0.001)  # prevent 100% CPU

    def close(self) -> None:
        self._socket.close()