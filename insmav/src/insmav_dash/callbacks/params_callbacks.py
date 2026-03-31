from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


def register_params_callbacks(app, state, core) -> None:
    @app.callback(
        Output("params-table", "data"),
        Input("refresh-interval", "n_intervals"),
        State("params-table", "data"),
    )
    def update_params_table(_n_intervals, current_rows):
        params = state.get_params()
        current_rows = current_rows or []

        current_new_values_by_name = {
            row["name"]: row.get("new_value")
            for row in current_rows
            if row.get("name") is not None
        }

        rows = []

        for name, data in sorted(params.items()):
            value = data.get("value")

            if name in current_new_values_by_name:
                new_value = current_new_values_by_name[name]
            else:
                new_value = value

            rows.append(
                {
                    "name": data.get("name", name),
                    "value": value,
                    "new_value": new_value,
                    "status": data.get("status"),
                    "type": data.get("type"),
                }
            )

        return rows

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
            current_param = current_params.get(name)

            if current_param is None:
                continue

            current_value = current_param.get("value")
            param_type = current_param.get("type")
            new_value_raw = row.get("new_value")

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