from pymavlink import mavutil

from tarsmav.streams.telemetry.tel_data import TelData
from tarsmav.streams.telemetry.tel_message_type import TelMessageType


class TelMessageFactory:
    @staticmethod
    def create_message(message_type: TelMessageType, data: TelData):
        if message_type == TelMessageType.HEARTBEAT:
            return TelMessageFactory.create_heartbeat(data)

        if message_type == TelMessageType.ATTITUDE:
            return TelMessageFactory.create_attitude(data)

        if message_type == TelMessageType.SYS_STATUS:
            return TelMessageFactory.create_sys_status(data)

        raise ValueError(f"Unsupported MAVLink message type: {message_type}")

    @staticmethod
    def create_heartbeat(data: TelData):
        payload = data.heartbeat

        return mavutil.mavlink.MAVLink_heartbeat_message(
            payload.mav_type,
            payload.autopilot,
            payload.base_mode,
            payload.custom_mode,
            payload.system_status,
            payload.mavlink_version,
        )

    @staticmethod
    def create_attitude(data: TelData):
        payload = data.attitude

        return mavutil.mavlink.MAVLink_attitude_message(
            payload.time_boot_ms,
            payload.roll,
            payload.pitch,
            payload.yaw,
            payload.rollspeed,
            payload.pitchspeed,
            payload.yawspeed,
        )

    @staticmethod
    def create_sys_status(data: TelData):
        payload = data.sys_status

        return mavutil.mavlink.MAVLink_sys_status_message(
            payload.onboard_control_sensors_present,
            payload.onboard_control_sensors_enabled,
            payload.onboard_control_sensors_health,
            payload.load,
            payload.voltage_battery,
            payload.current_battery,
            payload.battery_remaining,
            payload.drop_rate_comm,
            payload.errors_comm,
            payload.errors_count1,
            payload.errors_count2,
            payload.errors_count3,
            payload.errors_count4,
        )