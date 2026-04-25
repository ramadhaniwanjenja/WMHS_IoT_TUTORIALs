import serial
import mysql.connector
import time

# Change COM port to match yours
arduino = serial.Serial('COM5', 115200, timeout=1)
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