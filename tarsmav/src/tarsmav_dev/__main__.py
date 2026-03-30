import threading
import time

from tarsmav.core import TarsMavCore
from tarsmav_dev.param_definitions import PARAM_DEFINITIONS
from tarsmav_dev.rpc_event_listeners import RpcEventListeners
from tarsmav_dev.tars_mav_simulator import TarsMavSimulator
from tarsmav_dev.transport.udp_reader import UdpReader
from tarsmav_dev.transport.udp_writer import UdpWriter


def main():
    host = "127.0.0.1"

    reader = UdpReader(host=host, port=14551)
    writer = UdpWriter(host=host, port=14550)

    core = TarsMavCore(reader, writer, PARAM_DEFINITIONS)

    rpc_listeners = RpcEventListeners()
    core.rpc_command.subscribe(rpc_listeners.handle_event)

    simulator = TarsMavSimulator(
        logs=core.logs,
        tel=core.tel,
        dataset=core.custom_data_creator,
    )

    threading.Thread(target=core.start, daemon=True).start()

    while True:
        simulator.tick()

        core.tel.tick()
        core.load_metrics.tick()

        time.sleep(0.01)


if __name__ == "__main__":
    main()