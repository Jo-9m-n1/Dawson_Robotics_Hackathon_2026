"""Motor outputs for the Yahboom Pico Robot kit."""

try:
    from pico_car import pico_car
except ImportError:
    pico_car = None

try:
    from states import MIN_MOTOR_SPEED, MAX_MOTOR_SPEED, LEFT_TRIM, RIGHT_TRIM
except Exception:
    MIN_MOTOR_SPEED = 0.0
    MAX_MOTOR_SPEED = 1.0
    LEFT_TRIM = 1.0
    RIGHT_TRIM = 1.0


_motor = pico_car() if pico_car is not None else None


def _limit(speed: float, trim: float = 1.0) -> float:
    """Clamp signed speed to -MAX..MAX and apply minimum power when moving."""
    speed *= trim

    if speed > MAX_MOTOR_SPEED:
        speed = MAX_MOTOR_SPEED
    elif speed < -MAX_MOTOR_SPEED:
        speed = -MAX_MOTOR_SPEED

    if 0 < speed < MIN_MOTOR_SPEED:
        speed = MIN_MOTOR_SPEED
    elif -MIN_MOTOR_SPEED < speed < 0:
        speed = -MIN_MOTOR_SPEED

    return speed


def _pwm_abs(speed: float) -> int:
    """Convert absolute 0..1 speed to Yahboom's 0..255 motor range."""
    if speed < 0:
        speed = -speed
    if speed > 1:
        speed = 1
    return int(speed * 255)


def stop() -> None:
    if _motor is not None:
        _motor.Car_Stop()


def drive(left_speed: float, right_speed: float) -> None:
    """
    Signed drive control.

    Positive = forward, negative = backward.
    This allows main.py to really reverse when the line is lost.
    """
    left_speed = _limit(left_speed, LEFT_TRIM)
    right_speed = _limit(right_speed, RIGHT_TRIM)

    left_power = _pwm_abs(left_speed)
    right_power = _pwm_abs(right_speed)

    if _motor is None:
        return

    if left_speed >= 0 and right_speed >= 0:
        _motor.Car_Run(left_power, right_power)
    elif left_speed <= 0 and right_speed <= 0:
        _motor.Car_Back(left_power, right_power)
    elif left_speed < 0 and right_speed >= 0:
        _motor.Car_Left(left_power, right_power)
    else:
        _motor.Car_Right(left_power, right_power)


def forward(speed: float = 0.4) -> None:
    drive(speed, speed)


def turn_left(speed: float = 0.35) -> None:
    drive(speed * 0.45, speed)


def turn_right(speed: float = 0.35) -> None:
    drive(speed, speed * 0.45)


def backward(speed: float = 0.35) -> None:
    drive(-speed, -speed)


def spin_left(speed: float = 0.35) -> None:
    drive(-speed, speed)


def spin_right(speed: float = 0.35) -> None:
    drive(speed, -speed)


def apply_app_command(cmd: str) -> None:
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
