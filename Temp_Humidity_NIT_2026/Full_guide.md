# 🌦️ Smart Weather Monitoring System (DHT11)

> **Scenario:** Build an IoT weather station that monitors temperature and humidity in real-time, logs data to a MySQL database, and displays it on a live web dashboard.

A simple but complete IoT project for **NYAGATARE Greenhouse Farms Ltd** — a tomato greenhouse that needs to monitor indoor climate to keep crops healthy. Too hot? Too humid? The system warns farmers instantly with color-coded alerts and keeps a full history.

---

## 📋 Table of Contents

1. [Project Scenario](#-project-scenario)
2. [How It Works](#-how-it-works)
3. [Materials Needed](#-materials-needed)
4. [Wiring Diagram](#-wiring-diagram)
5. [Software Setup](#-software-setup)
6. [Database Setup](#-database-setup)
7. [Arduino Code (DHT11)](#-arduino-code-dht11)
8. [Python Bridge](#-python-bridge)
9. [PHP Web Dashboard](#-php-web-dashboard)
10. [Run the System](#-run-the-system)
11. [Expected Results](#-expected-results)
12. [Troubleshooting](#-troubleshooting)
13. [Presentation Q&A](#-presentation-qa)

---

## 🎯 Project Scenario

**Client:** NYAGATARE Greenhouse Farms Ltd  
**Problem:** Tomatoes get damaged when temperature goes above 30°C or humidity drops below 40%. Farmers need real-time alerts.  
**Solution:** A DHT11 sensor reads climate data every few seconds. LEDs flash warnings when conditions are dangerous. Every reading is logged to a database and shown on a web dashboard.

### Alert Logic

| Condition | LED | Meaning |
|-----------|-----|---------|
| Temp > 30°C | 🔴 Red | TOO HOT — open vents! |
| Humidity < 40% | 🟡 Yellow | TOO DRY — turn on misters! |
| All normal | 🟢 Green | Climate OK |

---

## 🏗 How It Works

```
DHT11 Sensor → Arduino Uno → Python Bridge (USB) → MySQL Database → PHP Web Dashboard
```

DHT11 is a tiny sensor that gives you both **temperature (°C)** and **humidity (%)** through a single wire. Arduino reads it, decides which LED to light, sends the data to your PC via USB, Python saves it to MySQL, and PHP shows it in the browser.

---

## 📦 Materials Needed

### Hardware

| # | Component | Qty |
|:-:|-----------|:---:|
| 1 | Arduino Uno + USB cable | 1 |
| 2 | DHT11 sensor (3 or 4 pins) | 1 |
| 3 | Red LED | 1 |
| 4 | Yellow LED | 1 |
| 5 | Green LED | 1 |
| 6 | 220Ω resistors | 3 |
| 7 | 10kΩ resistor (for DHT11 pull-up) | 1 |
| 8 | Breadboard | 1 |
| 9 | Jumper wires | ~8 |

### Software

- Arduino IDE
- XAMPP (Apache + MySQL + PHP)
- Python 3.x with `pyserial` and `mysql-connector-python`
- **DHT sensor library** (install in Arduino IDE — see Step 1 below)

---

## 🔌 Wiring Diagram

### DHT11 to Arduino

| DHT11 Pin | Arduino |
|-----------|---------|
| VCC (+) | 5V |
| DATA | Pin 7 *(plus 10kΩ resistor between DATA and 5V)* |
| GND (−) | GND |

> 💡 If your DHT11 is on a small **breakout board** (3 pins), the 10kΩ resistor is already built in. Skip it.

### LEDs to Arduino

| LED | Anode (long leg) | Cathode (short leg) |
|-----|------------------|---------------------|
| 🔴 Red (Hot) | 220Ω → Pin 2 | GND |
| 🟡 Yellow (Dry) | 220Ω → Pin 3 | GND |
| 🟢 Green (OK) | 220Ω → Pin 4 | GND |

---

## 💻 Software Setup

### Step 1: Install DHT Library in Arduino IDE

1. Open Arduino IDE
2. Go to **Sketch → Include Library → Manage Libraries...**
3. Search **"DHT sensor library by Adafruit"** → click **Install**
4. If asked to install dependencies (Adafruit Unified Sensor) → click **Install all** ✅

### Step 2: Start XAMPP

Open XAMPP Control Panel → click **Start** for both **Apache** and **MySQL**.

### Step 3: Install Python Libraries

```powershell
pip install pyserial mysql-connector-python
```

(Or `pip install pyserial mysql-connector-python --break-system-packages` if needed.)

---

## 🗄 Database Setup

Open `http://localhost/phpmyadmin` (or `http://localhost:8080/phpmyadmin` if you use port 8080).

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

## 🤖 Arduino Code (DHT11)

Save as `weather_station.ino`:

```cpp
// ============================================================
// NYAGATARE Greenhouse - Weather Monitoring System
// ============================================================
#include <DHT.h>

#define DHT_PIN 7
#define DHT_TYPE DHT11
#define LED_RED    2   // Too Hot
#define LED_YELLOW 3   // Too Dry
#define LED_GREEN  4   // Normal

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_YELLOW, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  Serial.begin(9600);
  dht.begin();
  delay(2000);
  Serial.println("Weather Station Ready");
}

void loop() {
  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();

  // Check if reading failed
  if (isnan(temp) || isnan(hum)) {
    Serial.println("Failed to read DHT11");
    delay(2000);
    return;
  }

  // Reset LEDs
  digitalWrite(LED_RED, LOW);
  digitalWrite(LED_YELLOW, LOW);
  digitalWrite(LED_GREEN, LOW);

  String status;

  if (temp > 30) {
    digitalWrite(LED_RED, HIGH);
    status = "HOT";
  }
  else if (hum < 40) {
    digitalWrite(LED_YELLOW, HIGH);
    status = "DRY";
  }
  else {
    digitalWrite(LED_GREEN, HIGH);
    status = "NORMAL";
  }

  // Send data over Serial: TEMP,HUM,STATUS
  Serial.print("DATA,");
  Serial.print(temp);
  Serial.print(",");
  Serial.print(hum);
  Serial.print(",");
  Serial.println(status);

  delay(3000);  // read every 3 seconds
}
```

### Upload Steps

1. Plug Arduino in
2. **Tools → Board → Arduino Uno**
3. **Tools → Port → COMx** (check Device Manager)
4. Click **Upload** ✅
5. Open Serial Monitor at **9600 baud** → you should see lines like:
```
   DATA,26.50,55.00,NORMAL
```

---

## 🐍 Python Bridge

Save as `weather_to_db.py`:

```python
import serial
import mysql.connector
import time

# Change COM port to match yours
arduino = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Weather_db'
)
cursor = db.cursor()

print("Weather Logger Active... (Ctrl+C to stop)")

while True:
    try:
        line = arduino.readline().decode('utf-8').strip()
        if line.startswith("DATA,"):
            parts = line.split(",")
            if len(parts) == 4:
                _, temp, hum, status = parts
                sql = "INSERT INTO Weather_data (Temperature, Humidity, Status) VALUES (%s, %s, %s)"
                cursor.execute(sql, (float(temp), float(hum), status))
                db.commit()
                print(f"✅ T={temp}°C  H={hum}%  Status={status}")
    except KeyboardInterrupt:
        break
    except Exception as e:
        print("❌", e)
        time.sleep(1)

arduino.close()
db.close()
```

Run with:
```powershell
python weather_to_db.py
```

> ⚠️ **Close Arduino Serial Monitor before running this!**

---

## 🌐 PHP Web Dashboard

Save as `C:\xampp\htdocs\weather\index.php`:

```php
<?php
$conn = new mysqli('localhost', 'root', '', 'Weather_db');
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);

$result = $conn->query("SELECT * FROM Weather_data ORDER BY timestamp DESC LIMIT 20");
$latest = $conn->query("SELECT * FROM Weather_data ORDER BY timestamp DESC LIMIT 1")->fetch_assoc();
?>
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>NYAGATARE Greenhouse Weather Station</title>
  <meta http-equiv="refresh" content="5">
  <style>
    body { font-family: Arial; background: #e6f4ea; margin: 0; padding: 30px; }
    .box { max-width: 900px; margin: auto; background: #fff; border-radius: 10px;
           box-shadow: 0 4px 15px rgba(0,0,0,0.1); overflow: hidden; }
    h1 { background: #2d6a4f; color: #fff; padding: 20px; margin: 0; text-align: center; }
    .now { display: flex; justify-content: space-around; padding: 25px; background: #f1f8f4; }
    .card { text-align: center; }
    .card .value { font-size: 36px; font-weight: bold; color: #2d6a4f; }
    .card .label { color: #666; font-size: 13px; text-transform: uppercase; }
    table { width: 100%; border-collapse: collapse; }
    th { background: #2d6a4f; color: white; padding: 12px; }
    td { padding: 10px; border-bottom: 1px solid #eee; }
    .badge { padding: 4px 10px; border-radius: 12px; color: white; font-size: 12px; }
    .HOT    { background: #c0392b; }
    .DRY    { background: #f39c12; }
    .NORMAL { background: #27ae60; }
  </style>
</head>
<body>
  <div class="box">
    <h1>🌿 NYAGATARE Greenhouse — Weather Station</h1>

    <?php if ($latest): ?>
    <div class="now">
      <div class="card">
        <div class="value"><?= $latest['Temperature'] ?>°C</div>
        <div class="label">Temperature</div>
      </div>
      <div class="card">
        <div class="value"><?= $latest['Humidity'] ?>%</div>
        <div class="label">Humidity</div>
      </div>
      <div class="card">
        <div class="value"><span class="badge <?= $latest['Status'] ?>"><?= $latest['Status'] ?></span></div>
        <div class="label">Current Status</div>
      </div>
    </div>
    <?php endif; ?>

    <table>
      <tr><th>ID</th><th>Temp (°C)</th><th>Humidity (%)</th><th>Status</th><th>Time</th></tr>
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

That's it. **Super simple PHP file** — connects, queries, displays. No fancy stuff.

---

## 🚀 Run the System

Run these in order:

1. **XAMPP** → Apache ✅ + MySQL ✅
2. **Arduino IDE** → Upload `weather_station.ino` → **Close Serial Monitor**
3. **PowerShell:**
```powershell
   python weather_to_db.py
```
4. **Browser:** `http://localhost/weather/` (or `http://localhost:8080/weather/`)

Wave the sensor near a warm cup or breathe on it — temperature/humidity should change, LEDs should react, dashboard updates every 5 seconds! 🎉

---

## ✅ Expected Results

### Serial Monitor / Python Output
```
✅ T=26.50°C  H=55.00%  Status=NORMAL
✅ T=27.10°C  H=53.20%  Status=NORMAL
✅ T=31.40°C  H=50.10%  Status=HOT
✅ T=29.80°C  H=38.50%  Status=DRY
```

### Web Dashboard
- Big numbers showing current temp & humidity
- Status badge: 🟢 NORMAL / 🔴 HOT / 🟡 DRY
- Table with last 20 readings, newest first
- Auto-refreshes every 5 seconds

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `Failed to read DHT11` | Check wiring; add 10kΩ pull-up resistor between DATA and 5V |
| All readings `nan` | DHT11 needs 2-second startup delay (already in code) |
| `DHT.h: No such file` | Install DHT library via Arduino IDE Library Manager |
| `Access denied COM5` | Close Arduino Serial Monitor before running Python |
| LEDs don't react | Check polarity (long leg = positive) |
| Dashboard 404 | Verify file is at `C:\xampp\htdocs\weather\index.php` |
| Page shows raw PHP | Apache not running, or saved as `.html` |
| Temperature jumps weirdly | DHT11 is slow & noisy by design — that's normal |

---

## 🎤 Presentation Q&A

**Q1: Name your product and key steps**
> "Greenhouse Weather Monitoring System for NYAGATARE Farms. Steps: identified components (Arduino, DHT11, LEDs), designed circuit, wired the breadboard, programmed Arduino with DHT library, created `Weather_db` database, built Python bridge to log data, developed PHP dashboard, tested end-to-end."

**Q2: Use/function**
> "Helps tomato farmers monitor greenhouse climate in real-time. Detects when temperature exceeds 30°C or humidity drops below 40% — both dangerous for tomatoes. Visual LED alerts let workers act immediately. The web dashboard provides historical data for analyzing climate patterns and making informed decisions."

**Q3: Challenges**
> "1) Initially the DHT11 returned `nan` because I tried to read it too fast — fixed by adding a 2-second startup delay. 2) The COM port was busy because I forgot to close Serial Monitor. 3) Setting up the pull-up resistor on DATA pin."

**Q4: How I solved them**
> "Added `delay(2000)` after `dht.begin()` to give the sensor time to initialize. Always close Serial Monitor before running Python. For the pull-up, connected a 10kΩ resistor between DATA and VCC for clean signal."

---

## 📁 File Structure

```
weather_project/
├── weather_station.ino        # Arduino code
├── weather_to_db.py           # Python bridge
└── README.md                  # This file

C:\xampp\htdocs\weather\
└── index.php                  # Dashboard
```

---

## 🎓 Project Info

**Trade:** Networking and Internet Technologies  
**RQF Level:** 5  
**Sensor:** DHT11 (Temperature & Humidity)  
**Stack:** Arduino + Python + MySQL + PHP

**Candidate:** ___________________  
**School:** ___________________  
**Date:** ___________________

---

**🌱 Keep it simple, test each step, and you'll nail it!**