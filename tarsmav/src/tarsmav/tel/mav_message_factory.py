from pymavlink import mavutil

from tarsmav.tel.mav_data import MavData
from tarsmav.tel.mav_message_type import MavMessageType


class MavMessageFactory:
    @staticmethod
    def create_message(message_type: MavMessageType, data: MavData):
        if message_type == MavMessageType.HEARTBEAT:
            return MavMessageFactory.create_heartbeat(data)

        if message_type == MavMessageType.ATTITUDE:
            return MavMessageFactory.create_attitude(data)

        if message_type == MavMessageType.SYS_STATUS:
            return MavMessageFactory.create_sys_status(data)

        raise ValueError(f"Unsupported MAVLink message type: {message_type}")

    @staticmethod
    def create_heartbeat(data: MavData):
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
    def create_attitude(data: MavData):
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
    def create_sys_status(data: MavData):
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