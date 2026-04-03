from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


def register_params_callbacks(app, state, core) -> None:
    @app.callback(
        Output("params-table", "data"),
        Input("refresh-interval", "n_intervals"),
    )
    def update_params_table(_n_intervals):
        params = state.try_read_params("params-table")

        if params is None:
            raise PreventUpdate

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

    @app.callback(
        Output("params-selected-name", "value"),
        Output("params-current-value", "value"),
        Output("params-new-value-input", "value"),
        Input("params-table", "selected_rows"),
        State("params-table", "data"),
        State("params-draft-store", "data"),
    )
    def select_param(selected_rows, rows, draft_store):
        if not rows or not selected_rows:
            return "", "", None

        row_index = selected_rows[0]

        if row_index < 0 or row_index >= len(rows):
            return "", "", None

        row = rows[row_index]
        name = row.get("name")
        current_value = row.get("value")
        draft_store = draft_store or {}

        if name in draft_store:
            new_value = draft_store[name]
        else:
            new_value = current_value

        return name, current_value, new_value

    @app.callback(
        Output("params-draft-store", "data"),
        Input("params-new-value-input", "value"),
        State("params-selected-name", "value"),
        State("params-current-value", "value"),
        State("params-draft-store", "data"),
        prevent_initial_call=True,
    )
    def update_params_draft_store(
        new_value,
        selected_name,
        current_value,
        draft_store,
    ):
        if not selected_name:
            raise PreventUpdate

        draft_store = dict(draft_store or {})

        if _values_equal(new_value, current_value):
            if selected_name not in draft_store:
                raise PreventUpdate

            draft_store.pop(selected_name, None)
            return draft_store

        draft_store[selected_name] = new_value
        return draft_store

    @app.callback(
        Output("params-apply-result", "children"),
        Output("params-draft-store", "data", allow_duplicate=True),
        Output("params-new-value-input", "value", allow_duplicate=True),
        Input("params-apply-button", "n_clicks"),
        State("params-selected-name", "value"),
        State("params-new-value-input", "value"),
        State("params-draft-store", "data"),
        prevent_initial_call=True,
    )
    def apply_param(
        _n_clicks,
        selected_name,
        new_value_raw,
        draft_store,
    ):
        if not selected_name:
            return "Select a parameter first", draft_store or {}, new_value_raw

        draft_store = dict(draft_store or {})
        current_params = state.read_params()
        current_param = current_params.get(selected_name)

        if current_param is None:
            return "Selected parameter is no longer available", draft_store, new_value_raw

        current_value = current_param.get("value")
        param_type = current_param.get("type")

        try:
            new_value = float(new_value_raw)
        except (TypeError, ValueError):
            return "Invalid new value", draft_store, new_value_raw

        if _values_equal(current_value, new_value):
            draft_store.pop(selected_name, None)
            return "No changes to apply", draft_store, current_value

        if param_type is None:
            return "Parameter type is unknown", draft_store, new_value_raw

        core.set_param(
            name=selected_name,
            value=new_value,
            param_type=param_type,
        )

        draft_store.pop(selected_name, None)

        return "Sent 1 param update", draft_store, new_value

def _values_equal(left, right) -> bool:
    try:
        return float(left) == float(right)
    except (TypeError, ValueError):
        return left == right