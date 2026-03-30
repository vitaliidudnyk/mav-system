import math
import time

from tarsmav.streams.custom_data.custom_data_sets import AttitudeDebug, ImuDebug, BatteryDebug
from tarsmav.custom_data_creator import CustomDataCreator
from tarsmav.streams.logs.log_creator import LogCreator
from tarsmav.streams.telemetry.tel_creator import TelCreator


class TarsMavSimulator:
    def __init__(
        self,
        tel: TelCreator,
        logs: LogCreator,
        dataset: CustomDataCreator,
    ):
        self._tel = tel
        self._logs = logs
        self._dataset = dataset

        self._started_at = time.monotonic()
        self._step = 0

        self._last_log_at = 0.0
        self._last_dataset_at = 0.0

        self._log_index = 0
        self._dataset_index = 0

    def tick(self) -> None:
        now = time.monotonic()
        t = now - self._started_at

        self._update_tel(t)
        self._tel.tick()

        if now - self._last_log_at >= 2.0:
            self._send_next_log(t)
            self._last_log_at = now

        if now - self._last_dataset_at >= 1.0:
            self._send_next_dataset(t)
            self._last_dataset_at = now

        self._step += 1

    def _update_tel(self, t: float) -> None:
        roll = math.sin(t) * 0.3
        pitch = math.cos(t * 0.7) * 0.2
        yaw = math.sin(t * 0.4) * 1.2

        rollspeed = math.cos(t) * 0.3
        pitchspeed = -math.sin(t * 0.7) * 0.14
        yawspeed = math.cos(t * 0.4) * 0.48

        battery_remaining = max(0, 100 - int(t * 0.5))
        voltage_battery = max(10500, 12600 - int(t * 8))
        current_battery = 120 + int(abs(math.sin(t)) * 40)

        self._tel.data.heartbeat.mav_type = 6
        self._tel.data.heartbeat.autopilot = 8
        self._tel.data.heartbeat.base_mode = 0
        self._tel.data.heartbeat.custom_mode = 0
        self._tel.data.heartbeat.system_status = 4
        self._tel.data.heartbeat.mavlink_version = 3

        self._tel.data.attitude.time_boot_ms = int(t * 1000)
        self._tel.data.attitude.roll = roll
        self._tel.data.attitude.pitch = pitch
        self._tel.data.attitude.yaw = yaw
        self._tel.data.attitude.rollspeed = rollspeed
        self._tel.data.attitude.pitchspeed = pitchspeed
        self._tel.data.attitude.yawspeed = yawspeed

        self._tel.data.sys_status.onboard_control_sensors_present = 0
        self._tel.data.sys_status.onboard_control_sensors_enabled = 0
        self._tel.data.sys_status.onboard_control_sensors_health = 0
        self._tel.data.sys_status.load = 320
        self._tel.data.sys_status.voltage_battery = voltage_battery
        self._tel.data.sys_status.current_battery = current_battery
        self._tel.data.sys_status.battery_remaining = battery_remaining
        self._tel.data.sys_status.drop_rate_comm = 0
        self._tel.data.sys_status.errors_comm = 0
        self._tel.data.sys_status.errors_count1 = 0
        self._tel.data.sys_status.errors_count2 = 0
        self._tel.data.sys_status.errors_count3 = 0
        self._tel.data.sys_status.errors_count4 = 0

    def _send_next_log(self, t: float) -> None:
        generators = [
            self._log_gen_1,
            self._log_gen_2,
            self._log_gen_3,
        ]

        generator = generators[self._log_index % len(generators)]
        self._logs.log(generator(t))
        self._log_index += 1

    def _send_next_dataset(self, t: float) -> None:
        generators = [
            self._dataset_gen_1,
            self._dataset_gen_2,
            self._dataset_gen_3,
        ]

        generator = generators[self._dataset_index % len(generators)]
        dataset = generator(t)
        self._dataset.send(dataset)
        self._dataset_index += 1

    def _log_gen_1(self, t: float) -> str:
        return f"[sim] step={self._step} uptime={t:.2f}s system ok"

    def _log_gen_2(self, t: float) -> str:
        roll = self._tel.data.attitude.roll
        pitch = self._tel.data.attitude.pitch
        yaw = self._tel.data.attitude.yaw
        return (
            f"[imu] roll={roll:.3f} pitch={pitch:.3f} yaw={yaw:.3f}"
        )

    def _log_gen_3(self, t: float) -> str:
        battery = self._tel.data.sys_status.battery_remaining
        voltage = self._tel.data.sys_status.voltage_battery
        return (
            f"[power] battery={battery}% voltage_mv={voltage}"
        )

    def _dataset_gen_1(self, t: float) -> ImuDebug:
        return ImuDebug(
            roll=self._tel.data.attitude.roll,
            pitch=self._tel.data.attitude.pitch,
            yaw=self._tel.data.attitude.yaw,
            gyro_x=self._tel.data.attitude.rollspeed,
            gyro_y=self._tel.data.attitude.pitchspeed,
            gyro_z=self._tel.data.attitude.yawspeed,
        )

    def _dataset_gen_2(self, t: float) -> AttitudeDebug:
        return AttitudeDebug(
            roll=self._tel.data.attitude.roll,
            pitch=self._tel.data.attitude.pitch,
            yaw=self._tel.data.attitude.yaw,
        )

    def _dataset_gen_3(self, t: float) -> BatteryDebug:
        return BatteryDebug(
            voltage=float(self._tel.data.sys_status.voltage_battery) / 1000.0,
            current=float(self._tel.data.sys_status.current_battery) / 100.0,
            remaining=float(self._tel.data.sys_status.battery_remaining),
        )