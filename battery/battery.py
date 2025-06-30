from abc import ABC, abstractmethod

class _Battery(ABC):
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
    
    
        
        
        
class MQTTBattery(_Battery):
    def __init__(self, state_of_charge_reader, mode_reader, mode_writer):
        self.soc_reader = state_of_charge_reader
        self.mode_reader = mode_reader
        self.mode_writer = mode_writer
        
    def get_state_of_charge(self) -> float:
        return self.soc_reader.get_message()
    
    def get_mode(self) -> str:
        mode = self.mode_reader()
        return mode
    
    def set_mode(self, mode: str):
        self.mode_writer(mode)
        return 