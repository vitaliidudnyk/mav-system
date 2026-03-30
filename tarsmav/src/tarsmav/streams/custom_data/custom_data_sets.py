from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class DatasetType(Enum):
    IMU = "imu"
    ATTITUDE = "attitude"
    BATTERY = "battery"
    SENDER_SNAPSHOT = "sndr_snap"


class DebugFloatDataset(Protocol):
    @property
    def dataset_type(self) -> DatasetType:
        ...

    def to_array(self) -> list[float]:
        ...

    def to_mavlink_name(self) -> bytes:
        return self.dataset_type.value.encode("utf-8")


# ===================== DATASETS =====================


@dataclass
class ImuDebug:
    roll: float
    pitch: float
    yaw: float
    gyro_x: float
    gyro_y: float
    gyro_z: float

    @property
    def dataset_type(self) -> DatasetType:
        return DatasetType.IMU

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
    def dataset_type(self) -> DatasetType:
        return DatasetType.ATTITUDE

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
    def dataset_type(self) -> DatasetType:
        return DatasetType.BATTERY

    def to_array(self) -> list[float]:
        return [
            self.voltage,
            self.current,
            self.remaining,
        ]


@dataclass
class SenderSnapshot:
    dropped_logs_total: int
    dropped_custom_total: int
    avg_load_pct: float
    high_load_time_pct: float
    sent_bytes_per_sec: float
    sent_messages_per_sec: float

    @property
    def dataset_type(self) -> DatasetType:
        return DatasetType.SENDER_SNAPSHOT

    def to_array(self) -> list[float]:
        return [
            float(self.dropped_logs_total),
            float(self.dropped_custom_total),
            self.avg_load_pct,
            self.high_load_time_pct,
            self.sent_bytes_per_sec,
            self.sent_messages_per_sec,
        ]