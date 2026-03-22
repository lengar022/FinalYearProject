import json
import ssl
import paho.mqtt.client as mqtt


class CloudMQTTPublisher:
    def __init__(self, host: str, port: int, username: str, password: str, client_id: str = ""):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)

        self.client.username_pw_set(username, password)
        self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
        self.client.connect(host, port, 60)
        self.client.loop_start()

    def publish_json(self, topic: str, payload: dict, qos: int = 0, retain: bool = False):
        self.client.publish(topic, json.dumps(payload), qos=qos, retain=retain)

    def close(self):
        try:
            self.client.loop_stop()
            self.client.disconnect()
        except Exception:
            pass