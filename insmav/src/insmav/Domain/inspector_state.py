from insmav.domain.datasets_state import DatasetsState
from insmav.domain.logs_state import LogsState
from insmav.domain.params_state import ParamsState
from insmav.domain.rpc_state import RpcState
from insmav.domain.telemetry_state import TelemetryState


class InspectorState:
    def __init__(
        self,
        telemetry_limit: int = 300,
        dataset_limit: int = 300,
        logs_limit: int = 100,
        rpc_limit: int = 100,
    ) -> None:
        self.telemetry = TelemetryState(limit=telemetry_limit)
        self.datasets = DatasetsState(dataset_limit=dataset_limit)
        self.params = ParamsState()
        self.logs = LogsState(limit=logs_limit)
        self.rpc = RpcState(limit=rpc_limit)

    # =========================
    # WRITE API
    # =========================

    def add_telemetry(self, message) -> None:
        # print(f"[state][WRITE][telemetry] {type(message).__name__}")
        self.telemetry.add_telemetry(message)

    def add_dataset(self, dataset_type: str, dataset) -> None:
        # print(f"[state][WRITE][dataset] type={dataset_type}")
        self.datasets.add_dataset(dataset_type, dataset)

    def set_param(
        self,
        name: str,
        value: float,
        status: str = "idle",
        param_type: int | None = None,
    ) -> None:
        print(
            f"[state][WRITE][param] {name}={value} "
            f"status={status} type={param_type}"
        )

        self.params.set_param(
            name=name,
            value=value,
            status=status,
            param_type=param_type,
        )

    def set_param_status(self, name: str, status: str) -> None:
        print(f"[state][WRITE][param_status] {name} -> {status}")

        self.params.set_param_status(name=name, status=status)

    def add_log(self, text: str) -> None:
        # print(f"[state][WRITE][log] {text}")
        self.logs.add_log(text)

    def add_rpc_request(
        self,
        command: int,
        command_name: str,
        event_name: str,
        params: list[float],
        status: str = "pending",
    ) -> int:
        print(f"[state][WRITE][rpc_request] {event_name} cmd={command}")

        return self.rpc.add_rpc_request(
            command=command,
            command_name=command_name,
            event_name=event_name,
            params=params,
            status=status,
        )

    def set_rpc_status(
        self,
        rpc_id: int,
        status: str,
        ack_result: int | None = None,
    ) -> None:
        print(
            f"[state][WRITE][rpc_status] id={rpc_id} "
            f"status={status} ack={ack_result}"
        )

        self.rpc.set_rpc_status(
            rpc_id=rpc_id,
            status=status,
            ack_result=ack_result,
        )

    def add_rpc_ack(self, message) -> None:
        print(
            f"[state][WRITE][rpc_ack] cmd={getattr(message, 'command', None)} "
            f"result={getattr(message, 'result', None)}"
        )

        self.rpc.add_rpc_ack(message)

    # =========================
    # READ API (FULL)
    # =========================

    def read_telemetry(self):
        data = self.telemetry.read_telemetry()
        # print(f"[state][READ][telemetry] size={len(data)}")
        return data

    def read_datasets(self):
        data = self.datasets.read_datasets()
        # print(f"[state][READ][datasets] keys={list(data.keys())}")
        return data

    def read_params(self):
        data = self.params.read_params()
        print(f"[state][READ][params] size={len(data)}")
        return data

    def read_logs(self):
        data = self.logs.read_logs()
        # print(f"[state][READ][logs] size={len(data)}")
        return data

    def read_rpc_history(self):
        data = self.rpc.read_rpc_history()
        print(f"[state][READ][rpc_history] size={len(data)}")
        return data

    def read_rpc_ack_history(self):
        data = self.rpc.read_rpc_ack_history()
        print(f"[state][READ][rpc_ack] size={len(data)}")
        return data

    def read_rpc_statuses(self):
        data = self.rpc.read_rpc_statuses()
        print(f"[state][READ][rpc_statuses] size={len(data)}")
        return data

    # =========================
    # TRY READ API
    # =========================

    def try_read_telemetry(self, reader_id: str):
        data = self.telemetry.try_read_telemetry(reader_id)

        # if data is None:
        #     print(f"[state][SKIP][telemetry] reader={reader_id}")
        # else:
        #     print(f"[state][TRY_READ][telemetry] size={len(data)} reader={reader_id}")

        return data

    def try_read_datasets(self, reader_id: str):
        data = self.datasets.try_read_datasets(reader_id)

        # if data is None:
        #     print(f"[state][SKIP][datasets] reader={reader_id}")
        # else:
        #     print(
        #         f"[state][TRY_READ][datasets] keys={list(data.keys())} "
        #         f"reader={reader_id}"
        #     )

        return data

    def try_read_params(self, reader_id: str):
        data = self.params.try_read_params(reader_id)

        if data is None:
            print(f"[state][SKIP][params] reader={reader_id}")
        else:
            print(f"[state][TRY_READ][params] size={len(data)} reader={reader_id}")

        return data

    def try_read_logs(self, reader_id: str):
        data = self.logs.try_read_logs(reader_id)

        # if data is None:
        #     print(f"[state][SKIP][logs] reader={reader_id}")
        # else:
        #     print(f"[state][TRY_READ][logs] size={len(data)} reader={reader_id}")

        return data

    def try_read_rpc_history(self, reader_id: str):
        data = self.rpc.try_read_rpc_history(reader_id)

        if data is None:
            print(f"[state][SKIP][rpc_history] reader={reader_id}")
        else:
            print(
                f"[state][TRY_READ][rpc_history] size={len(data)} "
                f"reader={reader_id}"
            )

        return data

    def try_read_rpc_ack_history(self, reader_id: str):
        data = self.rpc.try_read_rpc_ack_history(reader_id)

        if data is None:
            print(f"[state][SKIP][rpc_ack] reader={reader_id}")
        else:
            print(
                f"[state][TRY_READ][rpc_ack] size={len(data)} "
                f"reader={reader_id}"
            )

        return data

    def try_read_rpc_statuses(self, reader_id: str):
        data = self.rpc.try_read_rpc_statuses(reader_id)

        if data is None:
            print(f"[state][SKIP][rpc_statuses] reader={reader_id}")
        else:
            print(
                f"[state][TRY_READ][rpc_statuses] size={len(data)} "
                f"reader={reader_id}"
            )

        return data