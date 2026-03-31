from dash import dash_table, html


def build_params_tab():
    return html.Div(
        [
            html.H2("Parameters"),
            dash_table.DataTable(
                id="params-table",
                columns=[
                    {"name": "Name", "id": "name", "editable": False},
                    {"name": "Value", "id": "value", "editable": True},
                    {"name": "Status", "id": "status", "editable": False},
                    {"name": "Type", "id": "type", "editable": False},
                ],
                data=[],
                page_size=15,
                sort_action="native",
                editable=True,
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left"},
            ),
            html.Button(
                "Apply",
                id="params-apply-button",
                n_clicks=0,
                style={"marginTop": "12px"},
            ),
            html.Div(
                id="params-apply-result",
                style={"marginTop": "12px"},
            ),
        ],
        style={"padding": "16px"},
    )