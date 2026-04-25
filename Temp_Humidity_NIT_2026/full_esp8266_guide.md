# 🌐 IoT Weather Station with ESP8266 (Direct WiFi to Database)

> **Pure IoT project** — ESP8266 reads DHT11 sensor and sends data **directly over WiFi** to a MySQL database via a PHP API. No Python bridge needed!

**Scenario:** NYAGATARE Greenhouse Farms Ltd needs a wireless weather monitoring system. The ESP8266 is placed inside the greenhouse, connects to WiFi, and pushes climate data to a remote server every few seconds. Workers view real-time data on a web dashboard from anywhere on the network.

---

## 📋 Table of Contents

1. [How It Works](#-how-it-works)
2. [Materials](#-materials)
3. [Wiring Diagram](#-wiring-diagram)
4. [Software Setup](#-software-setup)
5. [Database Setup](#-database-setup)
6. [Step 1: PHP Insert API](#-step-1-php-insert-api)
7. [Step 2: ESP8266 Code](#-step-2-esp8266-code)
8. [Step 3: PHP Web Dashboard](#-step-3-php-web-dashboard)
9. [Step 4: Run the System](#-step-4-run-the-system)
10. [Expected Results](#-expected-results)
11. [Troubleshooting](#-troubleshooting)
12. [Presentation Q&A](#-presentation-qa)

---

## 🏗 How It Works

```
   ┌──────────┐                    ┌──────────────┐
   │  DHT11   │──── reads ────────▶│   ESP8266    │
   │  Sensor  │                    │   (WiFi)     │
   └──────────┘                    └──────┬───────┘
                                          │ HTTP POST
                                          ▼
                            ┌─────────────────────────┐
                            │  Your PC (XAMPP Server) │
                            │                         │
                            │  insert.php  ◀──── API  │
                            │      │                  │
                            │      ▼                  │
                            │  MySQL: Weather_db      │
                            │      │                  │
                            │      ▼                  │
                            │  index.php  (Dashboard) │
                            └─────────────────────────┘
                                          ▲
                                          │ Browser
                                       👨‍🌾 You
```

**The flow in plain English:**
1. ESP8266 reads DHT11 every 5 seconds
2. ESP8266 connects to your WiFi
3. ESP8266 sends data to `insert.php` on your PC via HTTP POST
4. `insert.php` saves it to MySQL
5. `index.php` shows the data in your browser

---

## 📦 Materials

### Hardware

| # | Component | Qty |
|:-:|-----------|:---:|
| 1 | ESP8266 NodeMCU + USB cable | 1 |
| 2 | DHT11 sensor | 1 |
| 3 | Red, Yellow, Green LEDs | 1 each |
| 4 | 220Ω resistors | 3 |
| 5 | 10kΩ resistor (if DHT11 has no breakout) | 1 |
| 6 | Breadboard + jumper wires | 1 set |

### Software & Network

- Arduino IDE with **ESP8266 board package**
- XAMPP (Apache + MySQL + PHP)
- **WiFi network** that both your PC and ESP8266 can connect to
- Your PC's local IP address (we'll find it together)

---

## 🔌 Wiring Diagram

| Component | Pin | NodeMCU Pin |
|-----------|-----|-------------|
| DHT11 VCC | + | **3.3V** |
| DHT11 DATA | data | **D4** (GPIO2) |
| DHT11 GND | − | GND |
| Red LED + 220Ω | anode | **D5** |
| Yellow LED + 220Ω | anode | **D6** |
| Green LED + 220Ω | anode | **D7** |
| All LED cathodes | − | GND |

> 💡 If your DHT11 module has 3 pins (breakout board), the 10kΩ pull-up resistor is built in. If it has 4 pins, add a 10kΩ resistor between DATA and 3.3V.

---

## 💻 Software Setup

### Step A: Install ESP8266 Board in Arduino IDE

1. Open **Arduino IDE → File → Preferences**
2. In **"Additional Board Manager URLs"**, paste:
```
   http://arduino.esp8266.com/stable/package_esp8266com_index.json
```
3. Click **OK**
4. Go to **Tools → Board → Boards Manager**
5. Search **"esp8266"** → click **Install** on "esp8266 by ESP8266 Community"
6. Now select **Tools → Board → ESP8266 Boards → NodeMCU 1.0 (ESP-12E Module)**

### Step B: Install Required Libraries

Go to **Sketch → Include Library → Manage Libraries...** and install:

- **DHT sensor library by Adafruit**
- **Adafruit Unified Sensor**

### Step C: Start XAMPP

Open XAMPP Control Panel → Start **Apache** ✅ and **MySQL** ✅.

### Step D: Find Your PC's Local IP Address ⭐ IMPORTANT

The ESP8266 needs to know your PC's IP address to send data.

Open **Command Prompt** (not PowerShell) and run:

```cmd
ipconfig
```

Look for the section **"Wireless LAN adapter Wi-Fi"** → find **"IPv4 Address"**.

It looks like:
```
IPv4 Address. . . . . . . . . . . : 192.168.1.105
```

**Write this down — you'll need it!** Example: `192.168.1.105`

> ⚠️ Both your PC and ESP8266 **MUST be on the same WiFi network**.

### Step E: Allow Apache Through Windows Firewall (CRITICAL!)

By default, Windows blocks incoming requests. Allow Apache:

1. Press **Win** → search **"Windows Defender Firewall"** → open it
2. Click **"Allow an app or feature through Windows Defender Firewall"**
3. Click **"Change settings"** → **"Allow another app..."**
4. Browse to `C:\xampp\apache\bin\httpd.exe` → Add it
5. Make sure **both Private and Public** boxes are checked ✅

Or quick way (run PowerShell as Administrator):
```powershell
New-NetFirewallRule -DisplayName "Apache HTTP" -Direction Inbound -LocalPort 80,8080 -Protocol TCP -Action Allow
```

---

## 🗄 Database Setup

Open `http://localhost/phpmyadmin` (or `http://localhost:8080/phpmyadmin`).

Click **SQL** tab → paste → **Go**:

```sql
CREATE DATABASE Weather_db;

USE Weather_db;

CREATE TABLE Weather_data (
  Id INT AUTO_INCREMENT PRIMARY KEY,
  Temperature FLOAT NOT NULL,
  Humidity FLOAT NOT NULL,
  Status VARCHAR(50) NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 📂 Project Folder Structure

Create folder `C:\xampp\htdocs\weather\` and inside it create **two files**:

```
C:\xampp\htdocs\weather\
├── insert.php       ← receives data from ESP8266
└── index.php        ← dashboard for browsers
```

---

## 📡 Step 1: PHP Insert API

Save as `C:\xampp\htdocs\weather\insert.php`:

```php
<?php
// API endpoint that the ESP8266 calls to save weather data
$conn = new mysqli('localhost', 'root', '', 'Weather_db');
if ($conn->connect_error) {
    http_response_code(500);
    die("DB Error: " . $conn->connect_error);
}

// Get values from POST request
$temp   = isset($_POST['temp'])   ? floatval($_POST['temp'])   : null;
$hum    = isset($_POST['hum'])    ? floatval($_POST['hum'])    : null;
$status = isset($_POST['status']) ? $_POST['status']           : null;

if ($temp === null || $hum === null || !$status) {
    http_response_code(400);
    die("Missing parameters");
}

$stmt = $conn->prepare("INSERT INTO Weather_data (Temperature, Humidity, Status) VALUES (?, ?, ?)");
$stmt->bind_param("dds", $temp, $hum, $status);

if ($stmt->execute()) {
    echo "OK - Saved: T=$temp H=$hum Status=$status";
} else {
    http_response_code(500);
    echo "Insert failed: " . $stmt->error;
}

$stmt->close();
$conn->close();
?>
```

### Test It Before Continuing!

In your browser, visit:
```
http://localhost/weather/insert.php?temp=25&hum=60&status=NORMAL
```

Wait — that won't work because `insert.php` expects POST not GET. Let's test with PowerShell:

```powershell
Invoke-RestMethod -Uri "http://localhost/weather/insert.php" -Method POST -Body @{temp=25.5; hum=60; status="NORMAL"}
```

You should see: `OK - Saved: T=25.5 H=60 Status=NORMAL` ✅

Check phpMyAdmin → `Weather_db` → `Weather_data` → you should see one row! 🎉

---

## 🔌 Step 2: ESP8266 Code

Save as `weather_esp8266.ino`. **Update three things at the top with your own values!**

```cpp
// ============================================================
// NYAGATARE Greenhouse - ESP8266 Weather Station
// Sends temperature & humidity directly to MySQL via PHP API
// ============================================================
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <DHT.h>

// ⚠️ CHANGE THESE 3 LINES! ⚠️
const char* WIFI_SSID     = "YourWiFiName";
const char* WIFI_PASSWORD = "YourWiFiPassword";
const char* SERVER_URL = "http://192.168.18.27:8080/weather/insert.php";;  // your PC's IP

// Pins
#define DHT_PIN  D4
#define DHT_TYPE DHT11
#define LED_RED    D5
#define LED_YELLOW D6
#define LED_GREEN  D7

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_YELLOW, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  Serial.begin(115200);
  delay(1000);
  dht.begin();

  // Connect to WiFi
  Serial.print("Connecting to WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("✅ WiFi Connected! IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();

  if (isnan(temp) || isnan(hum)) {
    Serial.println("❌ Failed to read DHT11");
    delay(2000);
    return;
  }

  // Decide status & light LEDs
  digitalWrite(LED_RED, LOW);
  digitalWrite(LED_YELLOW, LOW);
  digitalWrite(LED_GREEN, LOW);

  String status;
  if (temp > 30) {
    digitalWrite(LED_RED, HIGH);
    status = "HOT";
  } else if (hum < 40) {
    digitalWrite(LED_YELLOW, HIGH);
    status = "DRY";
  } else {
    digitalWrite(LED_GREEN, HIGH);
    status = "NORMAL";
  }

  Serial.printf("T=%.2f°C  H=%.2f%%  Status=%s\n", temp, hum, status.c_str());

  // Send to server
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;
    http.begin(client, SERVER_URL);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    String payload = "temp=" + String(temp, 2) +
                     "&hum=" + String(hum, 2) +
                     "&status=" + status;

    int code = http.POST(payload);
    if (code > 0) {
      Serial.printf("✅ Server response (%d): %s\n", code, http.getString().c_str());
    } else {
      Serial.printf("❌ HTTP error: %s\n", http.errorToString(code).c_str());
    }
    http.end();
  } else {
    Serial.println("❌ WiFi disconnected");
  }

  delay(5000); // send every 5 seconds
}
```

### Upload Steps

1. **Tools → Board → NodeMCU 1.0 (ESP-12E Module)**
2. **Tools → Port → COMx** (your ESP8266's port)
3. **Tools → Upload Speed → 115200**
4. Click **Upload** (the arrow button) — wait for "Done uploading" ✅
5. Open **Serial Monitor at 115200 baud**

You should see:
```
Connecting to WiFi.....
✅ WiFi Connected! IP: 192.168.1.150
T=27.50°C  H=55.00%  Status=NORMAL
✅ Server response (200): OK - Saved: T=27.5 H=55 Status=NORMAL
```

🎉 If you see "Saved" — **data is going from ESP8266 → WiFi → PC → MySQL!**

---

## 🌐 Step 3: PHP Web Dashboard

Save as `C:\xampp\htdocs\weather\index.php`:

```php
<?php
$conn = new mysqli('localhost', 'root', '', 'Weather_db');
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);

$result = $conn->query("SELECT * FROM Weather_data ORDER BY timestamp DESC LIMIT 20");
$latest = $conn->query("SELECT * FROM Weather_data ORDER BY timestamp DESC LIMIT 1")->fetch_assoc();
$total  = $conn->query("SELECT COUNT(*) as c FROM Weather_data")->fetch_assoc()['c'];
?>
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>NYAGATARE Greenhouse — IoT Weather Station</title>
  <meta http-equiv="refresh" content="5">
  <style>
    body { font-family: Arial; background: #e6f4ea; margin: 0; padding: 30px; }
    .box { max-width: 950px; margin: auto; background: #fff; border-radius: 12px;
           box-shadow: 0 6px 20px rgba(0,0,0,0.1); overflow: hidden; }
    h1 { background: #2d6a4f; color: white; padding: 20px; margin: 0; text-align: center; }
    .sub { background: #1b4332; color: #d8f3dc; text-align: center; padding: 8px; font-size: 13px; }
    .now { display: flex; justify-content: space-around; padding: 30px; background: #f1f8f4; }
    .card { text-align: center; }
    .card .value { font-size: 42px; font-weight: bold; color: #2d6a4f; }
    .card .label { color: #666; font-size: 12px; text-transform: uppercase; margin-top: 5px; }
    table { width: 100%; border-collapse: collapse; }
    th { background: #2d6a4f; color: white; padding: 12px; text-align: left; }
    td { padding: 10px 12px; border-bottom: 1px solid #eee; }
    tr:hover { background: #f7faf8; }
    .badge { padding: 4px 10px; border-radius: 12px; color: white; font-size: 11px; font-weight: bold; }
    .HOT    { background: #c0392b; }
    .DRY    { background: #f39c12; }
    .NORMAL { background: #27ae60; }
  </style>
</head>
<body>
  <div class="box">
    <h1>🌿 NYAGATARE Greenhouse — IoT Weather Station</h1>
    <div class="sub">📡 Live data from ESP8266 · Auto-refresh every 5 seconds · <?= $total ?> readings logged</div>

    <?php if ($latest): ?>
    <div class="now">
      <div class="card">
        <div class="value">🌡 <?= $latest['Temperature'] ?>°C</div>
        <div class="label">Temperature</div>
      </div>
      <div class="card">
        <div class="value">💧 <?= $latest['Humidity'] ?>%</div>
        <div class="label">Humidity</div>
      </div>
      <div class="card">
        <div class="value"><span class="badge <?= $latest['Status'] ?>"><?= $latest['Status'] ?></span></div>
        <div class="label">Status · <?= $latest['timestamp'] ?></div>
      </div>
    </div>
    <?php endif; ?>

    <table>
      <tr><th>ID</th><th>Temp (°C)</th><th>Humidity (%)</th><th>Status</th><th>Timestamp</th></tr>
      <?php while($row = $result->fetch_assoc()): ?>
      <tr>
        <td><?= $row['Id'] ?></td>
        <td><?= $row['Temperature'] ?></td>
        <td><?= $row['Humidity'] ?></td>
        <td><span class="badge <?= $row['Status'] ?>"><?= $row['Status'] ?></span></td>
        <td><?= $row['timestamp'] ?></td>
      </tr>
      <?php endwhile; ?>
    </table>
  </div>
</body>
</html>
```

View it at: **`http://localhost/weather/`** ✅

---

## 🚀 Step 4: Run the System

### Full startup checklist:

1. ✅ XAMPP Control Panel → **Apache + MySQL running**
2. ✅ Database `Weather_db` exists with `Weather_data` table
3. ✅ Files `insert.php` and `index.php` saved in `C:\xampp\htdocs\weather\`
4. ✅ Windows Firewall allows Apache
5. ✅ ESP8266 plugged in & code uploaded
6. ✅ ESP8266 and PC on **same WiFi network**
7. ✅ Open browser: **`http://localhost/weather/`**

### Test the live system

- Breathe on the DHT11 → humidity rises → dashboard updates within 5 seconds
- Hold a warm cup of water near it → temperature rises → 🔴 Red LED + HOT status
- ESP8266 Serial Monitor shows "Server response (200): OK" each time

---

## ✅ Expected Results

### ESP8266 Serial Monitor (115200 baud)
```
Connecting to WiFi.....
✅ WiFi Connected! IP: 192.168.1.150
T=26.50°C  H=58.00%  Status=NORMAL
✅ Server response (200): OK - Saved: T=26.5 H=58 Status=NORMAL
T=27.10°C  H=55.30%  Status=NORMAL
✅ Server response (200): OK - Saved: T=27.1 H=55.3 Status=NORMAL
T=31.40°C  H=50.10%  Status=HOT
✅ Server response (200): OK - Saved: T=31.4 H=50.1 Status=HOT
```

### Web Dashboard

You'll see:
- Top: big "🌡 27.10°C" and "💧 55.30%"
- Status badge: 🟢 NORMAL / 🔴 HOT / 🟡 DRY
- Table below with last 20 readings, newest at top
- Auto-refreshes every 5 seconds 🎉

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `WiFi.h: No such file` | Selected wrong board — pick **NodeMCU 1.0**, not Arduino Uno |
| Stuck on "Connecting to WiFi..." | Wrong SSID/password, or 5GHz network (ESP8266 only does 2.4GHz) |
| `HTTP error: connection refused` | Wrong IP address, or Apache firewall blocking |
| `HTTP error: -1` | PC's IP changed (DHCP). Run `ipconfig` again, update code |
| Server response 404 | URL wrong, check `insert.php` path |
| Server response 500 | MySQL not running, or database/table missing |
| `Failed to read DHT11` | Wiring issue, or sensor on wrong pin |
| Dashboard shows 0 records | ESP8266 not sending — check Serial Monitor |
| ESP8266 won't upload | Press & hold FLASH button on board while uploading |
| Both devices on same WiFi but no connection | Some routers block "AP isolation" — check router settings |

### Quick connectivity test

From your **phone** on the same WiFi, open browser:
```
http://192.168.1.105/weather/
```
(Use YOUR PC's IP)

If this works on phone → ESP8266 will work too. ✅  
If not → firewall is blocking, or wrong IP.

---

## 🎤 Presentation Q&A

**Q1: Name your product and key steps**
> "IoT Greenhouse Weather Station for NYAGATARE Farms using ESP8266. Steps: identified components (ESP8266, DHT11, LEDs), wired the breadboard, installed ESP8266 board package and DHT library in Arduino IDE, created MySQL database `Weather_db`, built a PHP API endpoint (`insert.php`) to receive data, programmed the ESP8266 to read DHT11 and send data over WiFi via HTTP POST, developed a PHP dashboard to display live readings, and tested the full wireless flow end-to-end."

**Q2: Use/function**
> "This wireless IoT system monitors greenhouse climate in real-time without any cables to the PC. The ESP8266 is mounted inside the greenhouse, reads temperature and humidity from the DHT11 every 5 seconds, and pushes the data over WiFi to a web server running on the farm's PC. Workers see live conditions on a dashboard and get color-coded LED alerts on the device itself. This helps prevent crop damage from heat or low humidity."

**Q3: Challenges**
> "1) Configuring the ESP8266 board package in Arduino IDE — needed to add a custom URL. 2) Finding my PC's IP address and making sure Windows Firewall allowed incoming connections. 3) DHT11 returned `nan` initially because I read it too fast at startup. 4) ESP8266 only supports 2.4GHz WiFi, but my home WiFi was 5GHz — I had to use a different network."

**Q4: How I solved them**
> "Added the ESP8266 community URL to Arduino preferences and installed the board package. Used `ipconfig` in Windows to find my PC's IP, then added an inbound firewall rule for Apache. Added a `delay(1000)` after `dht.begin()` and checked for `isnan()` before sending. Switched to a 2.4GHz network or used my phone's hotspot."

---

## 📁 Project File Structure

```
On your PC:
C:\xampp\htdocs\weather\
├── insert.php          # Receives data from ESP8266
└── index.php           # Dashboard for browser

In Arduino IDE:
weather_esp8266.ino     # ESP8266 firmware
```

---

## 🎯 Why This Project Is Stronger Than the Wired Version

| Feature | USB Bridge (Old) | ESP8266 WiFi (This) |
|---------|------------------|---------------------|
| Cable required | Yes (USB) | No (wireless) |
| Python script | Yes | **Not needed** ✅ |
| Distance limit | ~2m USB | Anywhere on WiFi |
| Real-world IoT | Hobbyist | **Production-grade** |
| Multiple sensors | Hard | Easy (each gets WiFi) |

This is the kind of project that wins exam grades — **fewer moving parts, more impressive demo**. 🏆

---

## 🎓 Project Info

**Trade:** Networking and Internet Technologies  
**RQF Level:** 5  
**Stack:** ESP8266 · DHT11 · WiFi · PHP · MySQL  
**Architecture:** Direct device-to-server over HTTP

**Candidate:** ___________________  
**School:** ___________________  
**Date:** ___________________

---

**🌐 Welcome to real IoT — your sensor talks to the internet directly! 🚀**