from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

__all__ = ["Battery"]


class Battery(ABC):
    @property
    @abstractmethod
    def state_of_charge(self) -> float:
        pass

    @abstractmethod
    def get_mode(self) -> str:
        pass

    @abstractmethod
    def set_mode(self, mode: str):
        pass

    @abstractmethod
    def get_output_power_limit(self) -> float:
        pass

    @abstractmethod
    def set_output_power_limit(self, power: float):
        pass