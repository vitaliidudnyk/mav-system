🔹 Setup (як підняти)
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

PYTHONPATH=./src python -m insmav_dev

🔹 Як це працює
InsMavCore
  ├── MavlinkReceiver (вхідні повідомлення)
  │     └── dispatch → streams (handlers)
  │
  ├── Streams (логіка по типам даних)
  │     ├── RPC (COMMAND_LONG → events + ACK)
  │     ├── Params (PARAM_* ↔ store)
  │     ├── Telemetry (обробка вхідних значень)
  │     ├── Logs (LOG_DATA)
  │     └── Datasets (DEBUG_FLOAT_ARRAY)
  │
  ├── MavlinkSender (вихідні повідомлення)
  │     └── send → transport
  │
  └── Transport (інжектиться зовні, insmav_dev)
        ├── UdpReader (on_data → receiver.handle_bytes)
        └── UdpWriter (send bytes)

🔹 Dev layer (insmav_dev)
insmav_dev
  ├── __main__        (entry point)
  ├── UdpReader       (читає UDP)
  ├── UdpWriter       (пише UDP)
  └── RpcGenerator    (генерує тестові RPC)

🔹 Потік даних
UDP → UdpReader → MavlinkReceiver → Handlers (streams)
                                            ↓
                                      бізнес-логіка
                                            ↓
RPC / Params / etc → MavlinkSender → UdpWriter → UDP