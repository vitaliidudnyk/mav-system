import logging

from src.tarsmav.rpc.rpc_events import (
    CalibrateImuEvent,
    SetModeEvent,
    StartMissionEvent,
)
from src.tarsmav.rpc.rpc_mapping import (
    RPC_CALIBRATE_IMU,
    RPC_SET_MODE,
    RPC_START_MISSION,
)


class RpcEventListeners:
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def handle_event(self, command: int, event) -> None:
        if command == RPC_START_MISSION:
            self._on_start_mission(event)
            return

        if command == RPC_SET_MODE:
            self._on_set_mode(event)
            return

        if command == RPC_CALIBRATE_IMU:
            self._on_calibrate_imu(event)
            return

        self._logger.warning("Unknown RPC command received: %s", command)

    def _on_start_mission(self, event: StartMissionEvent) -> None:
        self._logger.info(
            "RPC StartMissionEvent received: speed=%s altitude=%s timeout=%s retries=%s",
            event.speed,
            event.altitude,
            event.timeout,
            event.retries,
        )

    def _on_set_mode(self, event: SetModeEvent) -> None:
        self._logger.info(
            "RPC SetModeEvent received: mode_id=%s submode_id=%s flags=%s",
            event.mode_id,
            event.submode_id,
            event.flags,
        )

    def _on_calibrate_imu(self, event: CalibrateImuEvent) -> None:
        self._logger.info(
            "RPC CalibrateImuEvent received: gyro=%s accel=%s mag=%s",
            event.calibrate_gyro,
            event.calibrate_accel,
            event.calibrate_mag,
        )