from typing import Optional, Callable, Optional
from collections import deque
import paho.mqtt.client as mqtt
import logging
from .io import Sensor, Consumer

logger = logging.getLogger(__name__)


class Mqtt:
    def __init__(
        self,
        broker: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        port: int = 1883,
    ):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()
        self.subscriptions = {}
        self.client.on_message = self._on_message
        if username is not None:
            self.client.username_pw_set(username, password)

    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def disconnect(self):
        self.client.disconnect()

    def subscribe(self, topic: str, callback: Callable[[str], None]):
        if topic not in self.subscriptions:
            self.subscriptions[topic] = []
            self.client.subscribe(topic)

        self.subscriptions[topic].append(callback)

    def _on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode()
        for cb in self.subscriptions.get(topic, []):
            cb(payload)


class MqttSensor(Sensor):
    def __init__(
        self, mqtt_instance: Mqtt, topic: str, filter: Optional[Callable] = None
    ):
        self.topic = topic
        self.filter = filter
        self.messages = deque(maxlen=10)
        mqtt_instance.subscribe(topic, self._on_message)

    def _on_message(self, payload: str):
        self.messages.append(payload)

    def get(self):
        if not self.messages:
            return None

        message = self.messages[-1]
        return self.filter(message) if self.filter else message


class MqttConsumer(Consumer):
    def __init__(self, mqtt_instance: Mqtt, topic: str):
        self.mqtt = mqtt_instance
        self.topic = topic

    def set(self, value: str):
        self.mqtt.client.publish(self.topic, value)
