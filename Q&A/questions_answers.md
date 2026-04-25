# 📚 IoT Projects — 50 Q&A Study Guide

> Networking and Internet Technologies — RQF Level 5  
> Covers: Arduino, ESP8266, DHT11, HC-SR04, MySQL, PHP, IoT concepts

---

## 🔰 SECTION A: BASIC IoT CONCEPTS (Q1–Q10)

### Q1. What is IoT?
**Answer:** IoT (Internet of Things) is a network of physical devices like sensors, microcontrollers, and appliances that connect to the internet to collect, exchange, and act on data.

### Q2. Give 3 real-life examples of IoT.
**Answer:**
1. Smart home devices (smart bulbs, thermostats)
2. Fitness trackers (smartwatches)
3. Greenhouse monitoring systems (like our project)

### Q3. What are the 4 main components of an IoT system?
**Answer:**
1. **Sensors** — collect data (DHT11, HC-SR04)
2. **Microcontroller** — processes data (Arduino, ESP8266)
3. **Network** — sends data (WiFi, USB)
4. **Server/Database** — stores and displays data (MySQL, PHP)

### Q4. What is a microcontroller?
**Answer:** A small computer on a single chip that reads inputs from sensors, processes them according to a program, and controls outputs like LEDs or motors.

### Q5. What is the difference between Arduino Uno and ESP8266?
**Answer:**
- **Arduino Uno:** No built-in WiFi, uses USB cable, runs on 5V
- **ESP8266:** Has built-in WiFi, can connect wirelessly, runs on 3.3V

### Q6. What is a sensor?
**Answer:** A device that detects physical quantities like temperature, distance, or motion, and converts them into electrical signals a microcontroller can read.

### Q7. What is an actuator?
**Answer:** A device that performs an action based on a signal, such as LEDs lighting up, motors spinning, or buzzers sounding.

### Q8. What is the difference between digital and analog signals?
**Answer:**
- **Digital:** Only two states — HIGH (1) or LOW (0)
- **Analog:** Continuous range of values (e.g., 0 to 1023)

### Q9. What is a breadboard?
**Answer:** A reusable plastic board with holes for plugging components, used to build temporary circuits without soldering.

### Q10. What is a resistor and why do we use it with LEDs?
**Answer:** A resistor limits the flow of electrical current. We use it with LEDs to prevent too much current from burning out the LED.

---

## 🔌 SECTION B: HARDWARE & WIRING (Q11–Q20)

### Q11. What is the HC-SR04 sensor used for?
**Answer:** It's an ultrasonic sensor that measures distance by sending sound waves and timing how long they take to bounce back.

### Q12. Explain how the HC-SR04 works.
**Answer:** The TRIG pin sends a sound pulse. The ECHO pin receives the bounced echo. The microcontroller measures the echo time and calculates distance using:  
`distance (cm) = time × 0.034 / 2`

### Q13. Why do we divide by 2 in the distance formula?
**Answer:** Because the sound wave travels to the object **and** back. Dividing by 2 gives the one-way distance.

### Q14. What is the DHT11 sensor used for?
**Answer:** It measures **temperature** (in °C) and **humidity** (in %) using a single data pin.

### Q15. Why does DHT11 need a pull-up resistor?
**Answer:** A 10kΩ pull-up resistor between the DATA pin and VCC keeps the data line stable and prevents reading errors.

### Q16. What's the difference between an LED's anode and cathode?
**Answer:**
- **Anode (long leg):** Positive (+) — connects to power through resistor
- **Cathode (short leg):** Negative (−) — connects to GND

### Q17. What happens if you connect an LED backwards?
**Answer:** It simply won't light up. LEDs only allow current to flow in one direction.

### Q18. Why do we use 220Ω resistors for LEDs?
**Answer:** They limit the current to a safe level (about 15–20 mA), protecting both the LED and the microcontroller pin.

### Q19. What is the role of GND (Ground)?
**Answer:** GND is the common reference point and the return path for current in a circuit. All grounds must connect together.

### Q20. What is the difference between 5V and 3.3V power?
**Answer:**
- **5V:** Used by Arduino Uno and most sensors like HC-SR04
- **3.3V:** Used by ESP8266; its pins can be damaged by 5V

---

## 💻 SECTION C: ARDUINO PROGRAMMING (Q21–Q30)

### Q21. What are the two main functions in every Arduino sketch?
**Answer:**
1. `setup()` — runs once when the board powers on
2. `loop()` — runs continuously, over and over

### Q22. What does `pinMode()` do?
**Answer:** It sets a pin to either INPUT (read data) or OUTPUT (send signals).  
Example: `pinMode(13, OUTPUT);`

### Q23. What does `digitalWrite()` do?
**Answer:** It sets a digital pin to either HIGH (5V) or LOW (0V).  
Example: `digitalWrite(13, HIGH);` turns the LED on.

### Q24. What is `Serial.begin(9600)` used for?
**Answer:** It starts serial communication between the Arduino and the computer at 9600 bits per second, allowing data to be sent through USB.

### Q25. What does `delay(1000)` do?
**Answer:** It pauses the program for 1000 milliseconds (1 second).

### Q26. What is `pulseIn()` used for in our project?
**Answer:** It measures how long a pin stays HIGH in microseconds. We use it to time the echo from the ultrasonic sensor.

### Q27. Why do we put a `delay(2000)` after `dht.begin()`?
**Answer:** The DHT11 sensor needs about 2 seconds to stabilize when it powers on. Reading too early gives `nan` (not a number) errors.

### Q28. What does `isnan()` mean?
**Answer:** "Is Not a Number" — a function that checks if a sensor reading failed to return a valid value.

### Q29. What is a library in Arduino?
**Answer:** A collection of pre-written code that adds new functions. For example, the **DHT library** lets us read DHT11 sensors easily.

### Q30. How do you upload code to an Arduino?
**Answer:**
1. Connect Arduino via USB
2. In Arduino IDE: select **Tools → Board** and **Tools → Port**
3. Click the **Upload (→)** button
4. Wait for "Done uploading" message

---

## 🌐 SECTION D: ESP8266 & WIFI (Q31–Q35)

### Q31. What is the ESP8266?
**Answer:** A low-cost microcontroller with built-in WiFi, perfect for IoT projects that need wireless connectivity.

### Q32. What library do we use for WiFi on ESP8266?
**Answer:** `ESP8266WiFi.h` for WiFi connection and `ESP8266HTTPClient.h` for sending HTTP requests.

### Q33. What is HTTP POST?
**Answer:** A method for sending data to a web server. In our project, the ESP8266 uses HTTP POST to send temperature, humidity, and status to `insert.php`.

### Q34. Why does ESP8266 only support 2.4GHz WiFi?
**Answer:** Because of its hardware design — the WiFi chip is built only for the 2.4GHz frequency band, not 5GHz.

### Q35. What is an IP address?
**Answer:** A unique number assigned to each device on a network so devices can find and talk to each other (e.g., `192.168.18.27`).

---

## 🗄️ SECTION E: DATABASE (MySQL) (Q36–Q42)

### Q36. What is a database?
**Answer:** An organized collection of data stored on a computer that can be easily searched, updated, and managed.

### Q37. What is MySQL?
**Answer:** A popular free database management system that uses SQL (Structured Query Language) to store and retrieve data.

### Q38. What is SQL?
**Answer:** Structured Query Language — the standard language for talking to databases. It's used to create, read, update, and delete data.

### Q39. What is phpMyAdmin?
**Answer:** A web-based tool that lets you manage MySQL databases through a browser, without needing the command line.

### Q40. Write SQL to create the `Motion_db` database and `Motion_data` table.
**Answer:**
```sql