from insmav_dash.callbacks.dashboard_callbacks import register_dashboard_callbacks
from insmav_dash.callbacks.params_callbacks import register_params_callbacks
from insmav_dash.callbacks.rpc_callbacks import register_rpc_callbacks


def register_callbacks(app, state, core) -> None:
    register_dashboard_callbacks(app, state, core)
    register_params_callbacks(app, state, core)
    register_rpc_callbacks(app, state, core)