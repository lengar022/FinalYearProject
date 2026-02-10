import serial
import pynmea2
from datetime import datetime

ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)

while True:
    line = ser.readline().decode(errors="ignore").strip()
    if line.startswith("$GPRMC"):
        try:
            msg = pynmea2.parse(line)
            if msg.status == "A": 
                speed_kmh = msg.spd_over_grnd * 1.852
                print(
                    f"{datetime.now().isoformat(timespec='seconds')} "
                    f"lat={msg.latitude:.6f} lon={msg.longitude:.6f} "
                    f"speed={speed_kmh}"
                )
        except pynmea2.ParseError:
            pass
