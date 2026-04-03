from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate


def register_logs_callbacks(app, state, _core) -> None:
    @app.callback(
        Output("logs-container", "children"),
        Input("refresh-interval", "n_intervals"),
    )
    def update_logs(_n_intervals):
        logs = state.try_read_logs("logs")

        if logs is None:
            raise PreventUpdate

        return _build_logs(logs)


def _build_logs(logs: list[str]):
    recent_logs = logs[-20:]

    if not recent_logs:
        return html.Div("No logs yet")

    return html.Ul(
        [
            html.Li(log_text)
            for log_text in reversed(recent_logs)
        ]
    )