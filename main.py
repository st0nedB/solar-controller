import time
import json
import rootutils
root = rootutils.setup_root(__file__, dotenv=True, pythonpath=True, cwd=False)

from mqtt.mqtt import MQTT, Reader, Writer
from inverter.inverter import MQTTInverter
from powermeter.powermeter import MQTTPowerMeter
from controllers.controllers import ZeroConsumptionController

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    mqtt = MQTT(
        broker="mqtt.emptyvoid.xyz",
        port=1883,
        username="mqtter",
        password="hsJHXNNHxd7SqLhNrBS$44QtmDwAN2jYR4",
    )
    mqtt.connect()

    power_reader_house = Reader(
        mqtt,
        "tele/esp_pwr_mtr/SENSOR",
        filter=lambda message: json.loads(message)["ENERGY"]["Power"],
    )
    
    power_reader_solar = Reader(mqtt, "deye/ac/active_power")
    power_reader_solar_limit = Reader(mqtt, "deye/settings/active_power_regulation")
    power_setter_solar = Writer(mqtt, "deye/settings/active_power_regulation/command")

    powermeter = MQTTPowerMeter(
        power_reader=power_reader_house,
    )
    inverter = MQTTInverter(
        power_reader=power_reader_solar,
        production_limit_reader=power_reader_solar_limit,
        production_limit_setter=power_setter_solar,
        max_power=1600,
    )
    controller = ZeroConsumptionController(
        powermeter=powermeter,
        inverter=inverter,
        control_threshold=30,
        max_power=800,
    )

    while True:
        time.sleep(10)
        logger.info(f"Starting update")
        controller.update()
        logger.info(f"Update finished.\n\n")


if __name__ == "__main__":
    main()
