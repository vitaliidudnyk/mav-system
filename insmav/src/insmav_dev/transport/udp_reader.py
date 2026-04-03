import socket
import time


class UdpReader:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._on_data = None

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setblocking(False)

        self._is_running = False

    def set_on_data_callback(self, callback) -> None:
        self._on_data = callback

    def start(self) -> None:
        self._sock.bind((self._host, self._port))
        # print(f"[udp][UdpReader][start] Listening on {self._host}:{self._port}")

        self._is_running = True

        while self._is_running:
            try:
                data, addr = self._sock.recvfrom(4096)
                # print(f"[udp][UdpReader][start] Received {len(data)} bytes from {addr}")

                if self._on_data is not None:
                    self._on_data(data)

            except BlockingIOError:
                time.sleep(0.001)

            except OSError:
                # socket closed → exit loop
                break

    def stop(self) -> None:
        self._is_running = False
        self._sock.close()