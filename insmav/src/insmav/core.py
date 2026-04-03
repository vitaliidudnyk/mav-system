from insmav.inspector_state import InspectorState
from insmav.mavlink.mavlink_receiver import MavlinkReceiver
from insmav.mavlink.mavlink_sender import MavlinkSender

from insmav.streams.custom_data.custom_data_handler import DatasetHandler
from insmav.streams.logs.log_handler import LogHandler
from insmav.streams.params.param_handler import ParamHandler
from insmav.streams.params.param_requester import ParamRequester
from insmav.streams.params.pending_params import PendingParams
from insmav.streams.rpc.ack_handler import AckHandler
from insmav.streams.rpc.pending_commands import PendingCommands
from insmav.streams.rpc.reliable_rpc_sender import ReliableRpcSender
from insmav.streams.rpc.rpc_creator import RpcCreator
from insmav.streams.telemetry.telemetry_handler import TelemetryHandler
from shared.rpc.rpc_events import RpcEvent
from shared.rpc.rpc_mapping import RPC_EVENT_MAPPING


class InsMavCore:
    def __init__(self, reader, writer) -> None:
        self._reader = reader
        self._writer = writer

        # --- receiver ---
        self._receiver = MavlinkReceiver()

        self.state = InspectorState()

        # --- handlers ---
        self.telemetry = TelemetryHandler(self.state)
        self.dataset = DatasetHandler(self.state)
        self.logs = LogHandler(self.state)

        self.pending_commands = PendingCommands()
        self.ack = AckHandler(self.pending_commands, self.state)

        self.pending_params = PendingParams()
        self.params = ParamHandler(self.pending_params, self.state)

        # --- register handlers ---
        self.telemetry.register(self._receiver)
        self.dataset.register(self._receiver)
        self.logs.register(self._receiver)
        self.ack.register(self._receiver)
        self.params.register(self._receiver)

        # --- inject receiver callback into reader ---
        self._reader.set_on_data_callback(self._receiver.handle_bytes)

        # --- sender ---
        self._mavlink_sender = MavlinkSender(self._writer)

        # --- params requester ---
        self.param_requester = ParamRequester(
            mavlink_sender=self._mavlink_sender,
            pending_params=self.pending_params,
        )

        # --- rpc ---
        self._reliable_rpc_sender = ReliableRpcSender(
            mavlink_sender=self._mavlink_sender,
            pending_commands=self.pending_commands,
        )

        self.rpc = RpcCreator(
            mavlink_sender=self._reliable_rpc_sender,
            rpc_event_mapping=RPC_EVENT_MAPPING,
        )

    def start(self) -> None:
        self._reader.start()

    def stop(self) -> None:
        self._reader.stop()
        self._writer.close()

    def request_all_params(self) -> None:
        self.param_requester.request_all()

    def request_param(self, name: str) -> None:
        self.param_requester.request_param(name)

    def set_param(self, name: str, value: float, param_type: int) -> None:
        self.state.set_param(
            name=name,
            value=value,
            status="pending",
            param_type=param_type,
        )

        self.param_requester.set_param(
            name=name,
            value=value,
            param_type=param_type,
        )

    def send_rpc(self, event: RpcEvent) -> None:
        command = self.rpc.get_command(event)
        params = self.rpc.get_padded_params(event)

        self.state.add_rpc_request(
            command=command,
            command_name=self._get_rpc_command_name(command),
            event_name=type(event).__name__,
            params=params,
            status="pending",
        )

        self.rpc.send(event)

    @staticmethod
    def _get_rpc_command_name(command: int) -> str:
        for name, value in RPC_EVENT_MAPPING.items():
            if name == command:
                return str(command)

        return str(command)