from ..mavlink_config import mavutil


class TarsMavLogs:
    _CHUNK_SIZE = 90

    def __init__(self, trans, log_id: int = 0):
        self._trans = trans
        self._log_id = log_id
        self._ofs = 0

    def _create_log_data(self, chunk: bytes):
        return mavutil.mavlink.MAVLink_log_data_message(
            id=self._log_id,
            ofs=self._ofs,
            count=len(chunk),
            data=chunk.ljust(self._CHUNK_SIZE, b"\0"),
        )

    def log(self, message: str) -> None:
        data = (message + "\n").encode("utf-8")

        for i in range(0, len(data), self._CHUNK_SIZE):
            chunk = data[i:i + self._CHUNK_SIZE]
            msg = self._create_log_data(chunk)
            self._trans.send(msg)
            self._ofs += len(chunk)