"""Motor outputs for the Yahboom Pico Robot kit."""

try:
    from pico_car import pico_car
except ImportError:
    pico_car = None


_motor = pico_car() if pico_car is not None else None


def _pwm(speed: float) -> int:
    """Convert 0..1 starter speed to Yahboom's 0..255 motor range."""
    if speed < 0:
        speed = 0
    if speed > 1:
        speed = 1
    return int(speed * 255)


def stop() -> None:
    """All motors off."""
    if _motor is not None:
        _motor.Car_Stop()


def forward(speed: float = 0.4) -> None:
    """Drive forward; speed is 0..1."""
    power = _pwm(speed)
    if _motor is not None:
        _motor.Car_Run(power, power)


def turn_left(speed: float = 0.35) -> None:
    """Arc left by slowing/stopping the left motor."""
    power = _pwm(speed)
    if _motor is not None:
        _motor.Car_Run(0, power)


def turn_right(speed: float = 0.35) -> None:
    """Arc right by slowing/stopping the right motor."""
    power = _pwm(speed)
    if _motor is not None:
        _motor.Car_Run(power, 0)


def backward(speed: float = 0.35) -> None:
    power = _pwm(speed)
    if _motor is not None:
        _motor.Car_Back(power, power)


def spin_left(speed: float = 0.35) -> None:
    power = _pwm(speed)
    if _motor is not None:
        _motor.Car_Left(power, power)


def spin_right(speed: float = 0.35) -> None:
    power = _pwm(speed)
    if _motor is not None:
        _motor.Car_Right(power, power)


def apply_app_command(cmd: str) -> None:
    """Map app commands to robot motion."""
    if cmd == "forward":
        forward()
    elif cmd == "back":
        backward()
    elif cmd == "left":
        turn_left()
    elif cmd == "right":
        turn_right()
    elif cmd == "left_spin":
        spin_left()
    elif cmd == "right_spin":
        spin_right()
    else:
        stop()
