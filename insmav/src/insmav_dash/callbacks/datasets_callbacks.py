from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go


def register_datasets_callbacks(app, state, _core) -> None:
    @app.callback(
        Output("dataset-dropdown", "options"),
        Output("dataset-dropdown", "value"),
        Input("refresh-interval", "n_intervals"),
        State("dataset-dropdown", "value"),
    )
    def update_dataset_dropdown(_n_intervals, selected_dataset_type):
        datasets = state.try_read_datasets("datasets-dropdown")

        if datasets is None:
            raise PreventUpdate

        dataset_options = [
            {"label": dataset_type, "value": dataset_type}
            for dataset_type in sorted(datasets.keys())
        ]

        available_values = {
            item["value"]
            for item in dataset_options
        }

        if selected_dataset_type not in available_values:
            if dataset_options:
                selected_dataset_type = dataset_options[0]["value"]
            else:
                selected_dataset_type = None

        return dataset_options, selected_dataset_type

    @app.callback(
        Output("dataset-graph", "figure"),
        Input("refresh-interval", "n_intervals"),
        Input("dataset-dropdown", "value"),
    )
    def update_dataset_graph(_n_intervals, selected_dataset_type):
        datasets = state.read_datasets()

        return _build_dataset_figure(
            datasets=datasets,
            dataset_type=selected_dataset_type,
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