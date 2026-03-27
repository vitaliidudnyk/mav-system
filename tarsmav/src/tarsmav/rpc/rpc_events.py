from dataclasses import dataclass


@dataclass
class RpcEvent:
    pass


@dataclass
class StartMissionEvent(RpcEvent):
    speed: float
    altitude: float
    timeout: float
    retries: float


@dataclass
class SetModeEvent(RpcEvent):
    mode_id: float
    submode_id: float
    flags: float


@dataclass
class CalibrateImuEvent(RpcEvent):
    calibrate_gyro: float
    calibrate_accel: float
    calibrate_mag: float