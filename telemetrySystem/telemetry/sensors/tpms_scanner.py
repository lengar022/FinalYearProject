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
    print("hello")
    print(payload)
    if len(payload) != 3:
        return None

    byte0, byte1, byte2 = payload[0], payload[1], payload[2]

    if byte1 != 0x01:
        return None

    temp = int(byte0)
    psi = kpa_to_psi(float(byte2))
    return temp, psi

# TPMS Class
@dataclass
class LatestReading:
    ts: float
    psi: float
    temp: int

class TPMSMonitor:
    def __init__(self, sensors, sensorName = "AI-8000"):
        self.sensors = {m.lower(): pos for m, pos in sensors.items()}
        self.sensorName = sensorName
        self.last_pressure_hex: Dict[str, str] = {}
        self.latest_by_pos: Dict[str, LatestReading] = {pos: LatestReading(None, None, 0.0) for pos in self.sensors.values()}
        
    def callback(self, device: BLEDevice, adv: AdvertisementData):
        macAddress = (device.address or "").lower()
        if macAddress not in self.sensors:
            return

        name = (device.name or adv.local_name or "")
        if self.sensorName not in name:
            return

        if not adv.manufacturer_data:
            return

        for _, payload in adv.manufacturer_data.items():
            decodedPayload = decode_tpms(payload)
            if decodedPayload is None:
                continue

            temp, psi = decodedPayload
            
            raw_hex = payload.hex()

            if self.last_pressure_hex.get(macAddress) == raw_hex:
                return
            
            self.last_pressure_hex[macAddress] = raw_hex

            pos = self.sensors[macAddress]
            self.latest_by_pos[pos] = LatestReading(psi=psi, temp=temp, ts=time.time())
            return
        
    async def run_forever(self):
        scanner = BleakScanner(self.callback)
        await scanner.start()
        try: 
            while True:
                await asyncio.sleep(1.0)
        finally:
            await scanner.stop()

    def snapshot(self):
            pos_to_wheel = {"FL": "front_left", "FR": "front_right", "RL": "rear_left", "RR": "rear_right"}

            out = {
                "front_left": {"psi": None, "temp": None, "age": None},
                "front_right": {"psi": None, "temp": None, "age": None},
                "rear_left": {"psi": None, "temp": None, "age": None},
                "rear_right": {"psi": None, "temp": None, "age": None},
            }

            now = time.time()
            for pos, latestReading in self.latest_by_pos.items():
                wheel = pos_to_wheel.get(pos)
                if not wheel:
                    continue
                out[wheel] = {
                    "psi": round(latestReading.psi, 1) if latestReading.psi is not None else None,
                    "temp": float(latestReading.temp) if latestReading.temp is not None else None,
                    "age": round(now - latestReading.ts, 1) if latestReading.ts else None,
                }
            return out