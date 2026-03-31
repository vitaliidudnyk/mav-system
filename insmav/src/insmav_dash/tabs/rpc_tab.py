from dataclasses import fields

from dash import dash_table, dcc, html

from shared.rpc.rpc_mapping import RPC_EVENT_MAPPING


def build_rpc_tab():
    event_types = _get_event_types()
    event_names = [event_type.__name__ for event_type in event_types]
    default_event_type = event_types[0] if event_types else None
    default_value = default_event_type.__name__ if default_event_type else None

    return html.Div(
        [
            html.H2("RPC"),
            html.Div(
                [
                    html.Label("RPC Event"),
                    dcc.Dropdown(
                        id="rpc-event-dropdown",
                        options=[
                            {"label": event_name, "value": event_name}
                            for event_name in event_names
                        ],
                        value=default_value,
                        clearable=False,
                    ),
                ],
                style={"marginBottom": "16px"},
            ),
            html.Div(
                id="rpc-form-container",
                children=_build_rpc_form(default_event_type),
                style={
                    "padding": "12px",
                    "border": "1px solid #ccc",
                    "borderRadius": "8px",
                    "marginBottom": "16px",
                },
            ),
            html.Button(
                "Send RPC",
                id="rpc-send-button",
                n_clicks=0,
                style={"marginBottom": "12px"},
            ),
            html.Div(
                id="rpc-send-result",
                style={"marginBottom": "24px"},
            ),
            html.H3("RPC History"),
            dash_table.DataTable(
                id="rpc-history-table",
                columns=[
                    {"name": "rpc_id", "id": "rpc_id"},
                    {"name": "command", "id": "command"},
                    {"name": "command_name", "id": "command_name"},
                    {"name": "event_name", "id": "event_name"},
                    {"name": "params", "id": "params"},
                    {"name": "status", "id": "status"},
                    {"name": "ack_result", "id": "ack_result"},
                ],
                data=[],
                style_table={"overflowX": "auto"},
                style_cell={
                    "textAlign": "left",
                    "padding": "8px",
                },
                page_size=10,
            ),
            html.H3(
                "ACK History",
                style={"marginTop": "24px"},
            ),
            dash_table.DataTable(
                id="rpc-ack-table",
                columns=[
                    {"name": "command", "id": "command"},
                    {"name": "result", "id": "result"},
                    {"name": "created_at", "id": "created_at"},
                ],
                data=[],
                style_table={"overflowX": "auto"},
                style_cell={
                    "textAlign": "left",
                    "padding": "8px",
                },
                page_size=10,
            ),
        ],
        style={"padding": "16px"},
    )


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


def _build_rpc_form(event_type: type | None):
    if event_type is None:
        return html.Div("No RPC events available")

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