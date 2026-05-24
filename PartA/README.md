# 🌱 ICT5101 - IoT Project PartA Plant Monitoring System

This folder contains **Part A** of the ICT5101 Internet of Things coursework.

The project implements a simple **remote plant monitoring system** using an Arduino-based soil moisture sensor, an RGB LED indicator, an OLED display and a Python dashboard. 

## 📚 Table of Contents

- [📋 Project Overview](#-project-overview)
- [🧩 System Components](#-system-components)
- [📁 Folder Structure](#-folder-structure)
- [🔌 Arduino Scripts](#-arduino-scripts)
- [📊 Python Dashboard](#-python-dashboard)
- [⚙️ Installation](#️-installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
- [▶️ Running the Dashboard](#️-running-the-dashboard)
- [📝 Notes](#-notes)
- [👍 Acknowledgments](#-acknowledgments)

## 📋 Project Overview

The system is designed to monitor soil moisture levels and provide both local and remote feedback.

The Arduino handles the physical sensing and output components, while the Python dashboard provides a user-friendly interface for viewing and logging readings over time.

Main features include:

- Reading soil moisture values using an analogue moisture sensor
- Displaying the moisture percentage on an OLED screen
- Showing moisture status using an RGB LED
- Sending readings to a Python dashboard over serial communication
- Logging readings into a CSV file
- Visualising moisture trends using an interactive graph
- Showing latest, daily average, and weekly average moisture readings

## 🧩 System Components

The implementation uses:

- Arduino-compatible microcontroller
- Soil moisture sensor
- RGB LED
- OLED display
- Serial communication
- Python Dash dashboard

## 🗃️ Folder Structure

```bash
PartA/
│
├── Docs/
│   ├── PartA_ICT5101 Assignment 2026.pdf
│   │
│   ├── circuit_diagram/
│   │   ├── ICT5101_CiruitDiagram.fzz
│   │   └── ICT5101_CiruitDiagram.png
│   │
│   ├── datasheets/
│   │   ├── Arduino-Nano-datasheet.pdf
│   │   ├── OLED-display-module.pdf
│   │   ├── rgb-led.pdf
│   │   └── soil-moisture-sensor-ME110.pdf
│   │
│   ├── imgs/
│   │   └── dashboard.png
│   │
│   └── report/
│       └── ICT5101_IoT_PartA_Project_Report.pdf
│
├── arduino_scripts/
│   ├── ict5101_project_imp/
│   │   └── ict5101_project_imp.ino
│   │
│   ├── moisture_sensor_test/
│   │   └── moisture_sensor_test.ino
│   │
│   └── rgb_led_test/
│       └── rgb_led_test.ino
│
├── README.md
├── dashboard.py
├── moisture_history.csv    # Optional
└── requirements.txt
```

## 🔌 Arduino Scripts

The `arduino_scripts/` folder contains the Arduino code used during development and testing.

- **ict5101_project_imp/**<br>
Contains the main project implementation. It reads the moisture sensor value, converts it to a percentage, sends the value over serial communication, updates the OLED display, and changes the RGB LED colour based on the moisture level.

- **moisture_sensor_test/**<br>
Contains a calibration and testing script for reading raw soil moisture sensor values.

- **rgb_led_test/**<br>
Contains a simple script for testing the RGB LED colours.

## 📊 Python Dashboard

The `dashboard.py` file runs a local Dash dashboard for monitoring the plant moisture readings.

The dashboard allows the user to:

- Select the Arduino serial port
- Connect to the Arduino
- Read new moisture values automatically
- View the latest moisture reading
- View today’s average moisture level
- View the weekly average moisture level
- Check the current plant status
- Display a moisture-over-time graph
- Save readings to `moisture_history.csv`

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/DavidF-22/ICT5101-IoT_Project.git
cd ICT5101-IoT_Project/PartA
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python dependencies using:
```bash
pip install -r requirements.txt
```

Alternatively, install the main packages manually:
```bash
pip install pyserial dash plotly pandas
```

## ▶️ Running the Dashboard
Upload the main Arduino sketch to the board first, then connect the Arduino to the computer.

Run the dashboard using:
```bash
python dashboard.py
```

The dashboard will open locally at:
```text
http://127.0.0.1:8050
```

## 📝 Notes
- The Arduino and dashboard must use the same baud rate.
- The default baud rate used by the project is 9600.
- The dashboard reads values from the Arduino every 5 seconds.
- Moisture readings are saved in moisture_history.csv.
- A dry soil threshold is used to determine whether watering is needed.

## 👍 Acknowledgments

This individual project was carried out as part of the partial fulfilment of the requirements for the **ICT5101 Internet of Things** course @ **[The University of Malta](https://www.um.edu.mt/)**.

## 📧 Contact

For any inquiries or feedback, please contact [David Farrugia](mailto:david.farrugia.22@um.edu.mt)