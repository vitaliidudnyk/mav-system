from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go


def register_callbacks(app, state, core) -> None:
    @app.callback(
        Output("telemetry-summary", "children"),
        Output("telemetry-last-messages", "children"),
        Output("params-table", "data"),
        Output("logs-container", "children"),
        Output("dataset-dropdown", "options"),
        Output("dataset-dropdown", "value"),
        Output("dataset-graph", "figure"),
        Input("refresh-interval", "n_intervals"),
        Input("dataset-dropdown", "value"),
    )
    def update_dashboard(_n_intervals, selected_dataset_type):
        telemetry = state.get_telemetry()
        params = state.get_params()
        logs = state.get_logs()
        datasets = state.get_datasets()

        telemetry_summary = _build_telemetry_summary(telemetry)
        telemetry_last_messages = _build_telemetry_last_messages(telemetry)
        params_rows = _build_params_rows(params)
        logs_children = _build_logs(logs)

        dataset_options = [
            {"label": dataset_type, "value": dataset_type}
            for dataset_type in sorted(datasets.keys())
        ]

        if selected_dataset_type is None and dataset_options:
            selected_dataset_type = dataset_options[0]["value"]

        dataset_figure = _build_dataset_figure(
            datasets=datasets,
            dataset_type=selected_dataset_type,
        )

        return (
            telemetry_summary,
            telemetry_last_messages,
            params_rows,
            logs_children,
            dataset_options,
            selected_dataset_type,
            dataset_figure,
        )

    @app.callback(
        Output("params-apply-result", "children"),
        Input("params-apply-button", "n_clicks"),
        State("params-table", "data"),
        prevent_initial_call=True,
    )
    def apply_params(_n_clicks, rows):
        if not rows:
            raise PreventUpdate

        current_params = state.get_params()
        updated_count = 0

        for row in rows:
            name = row["name"]
            new_value_raw = row["value"]

            current_param = current_params.get(name)

            if current_param is None:
                continue

            current_value = current_param.get("value")
            param_type = current_param.get("type")

            try:
                new_value = float(new_value_raw)
            except (TypeError, ValueError):
                continue

            if current_value == new_value:
                continue

            if param_type is None:
                continue

            core.set_param(
                name=name,
                value=new_value,
                param_type=param_type,
            )
            updated_count += 1

        if updated_count == 0:
            return "No changes to apply"

        return f"Sent {updated_count} param update(s)"


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


def _build_params_rows(params: dict) -> list[dict]:
    rows = []

    for name, data in sorted(params.items()):
        rows.append(
            {
                "name": data.get("name", name),
                "value": data.get("value"),
                "status": data.get("status"),
                "type": data.get("type"),
            }
        )

    return rows


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


def _build_dataset_figure(datasets: dict[str, list], dataset_type: str | None):
    figure = go.Figure()

    figure.update_layout(
        title="Dataset History",
        xaxis_title="Index",
        yaxis_title="Value",
    )

    if dataset_type is None:
        return figure

    dataset_history = datasets.get(dataset_type, [])

    if not dataset_history:
        return figure

    sample = dataset_history[-1]

    if hasattr(sample, "__dict__"):
        field_names = list(sample.__dict__.keys())

        for field_name in field_names:
            y_values = [
                getattr(item, field_name, None)
                for item in dataset_history
            ]

            figure.add_trace(
                go.Scatter(
                    x=list(range(len(dataset_history))),
                    y=y_values,
                    mode="lines+markers",
                    name=field_name,
                )
            )

        return figure

    figure.add_trace(
        go.Scatter(
            x=list(range(len(dataset_history))),
            y=list(range(len(dataset_history))),
            mode="lines+markers",
            name=dataset_type,
        )
    )

    return figure