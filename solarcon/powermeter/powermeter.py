from abc import ABC, abstractmethod
from solarcon.io.io import Sensor

__all__ = ["PowerMeter"]

import logging
logger = logging.getLogger(__name__)

class _PowerMeter(ABC):
    @abstractmethod
    def get_current_power_consumption(self) -> float:
        pass


class PowerMeter(_PowerMeter):
    def __init__(self, power_reader: Sensor):
        self.power_reader = power_reader
        return

    def get_current_power_consumption(self) -> float:
        return self.power_reader.get()
