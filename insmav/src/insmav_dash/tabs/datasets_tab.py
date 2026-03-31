from dash import dcc, html


def build_datasets_tab():
    return html.Div(
        [
            html.H2("Datasets"),
            dcc.Dropdown(
                id="dataset-dropdown",
                options=[],
                value=None,
                placeholder="Select dataset type",
                clearable=False,
            ),
            dcc.Graph(id="dataset-graph"),
        ],
        style={"padding": "16px"},
    )