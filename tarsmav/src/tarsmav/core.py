from tarsmav.streams.custom_data.custom_data_creator import CustomDataCreator
from tarsmav.mavlink.mavlink_receiver import MavLinkReceiver
from tarsmav.mavlink.mavlink_sender import MavLinkSender
from tarsmav.mavlink.sender_policy import SenderPolicy

from tarsmav.load_metrics_creator import LoadMetricsCreator
from tarsmav.streams.logs.log_creator import LogCreator
from tarsmav.streams.rpc.rpc_command_handler import RpcCommandHandler
from tarsmav.streams.telemetry.tel_creator import TelCreator

from tarsmav.streams.params.param_store import ParamStore
from tarsmav.streams.params.param_handler import ParamHandler


class TarsMavCore:
    def __init__(self, reader: object, sender: object, param_definitions) -> None:
        self._reader = reader
        self._sender = sender

        self._sender_policy = SenderPolicy(
            max_messages_per_sec=50,
            max_bytes_per_sec=8192,
        )

        self._mavlink_sender = MavLinkSender(
            writer=self._sender,
            policy=self._sender_policy,
        )
        self._mavlink_receiver = MavLinkReceiver()

        self.rpc_command = RpcCommandHandler(self._mavlink_sender)
        self.rpc_command.register(self._mavlink_receiver)

        self.param_store = ParamStore(param_definitions)
        self.param_handler = ParamHandler(
            mavlink_sender=self._mavlink_sender,
            param_store=self.param_store,
        )
        self.param_handler.register(self._mavlink_receiver)

        self.logs = LogCreator(self._mavlink_sender)
        self.tel = TelCreator(self._mavlink_sender)
        self.custom_data_creator = CustomDataCreator(self._mavlink_sender)
        self.load_metrics = LoadMetricsCreator(
            custom_data_creator=self.custom_data_creator,
            sender_monitor=self._mavlink_sender.monitor,
            rate_hz=1.0,
        )

        self._reader.set_on_data_callback(self._mavlink_receiver.feed)

    def start(self) -> None:
        self._reader.start()

    def stop(self) -> None:
        self._reader.stop()
        self._sender.close()