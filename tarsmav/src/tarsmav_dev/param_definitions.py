from tarsmav.mavlink.mavlink_config import mavutil


PARAM_DEFINITIONS = [
    {
        "code": 100,
        "name": "camera_pitch_deg",
        "value": 15.0,
        "type": mavutil.mavlink.MAV_PARAM_TYPE_REAL32,
    },
    {
        "code": 200,
        "name": "bool_skip_preparation",
        "value": 0.0,
        "type": mavutil.mavlink.MAV_PARAM_TYPE_UINT8,
    },
    {
        "code": 201,
        "name": "bool_arm_on_skip_preparation",
        "value": 1.0,
        "type": mavutil.mavlink.MAV_PARAM_TYPE_UINT8,
    },
    {
        "code": 202,
        "name": "bool_use_camera_mock",
        "value": 0.0,
        "type": mavutil.mavlink.MAV_PARAM_TYPE_UINT8,
    },
    {
        "code": 203,
        "name": "bool_wait_for_target_before_init",
        "value": 1.0,
        "type": mavutil.mavlink.MAV_PARAM_TYPE_UINT8,
    },
    {
        "code": 204,
        "name": "attitude_freq_min",
        "value": 10.0,
        "type": mavutil.mavlink.MAV_PARAM_TYPE_REAL32,
    },
]