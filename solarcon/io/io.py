from abc import ABC, abstractmethod
from typing import Any

class Sensor:
    def get(self) -> Any:
        pass
    
class Consumer:
    def set(self, value: Any):
        pass