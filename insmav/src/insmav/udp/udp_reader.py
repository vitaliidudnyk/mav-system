import socket


class UdpReader:
    def __init__(self, host: str, port: int, on_data_callback):
        self._host = host
        self._port = port
        self._on_data = on_data_callback
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self) -> None:
        self._sock.bind((self._host, self._port))
        print(f"[udp][UdpReader][start] Listening on {self._host}:{self._port}")

        while True:
            data, addr = self._sock.recvfrom(4096)
            print(f"[udp][UdpReader][start] Received {len(data)} bytes from {addr}")
            self._on_data(data)