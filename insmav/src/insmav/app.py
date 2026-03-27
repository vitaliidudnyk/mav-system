from insmav.rpc.ack_handler import AckHandler
from insmav.rpc.pending_commands import PendingCommands
from insmav.rpc.reliable_rpc_sender import ReliableRpcSender
from src.insmav.handlers.dataset_handler import DatasetHandler
from src.insmav.handlers.log_handler import LogHandler
from src.insmav.handlers.telemetry_handler import TelemetryHandler
from src.insmav.mavlink.mavlink_receiver import MavlinkReceiver
from src.insmav.mavlink.mavlink_sender import MavlinkSender
from src.insmav.rpc.rpc_creator import RpcCreator
from src.insmav.rpc.rpc_mapping import RPC_EVENT_MAPPING
from src.insmav.rpc_generator import RpcGenerator
from src.insmav.udp.udp_reader import UdpReader
from src.insmav.udp.udp_writer import UdpWriter


def main():
    writer = UdpWriter(target_host="127.0.0.1", target_port=14551)

    telemetry_handler = TelemetryHandler()
    dataset_handler = DatasetHandler()
    log_handler = LogHandler()

    pending_commands = PendingCommands()
    ack_handler = AckHandler(pending_commands)

    receiver = MavlinkReceiver(
        telemetry_handler=telemetry_handler,
        dataset_handler=dataset_handler,
        log_handler=log_handler,
        ack_handler=ack_handler,
    )

    reader = UdpReader(host="0.0.0.0", port=14550, on_data_callback=receiver.handle_bytes)

    mavlink_sender = MavlinkSender(writer)

    reliable_rpc_sender = ReliableRpcSender(
        mavlink_sender=mavlink_sender,
        pending_commands=pending_commands,
    )

    rpc_creator = RpcCreator(
        mavlink_sender=reliable_rpc_sender,
        rpc_event_mapping=RPC_EVENT_MAPPING,
    )

    # rpc generator
    rpc_generator = RpcGenerator(rpc_creator)
    rpc_generator.start()

    # запуск
    reader.start()


if __name__ == "__main__":
    main()