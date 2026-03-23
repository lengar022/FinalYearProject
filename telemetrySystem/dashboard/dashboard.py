import json
import time
import pygame
import paho.mqtt.client as mqtt

from config import LOCAL_MQTT

STATE = {"last": {}, "updated_at": 0.0}

def on_message(client, userdata, msg):
    try:
        STATE["last"] = json.loads(msg.payload.decode())
        STATE["updated_at"] = time.time()
    except Exception:
        pass

def get(data, *keys, default=None):
    data_copy = data
    for k in keys:
        if not isinstance(data_copy, dict) or k not in data_copy:
            return default
        data_copy = data_copy[k]
    return data_copy

def main():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(LOCAL_MQTT.host, LOCAL_MQTT.port, 30)
    client.subscribe(LOCAL_MQTT.topic)
    client.loop_start()

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    w, h = screen.get_size()

    font_big = pygame.font.SysFont(None, int(h * 0.14))
    font_med = pygame.font.SysFont(None, int(h * 0.07))
    font_small = pygame.font.SysFont(None, int(h * 0.045))

    clock = pygame.time.Clock()
    running = True

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False

        screen.fill((0, 0, 0))

        data = STATE["last"]
        age = (time.time() - STATE["updated_at"]) if STATE["updated_at"] else 999

        speed = get(data, "gps", "speed_kph")
        fuel_pct = get(data, "fuel", "percent")
        water_c = get(data, "engine", "water_temp")

        speed_txt = "--" if speed is None else f"{speed:.0f}"
        screen.blit(font_big.render(speed_txt, True, (255, 255, 255)), (int(w*0.05), int(h*0.05)))
        screen.blit(font_med.render("km/h", True, (180, 180, 180)), (int(w*0.05), int(h*0.05 + h*0.12)))

        fuel_txt = "Fuel: --%" if fuel_pct is None else f"Fuel: {fuel_pct:.0f}%"
        temp_txt = "Water: --°C" if water_c is None else f"Water: {water_c:.1f}°C"
        screen.blit(font_med.render(fuel_txt, True, (255, 255, 255)), (int(w*0.55), int(h*0.08)))
        screen.blit(font_med.render(temp_txt, True, (255, 255, 255)), (int(w*0.55), int(h*0.18)))

        positions = [
            ("front_left",  int(w*0.05), int(h*0.55)),
            ("front_right", int(w*0.55), int(h*0.55)),
            ("rear_left",   int(w*0.05), int(h*0.75)),
            ("rear_right",  int(w*0.55), int(h*0.75)),
        ]

        for wheel, x, y in positions:
            psi = get(data, "tpms", wheel, "psi")
            temp  = get(data, "tpms", wheel, "temp")
            title = wheel.replace("_", " ").upper()
            psi_txt = "--.- psi" if psi is None else f"{psi:.1f} psi"
            temp_txt  = "--.- °C"  if temp is None else f"{temp:.1f} °C"

            if psi is not None and psi < 20:
                psi_color = (255, 0, 0) 
            else:
                psi_color = (255, 255, 255)
                
            pygame.draw.rect(screen, (60, 60, 60), (x, y, int(w*0.4), int(h*0.17)), 2)
            screen.blit(font_small.render(title, True, (200, 200, 200)), (x+15, y+10))
            screen.blit(font_med.render(psi_txt, True, psi_color), (x+15, y+55))
            screen.blit(font_small.render(temp_txt, True, (200, 200, 200)), (x+15, y+120))

        fix = get(data, "gps", "fix", default=False)
        status = f"MQTT age: {age:0.1f}s | GPS fix: {'YES' if fix else 'NO'}"
        screen.blit(font_small.render(status, True, (140, 140, 140)), (int(w*0.05), int(h*0.95)))

        pygame.display.flip()
        clock.tick(25)

    client.loop_stop()
    pygame.quit()

if __name__ == "__main__":
    main()
