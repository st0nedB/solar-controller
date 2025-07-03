from collections import deque
from solarcon.inverter import Inverter
from solarcon.powermeter import PowerMeter
from solarcon.controllers.controller import Controller
import time
import logging

logger = logging.getLogger(__name__)


class ZeroConsumptionController(Controller):
    def __init__(
        self,
        powermeter: PowerMeter,
        inverter: Inverter,
        control_threshold: float = 30.0,
        max_power: float = 800.0,
        smoothen: float = 0.5,
        offset: float = 0.0,
    ):
        self.powermeter = powermeter
        self.inverter = inverter
        self.control_threshold = control_threshold
        self.max_power = max_power
        self.smoothen = smoothen
        self.offset = offset
        self.consumption = deque(maxlen=5)
        self.production = deque(maxlen=5)

    def exponential_moving_average(self, values, alpha=0.3):
        if len(values) < 2:
            return values[-1]

        ema = values[0]
        for v in values[1:]:
            ema = alpha * v + (1 - alpha) * ema

        return ema

    def update(self):
        # read the current consumption
        self.consumption.append(self.powermeter.get_current_power_consumption())
        consumption = self.exponential_moving_average(list(self.consumption))
        logger.info(f"Consumption\t\t {consumption:.2f}W")

        # read the current production
        self.production.append(self.inverter.get_current_production())
        production = self.exponential_moving_average(list(self.production))
        logger.info(f"Production\t\t {production:.2f}W")

        # consumption = requirement - production
        #     ^       =      ^            ^
        #     |              |            |
        #  measured     calculated     measured
        # requirement = consumption + production

        # -> consumption should be zero, so ideally
        # requirement = production
        requirement = consumption + production
        logger.info(f"Requirement\t\t {requirement:.2f}W")
        # read the current limit
        limit = self.inverter.get_current_production_limit()
        logger.info(f"Current Limit\t {limit:.2f}W.")

        if abs(requirement - production) > self.control_threshold:
            logger.info(
                f"Difference of {requirement-production:.2f}W exceeds {self.control_threshold:.2f}W."
            )

            new_limit = requirement
            if new_limit >= self.max_power:
                new_limit = self.max_power
            logger.info(f"New Limit \t {new_limit:.2f}")

            if new_limit != limit:
                logger.info(f"Setting new {new_limit:.2f}W limit.")
                self.inverter.set_production_limit(new_limit)

            logger.info("Sleeping for 15s to wait for changes to take effect.")
            time.sleep(15)
            _ = self.inverter.get_current_production_limit()
            logger.info("Power limit updated successfully.")
        else:
            logger.info(
                f"No update required (threshold={self.control_threshold:.2f}W)."
            )
        return
