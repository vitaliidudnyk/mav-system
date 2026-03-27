from dataclasses import dataclass, field


@dataclass
class HeartbeatPayload:
    mav_type: int = 0
    autopilot: int = 0
    base_mode: int = 0
    custom_mode: int = 0
    system_status: int = 0
    mavlink_version: int = 3


@dataclass
class AttitudePayload:
    time_boot_ms: int = 0
    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0
    rollspeed: float = 0.0
    pitchspeed: float = 0.0
    yawspeed: float = 0.0


@dataclass
class SysStatusPayload:
    onboard_control_sensors_present: int = 0
    onboard_control_sensors_enabled: int = 0
    onboard_control_sensors_health: int = 0
    load: int = 0
    voltage_battery: int = 0
    current_battery: int = -1
    battery_remaining: int = -1
    drop_rate_comm: int = 0
    errors_comm: int = 0
    errors_count1: int = 0
    errors_count2: int = 0
    errors_count3: int = 0
    errors_count4: int = 0


@dataclass
class MavData:
    heartbeat: HeartbeatPayload = field(default_factory=HeartbeatPayload)
    attitude: AttitudePayload = field(default_factory=AttitudePayload)
    sys_status: SysStatusPayload = field(default_factory=SysStatusPayload)