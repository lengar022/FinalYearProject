#!/usr/bin/env python3
"""
TPMS BLE monitor.
"""

import asyncio
import time
from dataclasses import dataclass
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from typing import Dict

# Mapping
sensors = {
    "12:30:af:00:00:83": "RR",  # Rear Right
    "12:30:af:00:01:3b": "RL",  # Rear Left
    "12:30:af:00:04:80": "FR",  # Front Right
    "12:30:af:00:03:7e": "FL",  # Front Left
}

sensorName = "AI-8000"

# store last seen pressure frame per sensor so we only print when it changes
last_pressure_hex: Dict[str, str] = {}

# TPMS Class
@dataclass
class TpmsReading:
    ts: float
    pos: str
    psi: float
    temp: int
    
# Converts kPa to PSI
def kpa_to_psi(kpa: float):
    return kpa * 0.1450377377

def decode_tpms(payload: bytes):
    """
    Sensor sends a 3-byte message:
      byte0: temp
      byte1: frame type
      byte2: pressure in kPa

    Returns (temp, psi) if it's a pressure frame, else None.
    """
    if len(payload) != 3:
        return None

    byte0, byte1, byte2 = payload[0], payload[1], payload[2]

    if byte1 != 0x01:
        return None

    temp = int(byte0)
    psi = kpa_to_psi(float(byte2))
    return temp, psi

# Format reading
def format_reading(reading: TpmsReading):
    ts_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(reading.ts))
    return f"{ts_str} | {reading.pos:2s} | {reading.psi:5.1f} PSI | {reading.temp:2d}°C"


def callback(device: BLEDevice, adv: AdvertisementData):
    macAddress = (device.address or "").lower()
    if macAddress not in sensors:
        return

    name = (device.name or adv.local_name or "")
    if sensorName not in name:
        return

    if not adv.manufacturer_data:
        return

    for payload in adv.manufacturer_data.items():
        decodedPayload = decode_tpms(payload)
        if decodedPayload is None:
            continue

        temp, psi = decodedPayload
        
        raw_hex = payload.hex()

        # Only print when the pressure frame payload changes
        if last_pressure_hex.get(macAddress) == raw_hex:
            return
        
        last_pressure_hex[macAddress] = raw_hex

        reading = TpmsReading(
            ts=time.time(),
            pos=sensors[macAddress],
            psi=psi,
            temp=temp
        )
        print(format_reading(reading))
        return
    
async def main():
    scanner = BleakScanner(callback)
    print("TPMS monitor running (Ctrl+C to stop).")
    print("Timestamp | pos | PSI | temp |")

    while True:
        await scanner.start()
        await asyncio.sleep(5)
        await scanner.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")