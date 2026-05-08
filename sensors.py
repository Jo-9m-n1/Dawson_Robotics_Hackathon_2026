"""Sensor reads for the Yahboom Pico Robot kit."""

try:
    from machine import Pin, UART
    from pico_car import ultrasonic as YahboomUltrasonic
except ImportError:
    Pin = UART = YahboomUltrasonic = None

try:
    from states import BLACK_VALUE
except Exception:
    BLACK_VALUE = 0

_tracking_pins = None
_ultrasonic = None
_uart = None
_last_app_command = "stop"
_uart_buffer = b""

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
    """Return four line sensor values from left to right."""
    pins = _tracking()
    if pins is None:
        return (1, 0, 0, 1)
    return tuple(pin.value() for pin in pins)


def is_black(value):
    return value == BLACK_VALUE


def black_flags():
    """Return booleans: left_outer, left_inner, right_inner, right_outer."""
    return tuple(is_black(v) for v in line_values())


def center_seen():
    """True when either middle sensor sees black tape."""
    _, left_inner, right_inner, _ = black_flags()
    return left_inner or right_inner


def any_seen():
    """True when any of the four sensors sees black tape."""
    return any(black_flags())


def line_error():
    """
    Return where the black tape is.

    Negative = tape is to the left.
    0 = centered.
    Positive = tape is to the right.
    None = no sensor sees the tape.

    This version is intentionally calm on straight lines and stronger only when
    the outside sensors clearly see an angle/corner.
    """
    left_outer, left_inner, right_inner, right_outer = black_flags()

    if not (left_outer or left_inner or right_inner or right_outer):
        return None

    # Straight / almost straight patterns.
    if left_inner and right_inner:
        if left_outer and not right_outer:
            return -0.45
        if right_outer and not left_outer:
            return 0.45
        return 0.0

    # Slightly off-center patterns.
    if left_inner and not right_inner:
        return -0.85
    if right_inner and not left_inner:
        return 0.85

    # Corner / angle patterns: only outside sensor sees tape.
    if left_outer and not right_outer:
        return -2.20
    if right_outer and not left_outer:
        return 2.20

    # Weird wide pattern: stay calm instead of spinning.
    return 0.0


def line_direction():
    """Compatibility helper: -1 left, 0 straight, 1 right, None lost."""
    error = line_error()
    if error is None:
        return None
    if error < -0.4:
        return -1
    if error > 0.4:
        return 1
    return 0


def line_center_dark():
    return center_seen()


def ultrasonic_cm():
    sensor = _distance_sensor()
    if sensor is None:
        return 999.0
    try:
        distance = float(sensor.Distance_accurate())
        if distance <= 0:
            return 999.0
        return distance
    except Exception:
        return 999.0


def app_command():
    global _last_app_command, _uart_buffer

    uart = _bluetooth_uart()
    if uart is None:
        return _last_app_command

    available = uart.any()
    if available:
        data = uart.read(available)
        if data:
            _uart_buffer = (_uart_buffer + data)[-12:]

    while b"#" in _uart_buffer:
        end = _uart_buffer.find(b"#")
        packet = _uart_buffer[max(0, end - 1):end + 1]
        _uart_buffer = _uart_buffer[end + 1:]
        if packet in _APP_COMMANDS:
            _last_app_command = _APP_COMMANDS[packet]

    return _last_app_command
