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

    @classmethod
    def from_array(cls, data: list[float]):
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
    def dataset_type(self) -> DatasetType:
        return DatasetType.IMU

    @classmethod
    def from_array(cls, data: list[float]) -> "ImuDebug":
        return cls(
            roll=data[0],
            pitch=data[1],
            yaw=data[2],
            gyro_x=data[3],
            gyro_y=data[4],
            gyro_z=data[5],
        )


@dataclass
class AttitudeDebug:
    roll: float
    pitch: float
    yaw: float

    @property
    def dataset_type(self) -> DatasetType:
        return DatasetType.ATTITUDE

    @classmethod
    def from_array(cls, data: list[float]) -> "AttitudeDebug":
        return cls(
            roll=data[0],
            pitch=data[1],
            yaw=data[2],
        )


@dataclass
class BatteryDebug:
    voltage: float
    current: float
    remaining: float

    @property
    def dataset_type(self) -> DatasetType:
        return DatasetType.BATTERY

    @classmethod
    def from_array(cls, data: list[float]) -> "BatteryDebug":
        return cls(
            voltage=data[0],
            current=data[1],
            remaining=data[2],
        )


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

    @classmethod
    def from_array(cls, data: list[float]) -> "SenderSnapshot":
        return cls(
            dropped_logs_total=int(data[0]),
            dropped_custom_total=int(data[1]),
            avg_load_pct=data[2],
            high_load_time_pct=data[3],
            sent_bytes_per_sec=data[4],
            sent_messages_per_sec=data[5],
        )


DATASET_TYPES = {
    DatasetType.IMU: ImuDebug,
    DatasetType.ATTITUDE: AttitudeDebug,
    DatasetType.BATTERY: BatteryDebug,
    DatasetType.SENDER_SNAPSHOT: SenderSnapshot,
}