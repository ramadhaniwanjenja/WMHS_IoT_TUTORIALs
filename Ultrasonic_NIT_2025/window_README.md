# 🏭 KILIKU Cement - Motion Sensing & Detection System

> **IoT-based proximity security system for KILIKU Cement Limited** — Bugarama, Rusizi District, Western Province, Rwanda.

An Arduino-powered smart security system that detects approaching objects using an ultrasonic sensor, triggers color-coded LED warnings based on distance, logs every event to a MySQL database, and displays them on a live PHP web dashboard.

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [System Architecture](#-system-architecture)
3. [How It Works](#-how-it-works)
4. [Materials & Components](#-materials--components)
5. [Wiring Diagram](#-wiring-diagram)
6. [Software Requirements](#-software-requirements)
7. [Installation Guide (Windows)](#-installation-guide-windows)
8. [Proteus Circuit Design](#-proteus-circuit-design)
9. [Database Setup](#-database-setup)
10. [Arduino Code](#-arduino-code)
11. [Python Bridge Script](#-python-bridge-script)
12. [PHP Web Interface](#-php-web-interface)
13. [Running the System](#-running-the-system)
14. [Expected Results](#-expected-results)
15. [Troubleshooting](#-troubleshooting)
16. [Presentation Q&A](#-presentation-qa)
17. [Project Checklist](#-project-checklist)
18. [Credits](#-credits)

---

## 🎯 Project Overview

**Client:** KILIKU Cement Limited  
**Problem:** Weak physical security, product theft at company gate  
**Solution:** IoT proximity detection system with logging & visualization  
**Duration:** 6 hours (National Practical Exam)

### Detection Logic

| Distance Range | LED Color | On Delay | Off Delay | Alert Level |
|:--------------:|:---------:|:--------:|:---------:|:-----------:|
| Within 30 cm   | 🔴 Red    | 200 ms   | 150 ms    | Warning     |
| Within 20 cm   | 🟢 Green  | 250 ms   | 350 ms    | Closer      |
| Within 10 cm   | 🔵 Blue   | 300 ms   | 450 ms    | **Intruder!** |

---

## 🏗 System Architecture

```
┌─────────────┐   ┌──────────────┐   ┌─────────────┐   ┌──────────┐   ┌────────────┐
│   HC-SR04   │──▶│  Arduino Uno │──▶│ Python      │──▶│  MySQL   │──▶│ PHP Web UI │
│   Sensor    │   │ (with LEDs)  │   │ Bridge (USB)│   │ Database │   │ (Browser)  │
└─────────────┘   └──────────────┘   └─────────────┘   └──────────┘   └────────────┘
```

**Data Flow:**
1. Sensor detects distance → Arduino processes it
2. Arduino blinks the right LED and prints event to Serial
3. Python script reads Serial → saves to MySQL
4. PHP page queries MySQL → displays live log in browser

---

## 🔧 How It Works

### The Ultrasonic Sensor (HC-SR04)

Like a bat, this sensor sends sound waves and measures echo time:

- **TRIG pin** sends a 10-microsecond ultrasonic pulse
- **ECHO pin** receives the bounce back
- Arduino calculates: `distance (cm) = time × 0.034 / 2`

### Why divide by 2? 

Because the sound travels to the object **and** bounces back — we want the one-way distance.

### Speed of Sound Constant: 0.034

That's 340 meters/second converted to centimeters per microsecond.

---

## 📦 Materials & Components

### 🛠 Hardware

| # | Component | Quantity | Notes |
|:-:|-----------|:--------:|-------|
| 1 | Arduino Uno R3 | 1 | With USB Type-B cable |
| 2 | HC-SR04 Ultrasonic Sensor | 1 | 4-pin version |
| 3 | LED - Red | 1 | 5mm standard |
| 4 | LED - Green | 1 | 5mm standard |
| 5 | LED - Blue | 1 | 5mm standard |
| 6 | Resistor 220Ω | 3 | Red-Red-Brown-Gold stripes |
| 7 | Breadboard | 1 | Half-size or full-size |
| 8 | Jumper wires (Male-to-Male) | 10 | Various colors |
| 9 | Windows PC/Laptop | 1 | Windows 10/11 |

### 💻 Software (all free)

| Software | Purpose | Download |
|----------|---------|----------|
| Arduino IDE | Write/upload Arduino code | https://www.arduino.cc/en/software |
| Proteus 8 Professional | Circuit diagram design | From your school or licensed copy |
| XAMPP | Apache + MySQL + PHP bundle | https://www.apachefriends.org/ |
| Python 3.11+ | Runs the data bridge | https://www.python.org/downloads/ |
| VS Code | Code editor (optional) | https://code.visualstudio.com/ |

---

## 🔌 Wiring Diagram

### Component → Arduino Connection Table

| Component       | Pin/Leg            | Connects To                  |
|-----------------|--------------------|------------------------------|
| HC-SR04         | VCC                | Arduino **5V**               |
| HC-SR04         | GND                | Arduino **GND**              |
| HC-SR04         | TRIG               | Arduino **Pin 9**            |
| HC-SR04         | ECHO               | Arduino **Pin 10**           |
| Red LED         | Anode (long leg)   | 220Ω → Arduino **Pin 2**     |
| Red LED         | Cathode (short leg)| Arduino **GND**              |
| Green LED       | Anode (long leg)   | 220Ω → Arduino **Pin 3**     |
| Green LED       | Cathode (short leg)| Arduino **GND**              |
| Blue LED        | Anode (long leg)   | 220Ω → Arduino **Pin 4**     |
| Blue LED        | Cathode (short leg)| Arduino **GND**              |

> ⚠️ **LED Polarity:** Long leg = positive (+). Short leg = negative (−). If the LED doesn't light, flip it.

### Breadboard Layout Guide

```
Arduino 5V  ──────────▶  Red rail (+)
Arduino GND ──────────▶  Blue rail (−)

Red rail    ──────────▶  HC-SR04 VCC
Blue rail   ──────────▶  HC-SR04 GND + All LED cathodes

Pin 9  ───▶ HC-SR04 TRIG
Pin 10 ───▶ HC-SR04 ECHO
Pin 2  ───▶ 220Ω ───▶ Red LED anode   ───▶ Red LED cathode   ───▶ GND rail
Pin 3  ───▶ 220Ω ───▶ Green LED anode ───▶ Green LED cathode ───▶ GND rail
Pin 4  ───▶ 220Ω ───▶ Blue LED anode  ───▶ Blue LED cathode  ───▶ GND rail
```

---

## 💻 Software Requirements

- **OS:** Windows 10 or Windows 11 (64-bit)
- **RAM:** 4 GB minimum
- **Disk:** 2 GB free
- **USB Port:** At least one available

---

## 📥 Installation Guide (Windows)

### Step 1: Install Arduino IDE

1. Go to https://www.arduino.cc/en/software
2. Download **Windows Installer** (.exe)
3. Run the installer, click **I Agree** → **Install**
4. Accept **all driver installation prompts** (very important — installs USB drivers!)
5. Launch Arduino IDE from Start menu

### Step 2: Install XAMPP (Apache + MySQL + PHP)

1. Go to https://www.apachefriends.org/
2. Download **XAMPP for Windows** (PHP 8.x version)
3. Run installer as **Administrator**
4. Install to default location: `C:\xampp`
5. Select components: **Apache, MySQL, PHP, phpMyAdmin** (uncheck the rest)
6. Complete installation
7. Launch **XAMPP Control Panel** from Start menu

#### Start XAMPP Services

In the XAMPP Control Panel:

1. Click **Start** next to **Apache** → should turn green
2. Click **Start** next to **MySQL** → should turn green

> 💡 If Apache fails, it usually means Skype or IIS is using port 80. Close Skype or in XAMPP click **Config → httpd.conf** and change `Listen 80` to `Listen 8080`.

#### Verify XAMPP Works

- Open browser → `http://localhost` → XAMPP welcome page should appear ✅
- Open browser → `http://localhost/phpmyadmin` → phpMyAdmin interface should appear ✅

### Step 3: Install Python

1. Go to https://www.python.org/downloads/
2. Download **Python 3.11+** for Windows
3. Run installer → **✅ CHECK "Add Python to PATH"** (super important!)
4. Click **Install Now**
5. Verify installation — open Command Prompt (`Win + R` → type `cmd`):

```cmd
python --version
```

Should show `Python 3.11.x` or similar.

### Step 4: Install Python Libraries

In the same Command Prompt:

```cmd
pip install pyserial mysql-connector-python
```

Wait for both to download and install.

### Step 5: Install Proteus

1. Install Proteus 8 Professional from your school's copy
2. Open it → **File → New Project** → save as `KILIKU_motion.pdsprj`

### Step 6: Find Arduino's COM Port

1. Plug Arduino into USB
2. Open **Device Manager** (`Win + X` → Device Manager)
3. Expand **Ports (COM & LPT)**
4. Look for **Arduino Uno (COMx)** — note the number (e.g., COM3, COM4, COM5)

> 💡 If it says "Unknown Device", download the CH340 driver from http://www.wch-ic.com/downloads/CH341SER_EXE.html (for Arduino clones).

---

## 🎨 Proteus Circuit Design

### Steps

1. Open **Proteus 8 Professional**
2. **File → New Project** → Name it `KILIKU_motion` → Save in `C:\Users\YourName\Documents\`
3. Click the **"P" button** (Pick from Libraries) on the left toolbar
4. Search and add these components:
   - `ARDUINO UNO R3`
   - `SRF04` (simulates HC-SR04)
   - `LED-RED`, `LED-GREEN`, `LED-BLUE`
   - `RES` × 3 (double-click each → set value to `220`)
5. Click **Terminals Mode** (left toolbar) → add **GROUND** and **POWER** terminals
6. Connect everything according to the wiring table above
7. **File → Export Graphics → Export PDF** → save as `wiring_diagram.pdf`
8. Print or screenshot — **assessors will verify this!**

---

## 🗄 Database Setup

### Method 1: Using phpMyAdmin (Recommended)

1. Open browser → `http://localhost/phpmyadmin`
2. Click **SQL** tab at the top
3. Paste and click **Go**:

```sql
CREATE DATABASE Motion_db;

USE Motion_db;

CREATE TABLE Motion_data (
  Id INT AUTO_INCREMENT PRIMARY KEY,
  Motion_Detected VARCHAR(150) NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Method 2: Using MySQL Command Line

Open Command Prompt and navigate to XAMPP's MySQL bin folder:

```cmd
cd C:\xampp\mysql\bin
mysql -u root
```

Then paste the same SQL commands above.

### Verify Database

- Refresh phpMyAdmin sidebar → `Motion_db` should appear
- Click it → `Motion_data` table visible → click **Structure** to see columns

#### Expected Table Structure

| Column           | Type         | Extra              |
|:----------------:|:------------:|:------------------:|
| Id               | INT          | AUTO_INCREMENT, PK |
| Motion_Detected  | VARCHAR(150) | NOT NULL           |
| timestamp        | TIMESTAMP    | DEFAULT NOW()      |

---

## 🤖 Arduino Code

### Save as `KILIKU_motion.ino`

```cpp
// ============================================================
// KILIKU Cement - Motion Sensing & Detection System
// National Practical Exam 2024-2025
// Networking and Internet Technologies - RQF Level 5
// ============================================================

#define TRIG_PIN 9
#define ECHO_PIN 10
#define LED_RED   2   // Red   -> within 30 cm
#define LED_GREEN 3   // Green -> within 20 cm
#define LED_BLUE  4   // Blue  -> within 10 cm

long duration;
int distance;

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);
  Serial.begin(9600);
  Serial.println("KILIKU Motion System Ready");
}

void loop() {
  // Send 10-microsecond ultrasonic pulse
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Measure echo time
  duration = pulseIn(ECHO_PIN, HIGH);

  // Convert to distance in cm
  distance = duration * 0.034 / 2;

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // Reset all LEDs before deciding
  digitalWrite(LED_RED, LOW);
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_BLUE, LOW);

  // Closest range first so the right LED wins
  if (distance > 0 && distance <= 10) {
    digitalWrite(LED_BLUE, HIGH);
    delay(300);
    digitalWrite(LED_BLUE, LOW);
    delay(450);
    Serial.println("Motion detected within 10cm");
  }
  else if (distance <= 20) {
    digitalWrite(LED_GREEN, HIGH);
    delay(250);
    digitalWrite(LED_GREEN, LOW);
    delay(350);
    Serial.println("Motion detected within 20cm");
  }
  else if (distance <= 30) {
    digitalWrite(LED_RED, HIGH);
    delay(200);
    digitalWrite(LED_RED, LOW);
    delay(150);
    Serial.println("Motion detected within 30cm");
  }
  else {
    delay(200);
  }
}
```

### Upload Instructions

1. Plug Arduino into USB
2. Open Arduino IDE
3. **File → New** → paste the code above
4. **File → Save As** → `KILIKU_motion.ino`
5. **Tools → Board → Arduino Uno**
6. **Tools → Port → COMx** (the one you found in Device Manager)
7. Click the **✓ Verify** button → should say "Done compiling"
8. Click the **→ Upload** button → should say "Done uploading"
9. **Tools → Serial Monitor** → set baud rate to **9600**
10. Wave your hand → you should see distance readings ✅

---

## 🐍 Python Bridge Script

### Create Project Folder

Open Command Prompt:

```cmd
mkdir C:\kiliku_project
cd C:\kiliku_project
```

### Save as `serial_to_db.py`

Create the file in Notepad or VS Code, paste this:

```python
# ============================================================
# KILIKU Cement - Serial to Database Bridge
# Reads Arduino output and stores events in MySQL
# ============================================================

import serial
import mysql.connector
import time

# ⚠️ Change 'COM3' to your Arduino's actual COM port!
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)   # Wait for Arduino to reset

# Connect to MySQL (default XAMPP: user=root, no password)
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',                # Leave empty for default XAMPP
    database='Motion_db'
)
cursor = db.cursor()

print("=" * 50)
print("KILIKU Motion Logger - ACTIVE")
print("Listening for motion events... (Press Ctrl+C to stop)")
print("=" * 50)

while True:
    try:
        line = arduino.readline().decode('utf-8').strip()
        if line and "Motion detected" in line:
            sql = "INSERT INTO Motion_data (Motion_Detected) VALUES (%s)"
            cursor.execute(sql, (line,))
            db.commit()
            print(f"✅ Saved: {line}")
    except KeyboardInterrupt:
        print("\nStopping...")
        break
    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(1)

arduino.close()
db.close()
print("Disconnected cleanly.")
```

### Run It

```cmd
cd C:\kiliku_project
python serial_to_db.py
```

> ⚠️ **CRITICAL:** Close Arduino IDE's Serial Monitor before running this! Only one program can use the COM port at a time.

---

## 🌐 PHP Web Interface

### Create File Location

XAMPP serves files from `C:\xampp\htdocs\`. Create a new folder:

1. Open File Explorer → go to `C:\xampp\htdocs\`
2. Create new folder named `motion`
3. Inside that folder, create a new file called `index.php`

### Save as `C:\xampp\htdocs\motion\index.php`

```php
<?php
// ============================================================
// KILIKU Cement - Motion Events Dashboard
// ============================================================

$conn = new mysqli('localhost', 'root', '', 'Motion_db');
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$result = $conn->query("SELECT * FROM Motion_data ORDER BY timestamp DESC");
$total = $result->num_rows;
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>KILIKU Cement - Motion Detection Dashboard</title>
  <meta http-equiv="refresh" content="5">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', Arial, sans-serif;
      background: linear-gradient(135deg, #1a4d2e 0%, #2d6a4f 100%);
      min-height: 100vh;
      padding: 30px;
      color: #333;
    }
    .container {
      max-width: 1100px;
      margin: 0 auto;
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.2);
      overflow: hidden;
    }
    .header {
      background: #1a4d2e;
      color: white;
      padding: 30px;
      text-align: center;
    }
    .header h1 { font-size: 28px; margin-bottom: 8px; }
    .header p { opacity: 0.9; font-size: 14px; }
    .stats {
      display: flex;
      justify-content: space-around;
      padding: 20px;
      background: #f8f9fa;
      border-bottom: 2px solid #e9ecef;
    }
    .stat-box {
      text-align: center;
      flex: 1;
    }
    .stat-box .number {
      font-size: 32px;
      font-weight: bold;
      color: #1a4d2e;
    }
    .stat-box .label {
      font-size: 12px;
      text-transform: uppercase;
      color: #666;
      margin-top: 4px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
    }
    th {
      background: #1a4d2e;
      color: white;
      padding: 14px;
      text-align: left;
      font-size: 13px;
      text-transform: uppercase;
    }
    td {
      padding: 12px 14px;
      border-bottom: 1px solid #eee;
    }
    tr:nth-child(even) { background: #fafbfc; }
    tr:hover { background: #eef7f1; }
    .badge {
      padding: 5px 10px;
      border-radius: 20px;
      color: white;
      font-size: 11px;
      font-weight: bold;
      letter-spacing: 0.5px;
    }
    .red   { background: #c0392b; }
    .green { background: #27ae60; }
    .blue  { background: #2980b9; }
    .footer {
      padding: 15px;
      text-align: center;
      background: #f8f9fa;
      color: #666;
      font-size: 12px;
    }
    .empty {
      padding: 40px;
      text-align: center;
      color: #999;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🏭 KILIKU Cement Ltd</h1>
      <p>Motion Detection & Security Dashboard</p>
    </div>

    <div class="stats">
      <div class="stat-box">
        <div class="number"><?= $total ?></div>
        <div class="label">Total Events</div>
      </div>
      <div class="stat-box">
        <div class="number">🟢</div>
        <div class="label">System Active</div>
      </div>
      <div class="stat-box">
        <div class="number">5s</div>
        <div class="label">Auto-Refresh</div>
      </div>
    </div>

    <?php if ($total > 0): ?>
    <table>
      <tr>
        <th>ID</th>
        <th>Event Description</th>
        <th>Zone</th>
        <th>Timestamp</th>
      </tr>
      <?php while($row = $result->fetch_assoc()):
          $zone = 'red';
          if (strpos($row['Motion_Detected'],'10cm')!==false) $zone='blue';
          elseif (strpos($row['Motion_Detected'],'20cm')!==false) $zone='green';
      ?>
      <tr>
        <td><?= $row['Id'] ?></td>
        <td><?= htmlspecialchars($row['Motion_Detected']) ?></td>
        <td><span class="badge <?= $zone ?>"><?= strtoupper($zone) ?> ZONE</span></td>
        <td><?= $row['timestamp'] ?></td>
      </tr>
      <?php endwhile; ?>
    </table>
    <?php else: ?>
      <div class="empty">
        <h3>No motion events yet</h3>
        <p>Wave your hand in front of the sensor to generate events.</p>
      </div>
    <?php endif; ?>

    <div class="footer">
      Page auto-refreshes every 5 seconds · Developed for KILIKU Cement Limited
    </div>
  </div>
</body>
</html>
```

### View It

Open browser → `http://localhost/motion/` → Dashboard should appear. ✅

---

## 🚀 Running the System

### Full Startup Sequence

Every time you want to run the system, do these in order:

#### Terminal 1: Start XAMPP

1. Open **XAMPP Control Panel**
2. Click **Start** next to **Apache** (turns green)
3. Click **Start** next to **MySQL** (turns green)

#### Terminal 2: Arduino

1. Plug Arduino into USB
2. Open Arduino IDE
3. Verify **Tools → Port** is correct
4. If code isn't uploaded yet, click **Upload**
5. **Close Serial Monitor** (if open)

#### Terminal 3: Python Bridge

```cmd
cd C:\kiliku_project
python serial_to_db.py
```

Leave this running.

#### Browser: Web Dashboard

Open Firefox/Chrome → `http://localhost/motion/`

#### Test It

Wave your hand slowly toward the sensor — you should see:

1. LEDs blinking based on distance ✅
2. Python terminal printing `✅ Saved: Motion detected within XXcm` ✅
3. Web dashboard auto-refreshing with new rows ✅

---

## ✅ Expected Results

### Arduino Serial Monitor

```
KILIKU Motion System Ready
Distance: 156 cm
Distance: 78 cm
Distance: 28 cm
Motion detected within 30cm
Distance: 15 cm
Motion detected within 20cm
Distance: 7 cm
Motion detected within 10cm
```

### LED Behavior

| Hand Distance | LED Light | Blink Pattern |
|:-------------:|:---------:|:-------------:|
| > 30 cm       | None      | —             |
| 21–30 cm      | 🔴 Red    | Fast blink    |
| 11–20 cm      | 🟢 Green  | Medium blink  |
| 0–10 cm       | 🔵 Blue   | Slow blink    |

### Python Terminal

```
==================================================
KILIKU Motion Logger - ACTIVE
Listening for motion events... (Press Ctrl+C to stop)
==================================================
✅ Saved: Motion detected within 30cm
✅ Saved: Motion detected within 20cm
✅ Saved: Motion detected within 10cm
✅ Saved: Motion detected within 10cm
```

### phpMyAdmin

In `Motion_db` → `Motion_data`, you should see rows like:

| Id | Motion_Detected              | timestamp           |
|:--:|------------------------------|---------------------|
| 1  | Motion detected within 30cm  | 2025-05-28 10:15:23 |
| 2  | Motion detected within 20cm  | 2025-05-28 10:15:25 |
| 3  | Motion detected within 10cm  | 2025-05-28 10:15:28 |

### Web Dashboard

A beautiful green-themed dashboard with:
- 🏭 KILIKU Cement header
- Total event counter
- Color-coded zone badges (RED / GREEN / BLUE)
- Auto-refreshing table with timestamps

---

## 🐛 Troubleshooting

### Arduino / Hardware Issues

| Problem | Solution |
|---------|----------|
| Arduino IDE shows no COM port | Install CH340 driver: http://www.wch-ic.com/downloads/CH341SER_EXE.html |
| "avrdude: stk500_getsync()" error | Wrong board or port selected. Check Tools menu |
| LEDs don't light up | Flip the LED — long leg (+) must go to the Arduino pin via resistor |
| Distance always shows 0 | Check TRIG/ECHO wiring — they might be swapped |
| Distance shows huge numbers (2000+) | ECHO wire loose or sensor damaged |
| Only one LED works | Other LEDs might be burnt — replace them |

### XAMPP Issues

| Problem | Solution |
|---------|----------|
| Apache won't start | Port 80 is busy (Skype/IIS). Change to 8080 in httpd.conf |
| MySQL won't start | Delete `C:\xampp\mysql\data\ibdata1` (⚠️ loses all databases) and restart |
| phpMyAdmin shows "Access denied" | In XAMPP Control Panel, Shell → `mysql -u root -p` → set password |
| Port 3306 already in use | Another MySQL instance running. Open Task Manager, end `mysqld.exe` |

### Python Issues

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'serial'` | Run: `pip install pyserial` |
| `ModuleNotFoundError: No module named 'mysql'` | Run: `pip install mysql-connector-python` |
| `SerialException: could not open port` | COM port busy. Close Arduino Serial Monitor |
| `Access denied for user 'root'@'localhost'` | Check password in Python script matches MySQL |
| `Can't connect to MySQL server` | MySQL not started in XAMPP |
| Python not recognized | Reinstall Python with **"Add to PATH"** checked |

### PHP / Web Issues

| Problem | Solution |
|---------|----------|
| Browser shows raw PHP code | Apache not running, or saved file with wrong extension |
| "Connection failed" error | MySQL not started or wrong password |
| 404 Not Found at `/motion/` | File must be in `C:\xampp\htdocs\motion\index.php` |
| Page works but no data shows | Python script isn't running or Arduino not connected |

---

## 🎤 Presentation Q&A

> 💡 **35% of your grade is presentation!** Practice these answers out loud.

### Q1: "Name your product and announce the key steps of the process"

> **"My project is the Proximity-Triggered LED Security System with Database Logging, built for KILIKU Cement Limited. The key steps I followed were:**
> 1. Identified necessary components — Arduino Uno, HC-SR04 ultrasonic sensor, three LEDs, resistors, and breadboard
> 2. Designed the circuit diagram in Proteus
> 3. Mounted and connected all components on the breadboard
> 4. Wrote Arduino code to measure distance and control LEDs based on proximity zones
> 5. Created a MySQL database called `Motion_db` with a `Motion_data` table
> 6. Developed a Python bridge script to capture Arduino output and insert it into MySQL
> 7. Built a PHP web dashboard to visualize the logged events
> 8. Verified end-to-end functionality from sensor detection to web display"

### Q2: "What is the use / function / importance of your project?"

> **"This system enhances physical security at the KILIKU Cement gate in Bugarama.** The ultrasonic sensor detects when someone or something approaches the premises. Three color-coded LEDs provide instant visual warnings at 30 cm (red), 20 cm (green), and 10 cm (blue) — giving security personnel real-time proximity alerts. Every detection event is logged with a precise timestamp in a MySQL database, allowing management to review historical activity through an easy-to-use web interface accessible from any browser. This helps prevent product theft, which was the original security problem KILIKU faced."

### Q3: "Which challenges / difficulties have you met?"

Pick 2-3 real ones, like:
> **"Three main challenges:**
> 1. **COM Port conflicts** — the Arduino Serial Monitor and my Python script both tried to use the same port simultaneously
> 2. **MySQL authentication errors** — the default XAMPP setup wouldn't let Python connect
> 3. **LED polarity confusion** — some LEDs didn't light because I had reversed the legs"

### Q4: "How did you overcome the challenges?"

> **"For each challenge:**
> 1. **COM Port conflict** — I learned that only one program can use a serial port at a time, so I always close the Arduino Serial Monitor before running the Python bridge
> 2. **MySQL authentication** — I configured MySQL to accept connections from Python using the correct credentials
> 3. **LED polarity** — I learned to always connect the long leg (anode) to the Arduino pin through the resistor, and the short leg (cathode) to GND"

---

## ✅ Project Checklist

### Preliminary Activities (15%)
- [ ] Workspace is organized and safe
- [ ] All hardware components laid out and identified
- [ ] Software installed: Arduino IDE, XAMPP, Python, Proteus
- [ ] COM port identified for Arduino

### Process & Task Fulfillment (40%)
- [ ] Proteus diagram complete and saved as PDF
- [ ] Breadboard wiring neat and matches the diagram
- [ ] Arduino code uploaded successfully
- [ ] LEDs blink at correct distances with correct delays (200/150, 250/350, 300/450 ms)
- [ ] Database `Motion_db` created with `Motion_data` table
- [ ] Python bridge script saves events to database
- [ ] PHP dashboard displays events with timestamps

### Product Quality & Presentation (35%)
- [ ] Full end-to-end demonstration works
- [ ] Clearly answered all 4 presentation questions
- [ ] Explained purpose and technology choices
- [ ] Demonstrated confidence and understanding

### Closing Activities (10%)
- [ ] Arduino and components safely disconnected
- [ ] All code files saved with clear names
- [ ] Workspace cleaned and tools returned
- [ ] Final documentation submitted

---

## 📁 Project File Structure

```
C:\kiliku_project\
├── KILIKU_motion.ino          # Arduino code
├── serial_to_db.py            # Python bridge
├── wiring_diagram.pdf         # Proteus export
└── README.md                  # This file

C:\xampp\htdocs\motion\
└── index.php                  # Web dashboard
```

---

## 🎓 Credits

**TVET Sector:** ICT and Multimedia  
**Trade:** Networking and Internet Technologies  
**RQF Level:** 5  
**Qualification:** TVET Certificate V in Networking and Internet Technologies  
**Assessment:** National Practical Examination 2024-2025  
**Client (Scenario):** KILIKU Cement Limited — Bugarama, Rusizi District, Rwanda

**Candidate Name:** _____________________  
**Index Number:** _____________________  
**School:** _____________________  
**Date:** _____________________

---

## 📜 License

Educational project for TVET Practical Examination. Free to use for learning purposes.

---

**🚀 You've got this! Work systematically, test after each step, and trust the process.**