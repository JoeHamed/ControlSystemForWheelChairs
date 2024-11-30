# Servo Control System with Ultrasonic Sensors

This project demonstrates a Python-based servo control system that uses ultrasonic distance sensors to make decisions and a socket connection for remote commands. The system utilizes the `gpiozero` library for servo and sensor control and is designed to run on a Raspberry Pi.

---

## Features

- **Two Servo Motors**: Controlled via GPIO pins using the `gpiozero` library.
- **Three Ultrasonic Sensors**: Measure distances and make movement decisions.
- **Socket Communication**: Connects to a remote server to receive movement commands.
- **Decision Logic**: Automatically adjusts servo angles based on sensor data and remote inputs.
- **Failsafe Default Positions**: Resets servos to default positions after actions.

---

## Hardware Requirements

- Raspberry Pi (any model with GPIO support)
- 2x Servo Motors
- 3x Ultrasonic Sensors (HC-SR04 or similar)
- Breadboard and jumper wires
- External power supply for the servos (if needed)

---

## Software Requirements

- Python 3.x
- `gpiozero` library (with PiGPIOFactory support)
- Raspberry Pi OS or compatible Linux distribution
- Server to send commands to the Raspberry Pi (IP and port must match in the script)

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/<your_username>/<your_repo_name>.git
    cd <your_repo_name>
    ```

2. Install necessary Python libraries:
    ```bash
    pip install gpiozero pigpio
    ```

3. Enable `pigpiod` on your Raspberry Pi:
    ```bash
    sudo systemctl start pigpiod
    sudo systemctl enable pigpiod
    ```

4. Connect the hardware according to the wiring diagram (refer to the **Wiring** section).

5. Update the `host` and `port` variables in the script to match your server configuration.

---

## Usage

1. Run the script:
    ```bash
    python servo_control.py
    ```

2. Send commands from the server in the following format:
    ```python
    ('direction', boolean)
    ```
   - **direction**: `"left"` or `"right"`
   - **boolean**: `True` to move forward, `False` to stop.

3. The script will process the commands and adjust the servos based on ultrasonic sensor readings.

---

## Wiring

| Component            | GPIO Pin      | Description              |
|-----------------------|---------------|--------------------------|
| Servo 1              | GPIO 11       | Connected via PiGPIOFactory |
| Servo 2              | GPIO 9        | Connected via PiGPIOFactory |
| Ultrasonic Sensor 1  | GPIO 17, GPIO 4  | Trigger and Echo pins   |
| Ultrasonic Sensor 2  | GPIO 27, GPIO 23 | Trigger and Echo pins   |
| Ultrasonic Sensor 3  | GPIO 22, GPIO 25 | Trigger and Echo pins   |

---

## Code Overview

### Functions

- `setServo1Angle(direction)`: Adjusts Servo 1 based on the given direction.
- `setServo2Angle(direction)`: Adjusts Servo 2 for left or right turns.
- `setDefaultServo1Angle()` and `setDefaultServo2Angle()`: Resets the servos to their default (90°) positions.
- `create_socket()`: Establishes a socket connection and handles incoming commands.

---

## Known Issues

- Ultrasonic sensors may return inconsistent values if obstacles are too close.
- Network latency can impact real-time performance.
- Servos might jitter if underpowered; ensure a stable power supply.

---

