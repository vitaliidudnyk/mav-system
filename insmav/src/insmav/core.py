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
from insmav.streams.rpc.rpc_mapping import RPC_EVENT_MAPPING
from insmav.streams.telemetry.telemetry_handler import TelemetryHandler


class InsMavCore:
    def __init__(self, reader, writer) -> None:
        self._reader = reader
        self._writer = writer

        # --- receiver ---
        self._receiver = MavlinkReceiver()

        # --- handlers ---
        self.telemetry = TelemetryHandler()
        self.dataset = DatasetHandler()
        self.logs = LogHandler()

        self.pending_commands = PendingCommands()
        self.ack = AckHandler(self.pending_commands)

        self.pending_params = PendingParams()
        self.params = ParamHandler(self.pending_params)

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