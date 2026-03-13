import time
from smbus2 import SMBus

class FuelMonitor:
    conversion_address = 0x00
    config_address  = 0x01

    def __init__(self, 
                 i2c_address, 
                 voltage_range, 
                 resistor, 
                 voltage_supply,
                 resistance_empty,
                 resistance_full):
        self.i2c_address = i2c_address
        self.voltage_range = voltage_range
        self.resistor = resistor
        self.voltage_supply = voltage_supply
        self.resistance_empty = resistance_empty
        self.resistance_full = resistance_full
        self.resistance_span = resistance_empty - resistance_full
        self.bus = SMBus(1)
        
    def close(self):
        try: 
            self.bus.close()
        except Exception:
            pass
        
    def ads_config_a0(self):
        return 0xC383

    # Read ADS1115
    def read_adc_raw(self):
        cfg = self.ads_config_a0()
        self.bus.write_i2c_block_data(
            self.i2c_address,
            self.config_address,
            [(cfg >> 8) & 0xFF, cfg & 0xFF]
        )
        time.sleep(1/128 + 0.002)

        data = self.bus.read_i2c_block_data(self.i2c_address, self.conversion_address, 2)
        raw = (data[0] << 8) | data[1]
        if raw & 0x8000:
            raw -= 1 << 16
        return raw

    # Convert raw data to voltage
    def raw_to_volts(self, raw):
        return (raw / 32768.0) * self.voltage_range

    # Convert voltage to ohms
    def volts_to_ohms(self, v):
        v = max(0.001, min(v, self.voltage_supply - 0.001))
        return self.resistor * (v / (self.voltage_supply - v))

    # Convert ohms to percent
    def ohms_to_percent(self, r):
        pct = ((self.resistance_empty - r) / self.resistance_span) * 100.0
        return max(0.0, min(100.0, pct))

    def read(self):
        raw = self.read_adc_raw()
        volts = self.raw_to_volts(raw)
        r_sender = self.volts_to_ohms(volts)
        fuel_pct = self.ohms_to_percent(r_sender)

        return {"percent": round(fuel_pct, 1)}
