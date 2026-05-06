"""Sensor reads for the Yahboom Pico Robot kit."""

try:
    from machine import Pin, UART
    from pico_car import ultrasonic as YahboomUltrasonic
except ImportError:
    Pin = UART = YahboomUltrasonic = None  # allows lint on host


_tracking_pins = None
_ultrasonic = None
_uart = None
_last_app_command = "stop"

_APP_COMMANDS = {
    b"A#": "forward",
    b"B#": "back",
    b"C#": "left",
    b"D#": "right",
    b"E#": "left_spin",
    b"F#": "right_spin",
    b"0#": "stop",
}


def _tracking():
    global _tracking_pins
    if _tracking_pins is None and Pin is not None:
        # Yahboom tracking sensors 1-4 are GPIO 2-5, left to right.
        _tracking_pins = tuple(Pin(pin, Pin.IN) for pin in (2, 3, 4, 5))
    return _tracking_pins


def _distance_sensor():
    global _ultrasonic
    if _ultrasonic is None and YahboomUltrasonic is not None:
        _ultrasonic = YahboomUltrasonic()
    return _ultrasonic


def _bluetooth_uart():
    global _uart
    if _uart is None and UART is not None and Pin is not None:
        _uart = UART(0, 9600, bits=8, parity=None, stop=1, tx=Pin(16), rx=Pin(17))
    return _uart


def line_values():
    """
    Return four line sensor values from left to right.

    Yahboom tracking sensors report black as 0 and white as 1.
    """
    pins = _tracking()
    if pins is None:
        return (1, 0, 0, 1)
    return tuple(pin.value() for pin in pins)


def line_direction():
    """
    Return steering hint from the four tracking sensors.

    -1 means steer left, 0 means forward, 1 means steer right.
    None means the line is probably lost.
    """
    left_outer, left_inner, right_inner, right_outer = line_values()

    if (left_inner == 0) and (right_inner == 0):
        return 0
    if left_outer == 0 or left_inner == 0:
        return -1
    if right_outer == 0 or right_inner == 0:
        return 1
    return None


def line_center_dark() -> bool:
    """Return True if either center sensor sees the dark line."""
    _, left_inner, right_inner, _ = line_values()
    return left_inner == 0 or right_inner == 0


def ultrasonic_cm() -> float:
    """Forward distance in cm; return large value if no echo."""
    sensor = _distance_sensor()
    if sensor is None:
        return 999.0
    try:
        return float(sensor.Distance_accurate())
    except Exception:
        return 999.0


def app_command() -> str:
    """Return the latest manual-control command from the YahboomRobot app."""
    global _last_app_command

    uart = _bluetooth_uart()
    if uart is None:
        return _last_app_command

    while uart.any() >= 2:
        raw = uart.read(2)
        _last_app_command = _APP_COMMANDS.get(raw, _last_app_command)

    return _last_app_command
