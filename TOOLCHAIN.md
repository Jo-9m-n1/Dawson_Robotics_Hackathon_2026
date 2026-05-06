# Toolchain - Pico 2 + MicroPython

## Recommended path (beginners)

1. Install **Thonny** ([https://thonny.org/](https://thonny.org/)) on your laptop.
2. Install **MicroPython for Raspberry Pi Pico 2** — use the build linked from the official Raspberry Pi documentation for Pico 2, **or** the exact `.uf2` version your TA names on the first workshop day.
3. Connect the Pico 2 with USB while holding **BOOTSEL** if the board is not seen; drag the `.uf2` onto the drive that appears.
4. In Thonny: **Run → Configure interpreter → MicroPython (Raspberry Pi Pico)**; select the correct COM port.
5. Copy the Yahboom `pico_car.py` library file to the **device**.
6. Save this starter kit's `.py` files to the **device**.
7. Save `main.py` to the **device** so it runs on power-up.

## Alternate path

- **VS Code** with Raspberry Pi Pico extension, or **mpremote** for REPL and file copy. Same firmware rule as above.

## Project layout


| File         | Role                                                                       |
| ------------ | -------------------------------------------------------------------------- |
| `main.py`    | Super loop: read sensors, update state, set motors                         |
| `states.py`  | State names and simple transition helpers                                  |
| `sensors.py` | Yahboom tracking sensors, ultrasonic distance, and app command reads        |
| `motors.py`  | Yahboom motor helper wrapper                                               |

## Yahboom references to check

- Development environment construction: update firmware, build environment, import library file, and set startup code.
- Robot course 5.2: car movement.
- Robot course 5.4: car tracking.
- Robot course 5.6: ultrasonic avoiding.
- Robot course 5.11: Bluetooth control with the YahboomRobot app.

## Do not

- Do not `pip install` on the microcontroller.
- Do not leave USB tethered during an official trial.
