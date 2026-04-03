from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate


def register_telemetry_callbacks(app, state, _core) -> None:
    @app.callback(
        Output("telemetry-summary", "children"),
        Output("telemetry-last-messages", "children"),
        Input("refresh-interval", "n_intervals"),
    )
    def update_telemetry(_n_intervals):
        telemetry = state.try_read_telemetry("telemetry")

        if telemetry is None:
            raise PreventUpdate

        telemetry_summary = _build_telemetry_summary(telemetry)
        telemetry_last_messages = _build_telemetry_last_messages(telemetry)

        return telemetry_summary, telemetry_last_messages


def _build_telemetry_summary(telemetry: list):
    if not telemetry:
        return html.Div("No telemetry yet")

    last_message = telemetry[-1]
    message_type = getattr(
        last_message,
        "get_type",
        lambda: type(last_message).__name__,
    )()

    return html.Div(
        [
            html.Div(f"Total messages: {len(telemetry)}"),
            html.Div(f"Last message type: {message_type}"),
        ]
    )


def _build_telemetry_last_messages(telemetry: list):
    recent_messages = telemetry[-20:]

    if not recent_messages:
        return html.Div("No telemetry yet")

    return html.Ul(
        [
            html.Li(str(message))
            for message in reversed(recent_messages)
        ]
    )