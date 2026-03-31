from dash import html


def build_logs_tab():
    return html.Div(
        [
            html.H2("Logs"),
            html.Div(id="logs-container"),
        ],
        style={"padding": "16px"},
    )