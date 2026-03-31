from dash import html


def build_telemetry_tab():
    return html.Div(
        [
            html.H2("Telemetry"),
            html.Div(id="telemetry-summary"),
            html.H3("Last messages"),
            html.Div(id="telemetry-last-messages"),
        ],
        style={"padding": "16px"},
    )