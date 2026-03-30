class ParamStore:
    def __init__(self, param_definitions):
        self._params = {}
        self._order = []

        for param in param_definitions:
            name = param["name"]

            self._params[name] = {
                "code": param["code"],
                "name": name,
                "value": param["value"],
                "type": param["type"],
            }

            self._order.append(name)

        print(f"[params][ParamStore][__init__] Loaded {len(self._params)} params")

    def get_all(self) -> list:
        return [self._params[name] for name in self._order]

    def get_by_name(self, name: str):
        return self._params.get(name)

    def get_index_by_name(self, name: str) -> int:
        try:
            return self._order.index(name)
        except ValueError:
            return -1

    def update(self, name: str, value: float):
        param = self._params.get(name)

        if param is None:
            return None

        param["value"] = value

        print(f"[params][ParamStore][update] {name}={value}")

        return param