from .rpc_event_listeners import RpcEventListeners
from .tars_mav_simulator import TarsMavSimulator
from .datasets.tars_dataset_mav import TarsDatasetMav
from .rpc.rpc_command_handler import RpcCommandHandler
from .tel.tars_mav_tel import TarsMavTel
from .trans import mavlink_receiver
from .trans.mavlink_receiver import MavLinkReceiver
from .logs.tars_mav_logs import TarsMavLogs
from .trans.mavlink_transmitter import MavlinkTransmitter
from .trans.udp_reader import UdpReader
from .trans.udp_writer import UdpWriter


class TarsMavApp:
    def __init__(self, host: str = "127.0.0.1"):
        self._writer = UdpWriter(host=host, port=14550)
        self._reader = UdpReader(host=host, port=14551)

        self._trans = MavlinkTransmitter(self._writer)

        self.rpc_command = RpcCommandHandler(self._trans)
        self.rpc_listeners = RpcEventListeners()


        self.mavlink_receiver = MavLinkReceiver(self.rpc_command)

        self.logs = TarsMavLogs(self._trans)
        self.tel = TarsMavTel(self._trans)
        self.dataset = TarsDatasetMav(self._trans)



        self.sim = TarsMavSimulator(
            logs=self.logs,
            tel=self.tel,
            dataset=self.dataset,
        )

        self.rpc_command.subscribe(self.rpc_listeners.handle_event)

    def read(self):
        data = self._reader.read()

        if data:
            self.mavlink_receiver.feed(data)