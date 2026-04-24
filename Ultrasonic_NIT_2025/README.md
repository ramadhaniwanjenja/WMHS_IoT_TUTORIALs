# KILIKU Cement - Motion Sensing & Detection System

An IoT-based proximity security system for KILIKU Cement Limited (Bugarama, Rusizi District). Uses an ultrasonic sensor to detect objects near the company gate, triggers colored LEDs based on distance, logs all events to a MySQL database, and displays them on a PHP web interface.

## Table of Contents
- [Project Overview](#project-overview)
- [System Architecture](#system-architecture)
- [Materials & Components](#materials--components)
- [Wiring Diagram](#wiring-diagram)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Project Setup](#project-setup)
- [Running the System](#running-the-system)
- [Troubleshooting](#troubleshooting)
- [Presentation Q&A](#presentation-qa)

## Project Overview

| Distance Range | LED Color | On Delay | Off Delay |
|----------------|-----------|----------|-----------|
| Within 30 cm   | Red       | 200 ms   | 150 ms    |
| Within 20 cm   | Green     | 250 ms   | 350 ms    |
| Within 10 cm   | Blue      | 300 ms   | 450 ms    |

## System Architecture

# HC-SR04 Sensor → Arduino Uno → Serial (USB) → Python Bridge → MySQL Database → PHP Web Interface

## Materials & Components

### Hardware
- 1 × Arduino Uno with USB cable
- 1 × HC-SR04 Ultrasonic Sensor
- 1 × Red LED
- 1 × Green LED
- 1 × Blue LED
- 3 × 220Ω resistors
- 1 × Breadboard
- 10 × Jumper wires (male-to-male)
- 1 × Laptop/PC

### Software
- Arduino IDE
- Proteus (for circuit diagram)
- Apache2 + MySQL + PHP (LAMP stack)
- phpMyAdmin
- Python 3 with `pyserial` and `mysql-connector-python`

## Wiring Diagram

| Component        | Pin       | Arduino Pin |
|------------------|-----------|-------------|
| HC-SR04          | VCC       | 5V          |
| HC-SR04          | GND       | GND         |
| HC-SR04          | TRIG      | Pin 9       |
| HC-SR04          | ECHO      | Pin 10      |
| Red LED (+220Ω)  | Anode     | Pin 2       |
| Red LED          | Cathode   | GND         |
| Green LED (+220Ω)| Anode     | Pin 3       |
| Green LED        | Cathode   | GND         |
| Blue LED (+220Ω) | Anode     | Pin 4       |
| Blue LED         | Cathode   | GND         |

## Software Requirements

- Ubuntu 20.04+ (or any Linux distro)
- Arduino IDE 1.8+
- PHP 7.4+
- MySQL 8.0+
- Python 3.8+

## Installation

### 1. Install system packages

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install arduino apache2 mysql-server php php-mysql libapache2-mod-php phpmyadmin python3 python3-pip -y
pip3 install pyserial mysql-connector-python --break-system-packages
```

### 2. Configure MySQL

```bash
sudo mysql
```

Inside MySQL:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '1234';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Link phpMyAdmin to Apache

```bash
sudo ln -s /etc/phpmyadmin/apache.conf /etc/apache2/conf-available/phpmyadmin.conf
sudo a2enconf phpmyadmin
sudo systemctl reload apache2
```

### 4. Grant USB port permissions

```bash
sudo usermod -a -G dialout $USER
```

**Log out and log back in** for this to take effect.

### 5. Verify Arduino port

```bash
ls /dev/ttyACM* /dev/ttyUSB*
```

Note the port (usually `/dev/ttyACM0`).

## Project Setup

### 1. Create the database

Open `http://localhost/phpmyadmin`, log in as `root` with password `1234`, go to the SQL tab and run:

```sql
CREATE DATABASE Motion_db;

USE Motion_db;

CREATE TABLE Motion_data (
  Id INT AUTO_INCREMENT PRIMARY KEY,
  Motion_Detected VARCHAR(150) NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Arduino Code

Save as `KILIKU_motion.ino` and upload via Arduino IDE (Tools → Board: Arduino Uno, Tools → Port: /dev/ttyACM0).

```cpp
// KILIKU Cement - Motion Sensing & Detection System
#define TRIG_PIN 9
#define ECHO_PIN 10
#define LED_RED   2   // Within 30 cm
#define LED_GREEN 3   // Within 20 cm
#define LED_BLUE  4   // Within 10 cm

long duration;
int distance;

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);
  distance = duration * 0.034 / 2;

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  digitalWrite(LED_RED, LOW);
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_BLUE, LOW);

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

### 3. Python Bridge Script

Save as `~/serial_to_db.py`:

```python
import serial
import mysql.connector
import time

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='Motion_db'
)
cursor = db.cursor()

print("Listening to Arduino... (press Ctrl+C to stop)")

while True:
    try:
        line = arduino.readline().decode('utf-8').strip()
        if line and "Motion detected" in line:
            sql = "INSERT INTO Motion_data (Motion_Detected) VALUES (%s)"
            cursor.execute(sql, (line,))
            db.commit()
            print(f"Saved: {line}")
    except Exception as e:
        print("Error:", e)
        time.sleep(1)
```

### 4. PHP Web Interface

Create the web directory and file:

```bash
sudo mkdir /var/www/html/motion
sudo nano /var/www/html/motion/index.php
```

Paste this into `index.php`:

```php
<?php
$conn = new mysqli('localhost', 'root', '1234', 'Motion_db');
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$result = $conn->query("SELECT * FROM Motion_data ORDER BY timestamp DESC");
?>
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>KILIKU Cement - Motion Events</title>
  <meta http-equiv="refresh" content="5">
  <style>
    body { font-family: Arial, sans-serif; margin: 30px; background:#f0f2f5; }
    h1 { color:#1a4d2e; }
    table { width: 100%; border-collapse: collapse; background:#fff; box-shadow:0 2px 5px rgba(0,0,0,.1); }
    th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
    th { background:#1a4d2e; color:#fff; }
    tr:nth-child(even) { background:#f7f7f7; }
    .badge { padding:4px 8px; border-radius:4px; color:#fff; font-size:12px; }
    .red{background:#c0392b} .green{background:#27ae60} .blue{background:#2980b9}
  </style>
</head>
<body>
  <h1>KILIKU Cement Ltd — Motion Detection Log</h1>
  <p>Total events recorded: <?= $result->num_rows ?></p>
  <table>
    <tr><th>ID</th><th>Event</th><th>Zone</th><th>Timestamp</th></tr>
    <?php while($row = $result->fetch_assoc()):
        $zone = 'red';
        if (strpos($row['Motion_Detected'],'10cm')!==false) $zone='blue';
        elseif (strpos($row['Motion_Detected'],'20cm')!==false) $zone='green';
    ?>
      <tr>
        <td><?= $row['Id'] ?></td>
        <td><?= htmlspecialchars($row['Motion_Detected']) ?></td>
        <td><span class="badge <?= $zone ?>"><?= strtoupper($zone) ?></span></td>
        <td><?= $row['timestamp'] ?></td>
      </tr>
    <?php endwhile; ?>
  </table>
</body>
</html>
```

Set permissions:

```bash
sudo chown -R www-data:www-data /var/www/html/motion
```

## Running the System

Run these in order every time you want to start the system:

```bash
# 1. Start services
sudo systemctl start apache2 mysql

# 2. Upload Arduino code via Arduino IDE (one-time)

# 3. Close Arduino Serial Monitor if open, then run Python bridge
python3 ~/serial_to_db.py

# 4. Open browser
# Visit: http://localhost/motion/
```

Wave your hand in front of the ultrasonic sensor. You should see:
- LEDs blinking based on distance
- Python terminal printing `Saved: Motion detected...`
- Web page auto-refreshing with new entries every 5 seconds

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Permission denied: '/dev/ttyACM0'` | Run `sudo usermod -a -G dialout $USER`, then log out and back in |
| Arduino IDE can't find the port | Check `ls /dev/tty*` before and after plugging in Arduino |
| `Access denied for user 'root'@'localhost'` | Re-run the `ALTER USER` MySQL command |
| Python error: port busy | Close Arduino Serial Monitor before running Python script |
| PHP code shows as raw text | Run `sudo a2enmod php && sudo systemctl restart apache2` |
| phpMyAdmin 404 error | Re-run the symlink commands in Installation step 3 |
| `ModuleNotFoundError: serial` | Run `pip3 install pyserial --break-system-packages` |
| Distance always reads 0 | Check TRIG/ECHO wiring; make sure they aren't swapped |
| LEDs don't light up | LED polarity is wrong — flip the LED (long leg = positive) |

## Presentation Q&A

**Q1: Name your product and key steps**
> Proximity-Triggered LED Security System with Database Logging. Steps: identified components, designed Proteus diagram, assembled on breadboard, coded Arduino, created MySQL database, built Python bridge, developed PHP interface, tested end-to-end.

**Q2: Use/function/importance**
> Enhances physical security at KILIKU Cement gate. Detects approaching objects at 30 cm, 20 cm, 10 cm ranges with color-coded warnings. Logs every event with timestamp for security review, helping prevent product theft.

**Q3: Challenges met**
> USB port permissions on Linux, serial port conflicts between Arduino IDE and Python, MySQL authentication method mismatch.

**Q4: How I overcame them**
> Added user to `dialout` group for USB access, ensured only one program uses the serial port at a time, switched MySQL root to `mysql_native_password` authentication.

## Author

**Candidate Name:** [Your Name]
**Trade:** Networking and Internet Technologies
**RQF Level:** 5
**School Year:** 2024-2025

## License

Educational project for TVET National Practical Examination.