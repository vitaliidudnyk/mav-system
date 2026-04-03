from insmav_dash.callbacks.datasets_callbacks import register_datasets_callbacks
from insmav_dash.callbacks.logs_callbacks import register_logs_callbacks
from insmav_dash.callbacks.params_callbacks import register_params_callbacks
from insmav_dash.callbacks.rpc_callbacks import register_rpc_callbacks
from insmav_dash.callbacks.telemetry_callbacks import register_telemetry_callbacks


def register_callbacks(app, state, core) -> None:
    register_telemetry_callbacks(app, state, core)
    register_logs_callbacks(app, state, core)
    register_datasets_callbacks(app, state, core)
    register_params_callbacks(app, state, core)
    register_rpc_callbacks(app, state, core)