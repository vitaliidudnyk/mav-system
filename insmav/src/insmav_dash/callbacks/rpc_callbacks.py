from dataclasses import fields

from dash import ALL, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from shared.rpc.rpc_mapping import RPC_EVENT_MAPPING


def register_rpc_callbacks(app, state, core) -> None:
    event_types = _get_event_types()
    event_type_by_name = {
        event_type.__name__: event_type
        for event_type in event_types
    }

    @app.callback(
        Output("rpc-form-container", "children"),
        Input("rpc-event-dropdown", "value"),
    )
    def update_rpc_form(selected_event_name):
        if not selected_event_name:
            return html.Div("Select RPC event")

        event_type = event_type_by_name.get(selected_event_name)

        if event_type is None:
            return html.Div(f"Unknown RPC event: {selected_event_name}")

        return _build_rpc_form(event_type)

    @app.callback(
        Output("rpc-send-result", "children"),
        Input("rpc-send-button", "n_clicks"),
        State("rpc-event-dropdown", "value"),
        State({"type": "rpc-param-input", "name": ALL}, "id"),
        State({"type": "rpc-param-input", "name": ALL}, "value"),
        prevent_initial_call=True,
    )
    def send_rpc(_n_clicks, selected_event_name, input_ids, input_values):
        if not selected_event_name:
            raise PreventUpdate

        event_type = event_type_by_name.get(selected_event_name)

        if event_type is None:
            return f"Unknown RPC event: {selected_event_name}"

        expected_fields = [field_info.name for field_info in fields(event_type)]

        if not input_ids or len(input_ids) != len(expected_fields):
            return "RPC form is not ready yet"

        kwargs = {}

        for input_id, raw_value in zip(input_ids, input_values):
            field_name = input_id["name"]

            try:
                value = float(raw_value)
            except (TypeError, ValueError):
                return f"Invalid value for '{field_name}'"

            kwargs[field_name] = value

        missing_fields = [
            field_name
            for field_name in expected_fields
            if field_name not in kwargs
        ]

        if missing_fields:
            return f"Missing RPC fields: {', '.join(missing_fields)}"

        try:
            event = event_type(**kwargs)
            core.send_rpc(event)
        except Exception as error:
            return f"Failed to send RPC: {error}"

        return f"Sent {selected_event_name}"

    @app.callback(
        Output("rpc-history-table", "data"),
        Output("rpc-ack-table", "data"),
        Input("refresh-interval", "n_intervals"),
    )
    def update_rpc_tables(_n_intervals):
        rpc_history = state.get_rpc_history()
        rpc_ack_history = state.get_rpc_ack_history()

        history_rows = [
            {
                "rpc_id": item.get("rpc_id"),
                "command": item.get("command"),
                "command_name": item.get("command_name"),
                "event_name": item.get("event_name"),
                "params": _format_params(item.get("params")),
                "status": item.get("status"),
                "ack_result": item.get("ack_result"),
            }
            for item in reversed(rpc_history)
        ]

        ack_rows = [
            {
                "command": item.get("command"),
                "result": item.get("result"),
                "created_at": item.get("created_at"),
            }
            for item in reversed(rpc_ack_history)
        ]

        return history_rows, ack_rows


def _get_event_types() -> list[type]:
    unique_event_types = []
    seen = set()

    for event_type in RPC_EVENT_MAPPING.values():
        if event_type in seen:
            continue

        seen.add(event_type)
        unique_event_types.append(event_type)

    unique_event_types.sort(key=lambda item: item.__name__)

    return unique_event_types


def _build_rpc_form(event_type: type):
    controls = []

    for field_info in fields(event_type):
        controls.append(
            html.Div(
                [
                    html.Label(field_info.name),
                    dcc.Input(
                        id={
                            "type": "rpc-param-input",
                            "name": field_info.name,
                        },
                        type="number",
                        value=0,
                        debounce=True,
                        style={
                            "width": "100%",
                            "padding": "8px",
                            "marginTop": "4px",
                            "boxSizing": "border-box",
                        },
                    ),
                ],
                style={"marginBottom": "12px"},
            )
        )

    if not controls:
        return html.Div("This RPC event has no fields")

    return html.Div(controls)


def _format_params(params) -> str:
    if not params:
        return ""

    return ", ".join(str(value) for value in params)