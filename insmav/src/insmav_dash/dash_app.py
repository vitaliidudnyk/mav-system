import dash

from insmav_dash.callbacks import register_callbacks
from insmav_dash.layout import build_layout


class DashApp:
    def __init__(self, core):
        self._core = core
        self._state = core.state
        self._app = dash.Dash(__name__)

        self._app.layout = build_layout()
        register_callbacks(
            app=self._app,
            state=self._state,
            core=self._core,
        )

    def run(self, host: str = "127.0.0.1", port: int = 8050) -> None:
        self._app.run(host=host, port=port, debug=False)