from dataclasses import dataclass

@dataclass(frozen=True)
class Device:
    device_id: str = "carpi-01"

DEVICE = Device()

@dataclass(frozen=True)
class LocalMQTT:
    host = "localhost"
    port = 1883
    topic = "car/telemetry"

LOCAL_MQTT = LocalMQTT()

UI_PUBLISH_INTERVAL = 0.2

TPMS_SENSORS = {
    "12:30:af:00:00:83": "RR",
    "12:30:af:00:01:3b": "RL",
    "12:30:af:00:04:80": "FR",
    "12:30:af:00:03:7e": "FL",
}

I2C_ADDRESS = 0x48
VOLTAGE_RANGE = 4.096 
RESISTOR = 220.0
VOLTAGE_SUPPLY = 3.3
RESISTANCE_EMPTY = 242.8
RESISTANCE_FULL  = 33.2

GPS_PORT = "/dev/serial0"
GPS_BAUD = 9600
