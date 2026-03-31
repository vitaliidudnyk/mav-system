from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


def register_params_callbacks(app, state, core) -> None:
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