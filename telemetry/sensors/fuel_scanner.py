import time
from smbus2 import SMBus

# ADS1115 setup
i2c_address = 0x48
conversion_address = 0x00
config_address  = 0x01
voltage_range = 4.096

# Fuel Sender parameters
resistor = 220.0
voltage_supply = 3.3

resistance_empty = 242.8
resistance_full  = 33.2
resistance_span  = resistance_empty - resistance_full

# ADS1115 Configuration
def ads_config_a0():
    return 0xC383

# Read ADS1115
def read_adc_raw(bus):
    cfg = ads_config_a0()
    bus.write_i2c_block_data(
        i2c_address,
        config_address,
        [(cfg >> 8) & 0xFF, cfg & 0xFF]
    )
    time.sleep(1/128 + 0.002)

    data = bus.read_i2c_block_data(i2c_address, conversion_address, 2)
    raw = (data[0] << 8) | data[1]
    if raw & 0x8000:
        raw -= 1 << 16
    return raw

# Convert raw data to voltage
def raw_to_volts(raw):
    return (raw / 32768.0) * voltage_range

# Convert voltage to ohms
def volts_to_ohms(v):
    v = max(0.001, min(v, voltage_supply - 0.001))
    return resistor * (v / (voltage_supply - v))

# Convert ohms to percent
def ohms_to_percent(r):
    pct = ((resistance_empty - r) / resistance_span) * 100.0
    return max(0.0, min(100.0, pct))

with SMBus(1) as bus:
    while True:
        raw = read_adc_raw(bus)
        volts = raw_to_volts(raw)
        r_sender = volts_to_ohms(volts)
        fuel_pct = ohms_to_percent(r_sender)

        print(
            f"Fuel={fuel_pct:5.1f} %"
        )

        time.sleep(0.5)
