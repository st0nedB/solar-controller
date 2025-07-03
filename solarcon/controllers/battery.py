from solarcon.battery.battery import Battery
from solarcon.controllers.controller import Controller
import logging

logger = logging.getLogger(__name__)


class MinChargePowerLimit:
    def __init__(self, min_charge: float):
        self.min_charge = min_charge

    def eval(self, soc: float):
        return soc > self.min_charge


class BatteryController(Controller):
    def __init__(self, battery: Battery):
        self.battery = battery
        
        
    def update(self):
        soc = self.battery.state_of_charge
        
        


# What do I want from this?
# there should be a schedule which can configure the mode and associated max_output_power based on a Condition
# a Condition could be a SoC or a Time
# I dont think it makes sense to change the mode. It should always be load_first, but with not too frequent changes to the power limit
# ~2 a day? 
# -> when sun rises
# -> when sun sets?
# What if it were to depend on the currently available solar input power, i.e., the sliding average of the last 30 minutes
# if this dips below a defined threshold

# ISSUE: Growatt enforces limits on how often the Battery can set a different output power. So does that mean it makes sense to rather change the limit of the Inverter?
# That would create a dependency between the battery and the inverter, which is not desireable. 

