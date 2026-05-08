"""Main program: line following with faster turns and stronger reverse recovery."""

import time
import sensors
import motors
from states import (
    STRAIGHT_SPEED,
    ANGLE_SPEED,
    CORNER_INNER_SPEED,
    CORNER_OUTER_SPEED,
    KP,
    KD,
    MAX_CORRECTION,
    LINE_DEADBAND,
    ANGLE_ERROR,
    CORNER_ERROR,
    LOST_BACK_SPEED,
    LOST_BACK_CURVE,
    LINE_LOST_STOP_MS,
    LOOP_DELAY_MS,
    RUN_TIMEOUT_MS,
)


def ticks_ms():
    if hasattr(time, "ticks_ms"):
        return time.ticks_ms()
    return int(time.time() * 1000)


def ticks_diff(now, before):
    if hasattr(time, "ticks_diff"):
        return time.ticks_diff(now, before)
    return now - before


def sleep_ms(ms):
    if hasattr(time, "sleep_ms"):
        time.sleep_ms(ms)
    else:
        time.sleep(ms / 1000)


def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value


run_start = ticks_ms()
last_seen = run_start
last_error = 0.0
last_debug = 0

while True:
    now = ticks_ms()

    if RUN_TIMEOUT_MS and ticks_diff(now, run_start) > RUN_TIMEOUT_MS:
        motors.stop()
        break

    values = sensors.line_values()
    error = sensors.line_error()

    if error is None:
        # No sensor sees the tape: reverse more strongly.
        # Curve backward toward the last side where the line was seen.
        if ticks_diff(now, last_seen) > LINE_LOST_STOP_MS:
            motors.stop()
        elif last_error < -LINE_DEADBAND:
            # Last line was left, back up while curving left.
            motors.drive(-(LOST_BACK_SPEED + LOST_BACK_CURVE), -(LOST_BACK_SPEED - LOST_BACK_CURVE))
        elif last_error > LINE_DEADBAND:
            # Last line was right, back up while curving right.
            motors.drive(-(LOST_BACK_SPEED - LOST_BACK_CURVE), -(LOST_BACK_SPEED + LOST_BACK_CURVE))
        else:
            motors.drive(-LOST_BACK_SPEED, -LOST_BACK_SPEED)

    else:
        last_seen = now

        if abs(error) <= LINE_DEADBAND:
            # Stable straight line: go fast and do not over-correct.
            motors.drive(STRAIGHT_SPEED, STRAIGHT_SPEED)
            last_error = 0.0

        elif abs(error) >= CORNER_ERROR:
            # Edge/corner: turn faster, but keep both wheels moving forward.
            if error < 0:
                motors.drive(CORNER_INNER_SPEED, CORNER_OUTER_SPEED)
            else:
                motors.drive(CORNER_OUTER_SPEED, CORNER_INNER_SPEED)
            last_error = error

        else:
            # Normal angled line: slow down a little and correct smoothly.
            derivative = error - last_error
            correction = KP * error + KD * derivative
            correction = clamp(correction, -MAX_CORRECTION, MAX_CORRECTION)

            speed = ANGLE_SPEED if abs(error) >= ANGLE_ERROR else STRAIGHT_SPEED
            left_speed = speed + correction
            right_speed = speed - correction
            motors.drive(left_speed, right_speed)
            last_error = error

    if ticks_diff(now, last_debug) > 350:
        print("values=", values, "error=", error, "last=", last_error)
        last_debug = now

    sleep_ms(LOOP_DELAY_MS)
