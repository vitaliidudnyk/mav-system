import threading

from insmav.core import InsMavCore
from insmav_dev.param_request_generator import ParamRequestGenerator
from insmav_dev.rpc_generator import RpcGenerator
from insmav_dev.transport.udp_reader import UdpReader
from insmav_dev.transport.udp_writer import UdpWriter


def main() -> None:
    host = "127.0.0.1"

    reader = UdpReader(host=host, port=14550)
    writer = UdpWriter(target_host=host, target_port=14551)

    core = InsMavCore(reader=reader, writer=writer)

    rpc_generator = RpcGenerator(core.rpc)
    param_request_generator = ParamRequestGenerator(
        param_requester=core.param_requester,
        interval_sec=5.0,
    )

    core_thread = threading.Thread(target=core.start)
    params_thread = threading.Thread(target=param_request_generator.start)

    core_thread.start()
    params_thread.start()

    try:
        rpc_generator.start()
    except KeyboardInterrupt:
        print("[main] Stopping...")
        reader.stop()
        rpc_generator.stop()
        param_request_generator.stop()
        core_thread.join()
        params_thread.join()


if __name__ == "__main__":
    main()