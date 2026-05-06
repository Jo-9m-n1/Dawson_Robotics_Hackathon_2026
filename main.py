"""
Pico2 Hackathon 2026 - minimal state-machine loop.

Tunables for practice:
  - LINE_LOST_MS, OBSTACLE_CM from states.py
  - Tune sensors.line_direction() and motors.* behavior for your robot.
"""

import time
from states import States, LINE_LOST_MS, OBSTACLE_CM, BOX_ENTRY_MAX_MS
import sensors
import motors

state = States.S1_FOLLOW_LINE
_last_line_seen_ms = time.ticks_ms()
_box_entry_start_ms = 0


def ticks_ms() -> int:
    return time.ticks_ms()


while True:
    now = ticks_ms()

    if state == States.S0_CALIBRATE:
        # Optional: sample line thresholds stationary
        state = States.S1_FOLLOW_LINE

    elif state == States.S1_FOLLOW_LINE:
        # End-of-line obstacle detection starts the distance-only part of the run.
        if sensors.ultrasonic_cm() <= OBSTACLE_CM:
            state = States.S2_DETECT_OBSTACLE
            motors.stop()
        else:
            direction = sensors.line_direction()

            if direction is None:
                # If this happens before the obstacle zone, judges may apply a line penalty.
                if time.ticks_diff(now, _last_line_seen_ms) > LINE_LOST_MS:
                    motors.stop()
            elif direction < 0:
                _last_line_seen_ms = now
                motors.turn_left(0.32)
            elif direction > 0:
                _last_line_seen_ms = now
                motors.turn_right(0.32)
            else:
                _last_line_seen_ms = now
                motors.forward(0.35)

    elif state == States.S2_DETECT_OBSTACLE:
        # Turn or align here if needed, then leave the line toward the box.
        _box_entry_start_ms = now
        state = States.S3_ENTER_BOX

    elif state == States.S3_ENTER_BOX:
        # Starter behavior: drive straight into the boxed area for a short time.
        motors.forward(0.30)
        if time.ticks_diff(now, _box_entry_start_ms) > BOX_ENTRY_MAX_MS:
            state = States.S4_MANUAL_MAZE
            motors.stop()

    elif state == States.S4_MANUAL_MAZE:
        # The maze is driven manually through the robot control app.
        # Implement app command reads for your Pico setup, then map commands to motors.
        cmd = sensors.app_command()
        motors.apply_app_command(cmd)

    elif state == States.S5_FINISH:
        motors.stop()
        break

    elif state == States.ABORT:
        motors.stop()
        break

    time.sleep_ms(20)
