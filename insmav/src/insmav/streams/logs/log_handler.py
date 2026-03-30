from insmav.streams.shared.base_handler import BaseHandler


class LogHandler(BaseHandler):
    def __init__(self):
        self._buffers = {}

    @property
    def message_type(self) -> str:
        return "LOG_DATA"

    def handle(self, message) -> None:
        log_id = message.id
        offset = message.ofs
        count = message.count
        chunk = bytes(message.data[:count])

        if offset == 0 or log_id not in self._buffers:
            self._buffers[log_id] = bytearray()

        buffer = self._buffers[log_id]

        if len(buffer) < offset:
            buffer.extend(b"\x00" * (offset - len(buffer)))

        end_offset = offset + count

        if len(buffer) < end_offset:
            buffer.extend(b"\x00" * (end_offset - len(buffer)))

        buffer[offset:end_offset] = chunk

        try:
            text = bytes(buffer).decode("utf-8")
        except UnicodeDecodeError:
            text = bytes(buffer).decode("utf-8", errors="replace")

        print(
            f"[Log] id={log_id} ofs={offset} count={count} text='{text}'"
        )