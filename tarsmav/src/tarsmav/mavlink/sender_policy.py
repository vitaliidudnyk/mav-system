from dataclasses import dataclass
from enum import IntEnum


class MessagePriority(IntEnum):
    LOW = 1
    HIGH = 2
    CRITICAL = 3


CRITICAL_MESSAGE_TYPES = {
    "COMMAND_ACK",
    "PARAM_VALUE",
}

LOW_PRIORITY_MESSAGE_TYPES = {
    "LOG_DATA",
    "DEBUG_FLOAT_ARRAY",
}


@dataclass(frozen=True)
class SenderPolicy:
    max_messages_per_sec: int = 50
    max_bytes_per_sec: int = 8192

    def get_priority(self, message_type: str) -> MessagePriority:
        if message_type in CRITICAL_MESSAGE_TYPES:
            return MessagePriority.CRITICAL

        if message_type in LOW_PRIORITY_MESSAGE_TYPES:
            return MessagePriority.LOW

        return MessagePriority.HIGH

