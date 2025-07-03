from abc import ABC, abstractmethod
from solarcon.io.io import Sensor, Consumer
import logging

__all__ = ["DeyeSunM160G4", "Inverter"]

logger = logging.getLogger(__name__)

class Inverter(ABC):
    @abstractmethod
    def get_current_production(self) -> float:
        """Method to get the current production in [W]"""
        pass

    @abstractmethod
    def get_current_production_limit(self) -> float:
        """Method to get current production limit in [W]"""
        pass

    @abstractmethod
    def set_production_limit(self, limit: float):
        """Method to set the current limit in [W]"""
        return


class DeyeSunM160G4(Inverter):
    max_power: float = 800.0
    def __init__(
        self,
        power_sensor: Sensor,
        production_limit_sensor: Sensor,
        production_limit_consumer: Consumer,
    ):
        self.power_sensor = power_sensor
        self.production_limit_sensor = production_limit_sensor
        self.production_limit_consumer = production_limit_consumer
        return

    def get_current_production(self):
        return float(self.power_sensor.get())

    def get_current_production_limit(self):
        limit_per = float(self.production_limit_sensor.get()) / 100
        return self.max_power * limit_per

    def set_production_limit(self, limit: float):
        limit_per = round((limit / self.max_power) * 100)

        return self.production_limit_consumer.set(str(limit_per))
