from enum import Enum


class TelMessageType(Enum):
    HEARTBEAT = "heartbeat"
    ATTITUDE = "attitude"
    SYS_STATUS = "sys_status"