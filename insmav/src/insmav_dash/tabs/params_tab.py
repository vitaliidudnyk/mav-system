from dash import dcc, dash_table, html


def build_params_tab():
    return html.Div(
        [
            html.H2("Parameters"),
            dash_table.DataTable(
                id="params-table",
                columns=[
                    {"name": "Name", "id": "name"},
                    {"name": "Value", "id": "value"},
                    {"name": "Status", "id": "status"},
                    {"name": "Type", "id": "type"},
                ],
                data=[],
                page_size=15,
                sort_action="native",
                row_selectable="single",
                selected_rows=[],
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left"},
            ),
            html.Div(
                [
                    html.H3("Edit parameter"),
                    html.Div(
                        [
                            html.Label("Selected parameter"),
                            dcc.Input(
                                id="params-selected-name",
                                type="text",
                                value="",
                                readOnly=True,
                                style={
                                    "width": "100%",
                                    "padding": "8px",
                                    "marginTop": "4px",
                                    "boxSizing": "border-box",
                                },
                            ),
                        ],
                        style={"marginBottom": "12px"},
                    ),
                    html.Div(
                        [
                            html.Label("Current value"),
                            dcc.Input(
                                id="params-current-value",
                                type="text",
                                value="",
                                readOnly=True,
                                style={
                                    "width": "100%",
                                    "padding": "8px",
                                    "marginTop": "4px",
                                    "boxSizing": "border-box",
                                },
                            ),
                        ],
                        style={"marginBottom": "12px"},
                    ),
                    html.Div(
                        [
                            html.Label("New value"),
                            dcc.Input(
                                id="params-new-value-input",
                                type="number",
                                value=None,
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
                    ),
                    html.Button(
                        "Apply",
                        id="params-apply-button",
                        n_clicks=0,
                    ),
                    html.Div(
                        id="params-apply-result",
                        style={"marginTop": "12px"},
                    ),
                ],
                style={
                    "marginTop": "24px",
                    "padding": "16px",
                    "border": "1px solid #ddd",
                    "borderRadius": "8px",
                },
            ),
        ],
        style={"padding": "16px"},
    )