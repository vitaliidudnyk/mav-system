from dataclasses import dataclass
from typing import Protocol


class DebugFloatDataset(Protocol):
    @property
    def name(self) -> str:
        ...

    def to_array(self) -> list[float]:
        ...


@dataclass
class ImuDebug:
    roll: float
    pitch: float
    yaw: float
    gyro_x: float
    gyro_y: float
    gyro_z: float

    @property
    def name(self) -> str:
        return "imu"

    def to_array(self) -> list[float]:
        return [
            self.roll,
            self.pitch,
            self.yaw,
            self.gyro_x,
            self.gyro_y,
            self.gyro_z,
        ]


@dataclass
class AttitudeDebug:
    roll: float
    pitch: float
    yaw: float

    @property
    def name(self) -> str:
        return "attitude"

    def to_array(self) -> list[float]:
        return [
            self.roll,
            self.pitch,
            self.yaw,
        ]


@dataclass
class BatteryDebug:
    voltage: float
    current: float
    remaining: float

    @property
    def name(self) -> str:
        return "battery"

    def to_array(self) -> list[float]:
        return [
            self.voltage,
            self.current,
            self.remaining,
        ]