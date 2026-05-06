# Kit Setup - Yahboom Pico Robot

Use this file to connect the starter code to the robot kit quickly.

## Required Yahboom pieces

- `pico_car.py` library file copied to the Pico.
- YahboomRobot mobile app installed for manual maze control.
- Bluetooth module connected and powered.
- Robot battery charged before testing.

## Motor API

The starter `motors.py` wraps the Yahboom motor helper:

| Starter function | Yahboom call |
| --- | --- |
| `forward(speed)` | `Motor.Car_Run(left, right)` |
| `backward(speed)` | `Motor.Car_Back(left, right)` |
| `turn_left(speed)` | `Motor.Car_Run(0, right)` |
| `turn_right(speed)` | `Motor.Car_Run(left, 0)` |
| `spin_left(speed)` | `Motor.Car_Left(left, right)` |
| `spin_right(speed)` | `Motor.Car_Right(left, right)` |
| `stop()` | `Motor.Car_Stop()` |

The starter uses `0.0` to `1.0` speeds and converts them to Yahboom's `0` to `255` motor range.

## Tracking sensor

The four line sensors are read left to right:

| Sensor | GPIO |
| --- | ---: |
| Left outer | 2 |
| Left inner | 3 |
| Right inner | 4 |
| Right outer | 5 |

Yahboom examples treat black as `0` and white as `1`.

## Ultrasonic distance

The starter calls:

```python
ultrasonic().Distance_accurate()
```

Use the printed distance values during practice to tune `OBSTACLE_CM` in `states.py`.

## Manual maze app

The YahboomRobot app sends two-byte Bluetooth commands over UART 0:

| App action | Command |
| --- | --- |
| Forward | `A#` |
| Back | `B#` |
| Turn left | `C#` |
| Turn right | `D#` |
| Spin left | `E#` |
| Spin right | `F#` |
| Stop | `0#` |

UART settings used by the starter:

```python
UART(0, 9600, bits=8, parity=None, stop=1, tx=Pin(16), rx=Pin(17))
```

For the official run, the line-following and box-entry phases should run from code. The maze phase is manually driven with the app.
