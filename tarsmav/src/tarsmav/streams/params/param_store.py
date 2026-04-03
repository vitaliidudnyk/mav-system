from tarsmav.streams.params.param_name import normalize_param_name


class ParamStore:
    def __init__(self, param_definitions):
        self._params = {}
        self._order = []

        for param in param_definitions:
            full_name = param["name"]
            normalized_name = normalize_param_name(full_name)

            self._params[normalized_name] = {
                "code": param["code"],
                "name": normalized_name,
                "full_name": full_name,
                "value": param["value"],
                "type": param["type"],
            }

            self._order.append(normalized_name)

        print(f"[params][ParamStore][__init__] Loaded {len(self._params)} params")

    def get_all(self) -> list:
        return [self._params[name] for name in self._order]

    def get_by_name(self, name: str):
        normalized_name = normalize_param_name(name)
        return self._params.get(normalized_name)

    def get_index_by_name(self, name: str) -> int:
        normalized_name = normalize_param_name(name)

        try:
            return self._order.index(normalized_name)
        except ValueError:
            return -1

    def update(self, name: str, value: float):
        normalized_name = normalize_param_name(name)
        param = self._params.get(normalized_name)

        if param is None:
            return None

        old_value = param["value"]
        param["value"] = value

        print(
            f"[params][ParamStore][update] "
            f"{normalized_name}: {old_value} -> {value}"
        )

        return param