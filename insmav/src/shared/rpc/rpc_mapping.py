from shared.rpc.rpc_events import StartMissionEvent, SetModeEvent, CalibrateImuEvent

RPC_START_MISSION = 31001
RPC_SET_MODE = 31002
RPC_CALIBRATE_IMU = 31003

RPC_EVENT_MAPPING = {
    RPC_START_MISSION: StartMissionEvent,
    RPC_SET_MODE: SetModeEvent,
    RPC_CALIBRATE_IMU: CalibrateImuEvent,
}