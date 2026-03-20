import json
import paho.mqtt.client as mqtt

class LocalMQTTPublisher:
    def __init__(self, host: str, port: int):
        self.client = mqtt.Client()
        self.client.connect(host, port, keepalive=30)

    def publish_json(self, topic: str, payload: dict, qos: int = 0, retain: bool = False):
        self.client.publish(topic, json.dumps(payload), qos=qos, retain=retain)
