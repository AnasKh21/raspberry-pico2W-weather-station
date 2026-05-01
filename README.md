# 🌤️ Room Weather Station – Pico 2W + BME280

A simple project to turn a Raspberry Pi Pico 2W into a **real-time room weather station**.

The Pico reads temperature, humidity and pressure from a BME280 sensor and exposes a **live dashboard accessible from your phone or computer**.

---

![Dashboard](assets/weather-station.jpeg)

---

##  Requirements

- Raspberry Pi Pico 2W (already flashed with MicroPython)
- BME280 sensor (I2C version)
- Thonny IDE  
  👉 https://thonny.org/

---

##  Wiring

It's the hardest part about the project, I recommend to use a presoldered Raspberry.

### Connections:

| BME280 | Pico 2W |
|--------|--------|
| VCC    | 3.3V   |
| GND    | GND    |
| SDA    | GP4    |
| SCL    | GP5    |

---

## 💻 Setup

### 1. Flash MicroPython on the Pico

If not already done:

👉 https://micropython.org/download/rp2-pico-w/

Plug your Pico while holding BOOTSEL and drag & drop the firmware.

---

### 2. Open Thonny

- Select interpreter: **MicroPython (Raspberry Pi Pico)**
- Connect your board

---

### 3. Add project files

Upload these files to the Pico:

```text
main.py
sensor.py
bme280.py
config.py
