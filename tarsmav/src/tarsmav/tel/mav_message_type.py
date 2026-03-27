from enum import Enum


class MavMessageType(Enum):
    HEARTBEAT = "heartbeat"
    ATTITUDE = "attitude"
    SYS_STATUS = "sys_status"