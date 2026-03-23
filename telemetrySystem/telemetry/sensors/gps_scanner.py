import serial
import pynmea2
import time

class GPSMonitor:
    def __init__(self, port: str,  baud: int):
        self.ser = serial.Serial(port, baudrate=baud, timeout=0.1)

        self.last = {
            "fix": False,
            "lat": None,
            "lon": None,
            "speed_kph": None,
        }
    
    def read_gps(self, max_lines: int = 8, max_time: float = 0.2):
        t0 = time.time()
        
        for _ in range(max_lines):
            if time.time() - t0 > max_time:
                break

            line = self.ser.readline().decode(errors="ignore").strip()
            
            if not line.startswith("$GPRMC"):
                continue

            try:
                msg = pynmea2.parse(line)
            except pynmea2.ParseError:
                continue
            
            if getattr(msg, "status", "") != "A":
                self.last["fix"] = False
                continue
            
            self.last["fix"] = True

            if msg.latitude:
                self.last["lat"] = float(f"{msg.latitude:.6f}")
            if msg.longitude:
                self.last["lon"] = float(f"{msg.longitude:.6f}")
                
            spd_knots = None
            try:
                spd_knots = float(msg.spd_over_grnd) if msg.spd_over_grnd else None
            except Exception:
                spd_knots = None

            if spd_knots is not None:
                self.last["speed_kph"] = spd_knots * 1.852
                
            break
        return dict(self.last)
