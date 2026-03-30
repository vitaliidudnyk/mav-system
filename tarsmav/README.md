🔹 Setup (як підняти)
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

PYTHONPATH=./src python -m tarsmav_dev

🔹 Як це працює
TarsMavCore
  ├── MavlinkReceiver (вхідні повідомлення)
  │     └── dispatch → streams (handlers)
  │
  ├── Streams (логіка по типам даних)
  │     ├── RPC (COMMAND_LONG → events + ACK)
  │     ├── Params (PARAM_* ↔ store)
  │     ├── Telemetry (періодичні повідомлення)
  │     ├── Logs (LOG_DATA chunks)
  │     └── Datasets (DEBUG_FLOAT_ARRAY)
  │
  ├── MavlinkSender (вихідні повідомлення)
  │     └── send → transport
  │
  └── Transport (інжектиться зовні)
        ├── Reader (on_data → receiver.feed)
        └── Writer (send bytes)