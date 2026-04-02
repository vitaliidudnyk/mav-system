🔹 Setup (як підняти)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=./src python -m insmav_dev

http://127.0.0.1:8050/ - вмикати dash

## Як це працює

Проєкт складається з трьох основних частин:

### `insmav`
Ядро Inspector-side застосунку.
`InsMavCore` піднімає:
- `MavlinkReceiver` для прийому MAVLink-повідомлень
- handlers для telemetry, datasets, logs, params, rpc
- `MavlinkSender` для відправки команд назад у TARS
- `InspectorState` як спільне thread-safe сховище стану

Також `InsMavCore` надає API для:
- запиту всіх параметрів
- запиту одного параметра
- зміни параметра
- відправки RPC-команд

### `insmav_dash`
UI-шар на Dash.
`DashApp` створює dashboard, підключає layout і callbacks та читає дані зі `state`, який наповнює `InsMavCore`.

У dashboard є вкладки:
- Telemetry
- Datasets
- Params
- Logs
- RPC

### `insmav_dev`
Dev-інфраструктура для локального запуску.
Тут знаходяться UDP transport-класи та генератори тестових запитів/команд.

## Потік роботи

1. `__main__.py` створює `UdpReader` і `UdpWriter`
2. На їх основі створюється `InsMavCore`
3. Окремо створюється `DashApp`
4. `InsMavCore` запускається в окремому потоці та слухає UDP/MAVLink
5. `DashApp` запускає web dashboard
6. Після старту Inspector автоматично запитує всі параметри
7. Усі отримані дані складаються в `InspectorState`, а dashboard їх відображає

## Призначення

`insmav` — це Inspector/ground-side частина системи, яка:
- приймає телеметрію та дані
- показує їх у dashboard
- дозволяє читати/міняти params
- дозволяє відправляти RPC-команди в TARS