from abc import ABC, abstractmethod
import logging
logger = logging.getLogger(__name__)

class _Inverter(ABC):
    def __init__(self, max_power: float | int):
        self.max_power = max_power

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


class MQTTInverter(_Inverter):
    def __init__(
        self,
        power_reader,
        production_limit_reader,
        production_limit_setter,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.power_reader = power_reader
        self.production_limit_reader = production_limit_reader
        self.production_limit_setter = production_limit_setter
        return

    def get_current_production(self):
        return float(self.power_reader.get_message())

    def get_current_production_limit(self):
        limit_per = float(self.production_limit_reader.get_message()) / 100
        return self.max_power * limit_per

    def set_production_limit(self, limit: float):
        limit_per = round((limit / self.max_power) * 100)

        return self.production_limit_setter.publish(str(limit_per))
