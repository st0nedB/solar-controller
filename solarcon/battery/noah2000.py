from solarcon.battery.battery import Battery
from solarcon.io.io import Sensor, Consumer
import logging

__all__ = ["Noah2000"]

logger = logging.getLogger(__name__)

class Noah2000(Battery):
    max_power: float = 800
    supported_modes = ["load_first", "battery_first"]
    
    def __init__(
        self,
        state_of_charge_sensor: Sensor,
        mode_sensor: Sensor,
        mode_consumer: Consumer,
        output_power_sensor: Sensor,
        output_power_consumer: Consumer,
    ):
        self.soc_sensor = state_of_charge_sensor
        self.mode_sensor = mode_sensor
        self.mode_consumer = mode_consumer
        self.output_power_sensor = output_power_sensor
        self.output_power_consumer = output_power_consumer

    def get_state_of_charge(self) -> float:
        return self.soc_sensor.get()

    def get_mode(self) -> str:
        mode = self.mode_sensor.get()
        return mode

    def set_mode(self, mode: str):
        if mode not in self.supported_modes:
            logger.error(f"Unsupported mode {mode}. Not setting!")
        self.mode_consumer.set(mode)
        return

    def get_output_power_limit(self) -> float:
        return self.output_power_sensor.get()

    def set_output_power_limit(self, power: float):
        if power > self.max_power:
            power = self.max_power
            logger.warning(
                f"Output power target exceeds batteries configured maximum power. Setting power = {self.max_power}."
            )

        self.output_power_consumer.set(power)
        return
