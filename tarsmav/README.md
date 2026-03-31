🔹 Setup (як підняти)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=./src python -m tarsmav_dev

## 🔹 Як це працює
TarsMavCore — збирає всі компоненти.

IN:  Reader → MavlinkReceiver → dispatch → Streams  
OUT: Streams → MavlinkSender → Policy → Writer  

Streams:
- RPC → COMMAND_LONG → events + ACK
- Params → PARAM_* ↔ store
- Telemetry / Logs / Datasets → генерують повідомлення

Зв’язки:
- Core інжектить sender у streams
- Streams реєструються в receiver
- Receiver тільки парсить і диспатчить
- Sender — єдина точка відправки

Runtime:
- Reader — окремий потік (blocking)
- main loop → simulator + tick()

Ідея:
єдиний вхід (receiver) + єдиний вихід (sender)

## 🔹 Mavlink layer

- **MavLinkReceiver** — приймає сирі байти, парсить їх у MAVLink-повідомлення і диспатчить у підписані callbacks за `message_type`.
- **MavLinkSender** — єдина точка відправки MAVLink-повідомлень; пакує message у bytes, перевіряє policy, відправляє через writer.
- **SenderMonitor** — збирає runtime-метрики відправки: messages/sec, bytes/sec, average load, high-load time, dropped low-priority messages.
- **SenderPolicy** — задає ліміти відправки та пріоритет повідомлень:
  - `CRITICAL` — не дропаються
  - `HIGH` — звичайні повідомлення
  - `LOW` — можуть дропатись при перевищенні лімітів

### Зв’язки

- `Reader` передає байти у `MavLinkReceiver.feed()`
- `MavLinkReceiver` після парсингу викликає subscribers потрібного типу повідомлення
- Streams реєструють свої handlers через `subscribe(...)`
- Усі вихідні повідомлення йдуть через `MavLinkSender.send(...)`
- `MavLinkSender` використовує:
  - `SenderPolicy` — щоб визначити пріоритет і правила дропу
  - `SenderMonitor` — щоб рахувати навантаження і warning-и
  - `Writer` — щоб фактично відправити bytes у transport

- ## 🔹 Telemetry stream

- **TelData** — спільне сховище telemetry payload-ів (`heartbeat`, `attitude`, `sys_status`).
- **TelMessageType** — перелік типів telemetry-повідомлень, які підтримує стрім.
- **DEFAULT_TEL_RATES_HZ** — дефолтні частоти відправки для кожного telemetry message type.
- **TelMessageFactory** — будує конкретне MAVLink-повідомлення з `TelData` залежно від `TelMessageType`.
- **TelCreator** — керує періодичною відправкою телеметрії через `tick()` з потрібною частотою.

### Зв’язки

- `TelCreator` зберігає `TelData`
- `TelCreator.tick()` перевіряє, які telemetry message вже час відправити
- для кожного типу викликає `TelMessageFactory.create_message(...)`
- готове MAVLink-повідомлення передається у `MavLinkSender.send(...)`
- частоти можна змінювати через `set_rate(...)`

## 🔹 RPC stream

- **RpcCommandHandler** — обробляє `COMMAND_LONG`, конвертує у події і розсилає subscribers.
- **RPC_EVENT_MAPPING** — мапінг `command → event class`.
- **RpcEvent** — базовий клас для RPC подій.
- Конкретні події (наприклад `StartMissionEvent`, `SetModeEvent`, `CalibrateImuEvent`) — описують payload.

### Зв’язки

- `RpcCommandHandler.register(...)` підписується на `COMMAND_LONG` у `MavLinkReceiver`
- при отриманні повідомлення:
  - бере `command`
  - знаходить `event_class` у `RPC_EVENT_MAPPING`
  - мапить `param1..7 → dataclass`
- створений event передається у всі subscribers через `_emit(...)`
- після обробки завжди відправляється ACK через `MavLinkSender`

### Поведінка

- unknown command → `MAV_RESULT_UNSUPPORTED`
- success → `MAV_RESULT_ACCEPTED`
- exception → `MAV_RESULT_FAILED`