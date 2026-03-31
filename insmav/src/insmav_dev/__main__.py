import threading
import time

from insmav.core import InsMavCore
from insmav_dash.dash_app import DashApp
from insmav_dev.transport.udp_reader import UdpReader
from insmav_dev.transport.udp_writer import UdpWriter


def main() -> None:
    host = "127.0.0.1"

    reader = UdpReader(host=host, port=14550)
    writer = UdpWriter(target_host=host, target_port=14551)

    core = InsMavCore(reader=reader, writer=writer)
    dash_app = DashApp(core)

    core_thread = threading.Thread(target=core.start, daemon=True)
    dash_thread = threading.Thread(target=dash_app.run, daemon=True)

    core_thread.start()
    dash_thread.start()

    time.sleep(0.5)
    core.request_all_params()

    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("[main] Stopping...")
        reader.stop()


if __name__ == "__main__":
    main()