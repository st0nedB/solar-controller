from abc import ABC, abstractmethod
import logging
logger = logging.getLogger(__name__)

class _PowerMeter:
    @abstractmethod
    def get_current_power_consumption(self) -> float:
        pass


class MQTTPowerMeter(_PowerMeter):
    def __init__(self, power_reader):
        self.power_reader = power_reader
        return

    def get_current_power_consumption(self) -> float:
        return self.power_reader.get_message()
