import asyncio
from datetime import datetime, timezone

from config import (
    DEVICE,
    LOCAL_MQTT,
    DASHBOARD_PUBLISH_INTERVAL,
    TPMS_SENSORS,
    I2C_ADDRESS,
    VOLTAGE_RANGE,
    RESISTOR,
    VOLTAGE_SUPPLY,
    RESISTANCE_EMPTY,
    RESISTANCE_FULL,
    GPS_PORT,
    GPS_BAUD,
)

from telemetry.mqtt_local import LocalMQTTPublisher
from telemetry.sensors.tpms_scanner import TPMSMonitor
from telemetry.sensors.gps_scanner import GPSMonitor
from telemetry.sensors.temp_scanner import TempMonitor
from telemetry.sensors.fuel_scanner import FuelMonitor


def get_current_time():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

async def main():
    print("LOCAL PUBLISHER STARTED | LOCAL TOPIC =", LOCAL_MQTT.topic)

    local_mqtt = LocalMQTTPublisher(
        LOCAL_MQTT.host,
        LOCAL_MQTT.port,
    )

    tpms = TPMSMonitor(TPMS_SENSORS)
    gps = GPSMonitor(GPS_PORT, GPS_BAUD)
    temp = TempMonitor()
    fuel = FuelMonitor(
        i2c_address=I2C_ADDRESS,
        voltage_range=VOLTAGE_RANGE,
        resistor=RESISTOR,
        voltage_supply=VOLTAGE_SUPPLY,
        resistance_empty=RESISTANCE_EMPTY,
        resistance_full=RESISTANCE_FULL,
    )

    last_tpms = {
        "front_left": {"psi": None, "temp": None, "age": None},
        "front_right": {"psi": None, "temp": None, "age": None},
        "rear_left": {"psi": None, "temp": None, "age": None},
        "rear_right": {"psi": None, "temp": None, "age": None},
    }

    last_temp = None

    last_gps = {
        "fix": False,
        "lat": None,
        "lon": None,
        "speed_kph": None,
    }

    last_fuel = {
        "percent": None,
    }

    TEMP_PERIOD = 1.0
    GPS_PERIOD = 1.0
    FUEL_PERIOD = 1.0

    async def temp_worker():
        nonlocal last_temp
        while True:
            try:
                temp_reading = await asyncio.to_thread(temp.read_temp)
                if temp_reading is not None:
                    last_temp = temp_reading
            except Exception:
                pass
            await asyncio.sleep(TEMP_PERIOD)

    async def gps_worker():
        nonlocal last_gps
        while True:
            try:
                gps_reading = await asyncio.to_thread(gps.read_gps)
                last_gps["fix"] = bool(gps_reading.get("fix", False))

                if gps_reading.get("lat") is not None:
                    last_gps["lat"] = gps_reading["lat"]

                if gps_reading.get("lon") is not None:
                    last_gps["lon"] = gps_reading["lon"]

                if gps_reading.get("speed_kph") is not None:
                    last_gps["speed_kph"] = gps_reading["speed_kph"]
            except Exception:
                pass
            await asyncio.sleep(GPS_PERIOD)

    async def fuel_worker():
        nonlocal last_fuel
        while True:
            try:
                fuel_reading = await asyncio.to_thread(fuel.read_fuel)
                if fuel_reading is not None:
                    last_fuel = fuel_reading
            except Exception:
                pass
            await asyncio.sleep(FUEL_PERIOD)

    asyncio.create_task(tpms.run_forever())
    asyncio.create_task(temp_worker())
    asyncio.create_task(gps_worker())
    asyncio.create_task(fuel_worker())


    while True:
        try:
            snap = tpms.snapshot()
            for wheel in last_tpms:
                if snap[wheel].get("psi") is not None:
                    last_tpms[wheel]["psi"] = snap[wheel]["psi"]
                if snap[wheel].get("temp") is not None:
                    last_tpms[wheel]["temp"] = snap[wheel]["temp"]
                last_tpms[wheel]["age"] = snap[wheel].get("age")
        except Exception:
            pass

        payload = {
            "ts": get_current_time(),
            "device_id": DEVICE.device_id,
            "tpms": {
                wheel: {
                    "psi": last_tpms[wheel]["psi"],
                    "temp": last_tpms[wheel]["temp"],
                }
                for wheel in last_tpms
            },
            "engine": {
                "water_temp": round(last_temp, 1) if last_temp is not None else None
            },
            "fuel": last_fuel,
            "gps": {
                "fix": last_gps["fix"],
                "lat": last_gps["lat"],
                "lon": last_gps["lon"],
                "speed_kph": round(last_gps["speed_kph"], 1) if last_gps["speed_kph"] is not None else None,
            },
        }
        
        try:
            local_mqtt.publish_json(LOCAL_MQTT.topic, payload, qos=0, retain=False)
        except Exception as e:
            print(f"LOCAL_MQTT_PUBLISH_FAILED: {e}")

        await asyncio.sleep(DASHBOARD_PUBLISH_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())