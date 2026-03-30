from tarsmav.streams.telemetry.tel_message_type import TelMessageType


DEFAULT_TEL_RATES_HZ = {
    TelMessageType.HEARTBEAT: 1.0,
    TelMessageType.ATTITUDE: 10.0,
    TelMessageType.SYS_STATUS: 2.0,
}