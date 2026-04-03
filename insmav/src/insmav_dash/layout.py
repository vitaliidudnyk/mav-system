from dash import dcc, html

from insmav_dash.tabs.datasets_tab import build_datasets_tab
from insmav_dash.tabs.logs_tab import build_logs_tab
from insmav_dash.tabs.params_tab import build_params_tab
from insmav_dash.tabs.rpc_tab import build_rpc_tab
from insmav_dash.tabs.telemetry_tab import build_telemetry_tab


def build_layout():
    return html.Div(
        [
            html.H1("Inspector Dashboard"),
            dcc.Interval(
                id="refresh-interval",
                interval=1000,
                n_intervals=0,
            ),
            dcc.Store(
                id="params-draft-store",
                data={},
            ),
            dcc.Tabs(
                id="main-tabs",
                value="telemetry",
                children=[
                    dcc.Tab(
                        label="Telemetry",
                        value="telemetry",
                        children=build_telemetry_tab(),
                    ),
                    dcc.Tab(
                        label="Datasets",
                        value="datasets",
                        children=build_datasets_tab(),
                    ),
                    dcc.Tab(
                        label="Params",
                        value="params",
                        children=build_params_tab(),
                    ),
                    dcc.Tab(
                        label="Logs",
                        value="logs",
                        children=build_logs_tab(),
                    ),
                    dcc.Tab(
                        label="RPC",
                        value="rpc",
                        children=build_rpc_tab(),
                    ),
                ],
            ),
        ],
        style={
            "maxWidth": "1200px",
            "margin": "0 auto",
            "padding": "24px",
        },
    )