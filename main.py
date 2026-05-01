import network
import socket
import time

from config import WIFI_SSID, WIFI_PASSWORD
from sensor import init_sensor, read_sensor


sensor = init_sensor()


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    while not wlan.isconnected():
        print("Connexion WiFi...")
        time.sleep(1)

    ip = wlan.ifconfig()[0]
    print("Connecté:", ip)
    print("Ouvre: http://" + ip)

    return ip


def html_page():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Room Weather Station</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    color: #172033;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
        radial-gradient(circle at top left, #bae6fd 0, transparent 32%),
        radial-gradient(circle at bottom right, #ddd6fe 0, transparent 35%),
        linear-gradient(135deg, #eef6ff, #e0f2fe, #f5f3ff);
}

.panel {
    width: 90%;
    max-width: 430px;
    padding: 28px;
    border-radius: 34px;
    background: rgba(248, 250, 252, 0.72);
    backdrop-filter: blur(14px);
    box-shadow: 0 24px 55px rgba(59, 130, 246, 0.18);
    border: 1px solid rgba(255, 255, 255, 0.85);
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 18px;
}

h1 {
    margin: 0;
    font-size: 31px;
    line-height: 1.05;
    letter-spacing: -1px;
}

.subtitle {
    margin-top: 8px;
    color: #64748b;
    font-size: 14px;
}

.badge {
    background: linear-gradient(135deg, #bfdbfe, #ddd6fe);
    color: #1d4ed8;
    padding: 8px 13px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
}

.hero {
    text-align: center;
    margin: 22px 0 26px;
}

.hero-icon {
    width: 76px;
    height: 76px;
    margin: 0 auto 2px;
    border-radius: 26px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #dbeafe, #ede9fe);
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.8);
}

.hero-icon svg {
    width: 43px;
    height: 43px;
    stroke: #2563eb;
}

.temp {
    font-size: 68px;
    font-weight: 900;
    margin-top: 4px;
    letter-spacing: -3px;
}

.status {
    color: #64748b;
    font-size: 15px;
    margin-top: 4px;
}

.grid {
    display: grid;
    gap: 14px;
}

.card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 17px;
    border-radius: 24px;
    background: rgba(255,255,255,0.68);
    box-shadow: 0 14px 30px rgba(15, 23, 42, 0.07);
    border: 1px solid rgba(255,255,255,0.75);
}

.icon-box {
    width: 50px;
    height: 50px;
    border-radius: 18px;
    background: linear-gradient(135deg, #e0f2fe, #ede9fe);
    display: flex;
    align-items: center;
    justify-content: center;
}

.icon-box svg {
    width: 27px;
    height: 27px;
    stroke: #2563eb;
}

.label {
    color: #64748b;
    font-size: 14px;
}

.value {
    margin-top: 2px;
    font-size: 24px;
    font-weight: 850;
    letter-spacing: -0.5px;
}

.footer {
    text-align: center;
    margin-top: 23px;
    color: #94a3b8;
    font-size: 12px;
}
</style>
</head>

<body>
<div class="panel">
    <div class="header">
        <div>
            <h1>Room Weather<br>Station</h1>
            <div class="subtitle">Capturing and chilling</div>
        </div>
        <div class="badge">LIVE</div>
    </div>

    <div class="hero">
        <div class="hero-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 13.5V5a4 4 0 0 0-8 0v8.5a6 6 0 1 0 8 0z"/>
                <path d="M10 6v9"/>
                <circle cx="10" cy="17" r="2.4"/>
            </svg>
        </div>
        <div class="temp" id="temp">--</div>
        <div class="status">Pico 2W + BME280</div>
    </div>

    <div class="grid">
        <div class="card">
            <div class="icon-box">
                <svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 3s-6 7-6 11a6 6 0 0 0 12 0c0-4-6-11-6-11z"/>
                </svg>
            </div>
            <div>
                <div class="label">Humidity</div>
                <div class="value" id="humidity">--</div>
            </div>
        </div>

        <div class="card">
            <div class="icon-box">
                <svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round">
                    <path d="M4 8h11"/>
                    <path d="M4 13h16"/>
                    <path d="M4 18h8"/>
                    <path d="M17 8a3 3 0 1 1 0 6"/>
                </svg>
            </div>
            <div>
                <div class="label">Pressure</div>
                <div class="value" id="pressure">--</div>
            </div>
        </div>

        <div class="card">
            <div class="icon-box">
                <svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 11l8-7 8 7"/>
                    <path d="M6 10v10h12V10"/>
                    <path d="M10 20v-5h4v5"/>
                </svg>
            </div>
            <div>
                <div class="label">Room mood</div>
                <div class="value" id="mood">--</div>
            </div>
        </div>
    </div>

    <div class="footer">Updated every second</div>
</div>

<script>
function parseValue(value) {
    return parseFloat(value);
}

function getMood(temp, humidity) {
    if (temp < 18) return "Cold room";
    if (temp > 27) return "Warm room";
    if (humidity > 70) return "Humid air";
    if (humidity < 35) return "Dry air";
    return "Comfort zone";
}

async function updateData() {
    const response = await fetch('/data');
    const data = await response.json();

    const temp = parseValue(data.temp);
    const humidity = parseValue(data.humidity);

    document.getElementById('temp').innerText = data.temp;
    document.getElementById('humidity').innerText = data.humidity;
    document.getElementById('pressure').innerText = data.pressure;
    document.getElementById('mood').innerText = getMood(temp, humidity);
}

setInterval(updateData, 1000);
updateData();
</script>
</body>
</html>
"""


def json_data():
    data = read_sensor(sensor)
    return (
        '{"temp":"'
        + data["temp"]
        + '","pressure":"'
        + data["pressure"]
        + '","humidity":"'
        + data["humidity"]
        + '"}'
    )


def send_response(client, content, content_type):
    client.send("HTTP/1.1 200 OK\r\n")
    client.send("Content-Type: " + content_type + "; charset=utf-8\r\n")
    client.send("Connection: close\r\n\r\n")
    client.sendall(content)
    client.close()


ip = connect_wifi()

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 80))
server.listen(1)

print("Serveur lancé")

while True:
    client, addr = server.accept()
    request = client.recv(1024).decode()

    if "GET /data" in request:
        send_response(client, json_data(), "application/json")
    else:
        send_response(client, html_page(), "text/html")
