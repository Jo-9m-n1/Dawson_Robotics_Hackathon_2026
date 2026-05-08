"""Tuning values for the Pico line-following car."""


class States:
    S0_CALIBRATE = 0
    S1_FOLLOW_LINE = 1
    S2_DETECT_OBSTACLE = 2
    S3_ENTER_BOX = 3
    S4_MANUAL_MAZE = 4
    S5_FINISH = 5
    ABORT = 99


# Yahboom tracking sensors usually read black tape as 0 and white floor as 1.
BLACK_VALUE = 0

# Keep obstacle/manual mode off while fixing line following.
ENABLE_OBSTACLE_DETECTION = False
OBSTACLE_CM = 15.0
OBSTACLE_CONFIRM_COUNT = 3
BOX_ENTRY_MAX_MS = 1800

# Speeds: fast on straight, slower but stronger on turns.
STRAIGHT_SPEED = 0.40
ANGLE_SPEED = 0.30

# Faster edge/corner turn. Both wheels still move forward, so it should not spin in place.
CORNER_INNER_SPEED = 0.32
CORNER_OUTER_SPEED = 0.70

# PD correction for normal line following.
KP = 0.090
KD = 0.025
MAX_CORRECTION = 0.24
LINE_DEADBAND = 0.18

# Error zones.
ANGLE_ERROR = 0.70
CORNER_ERROR = 1.35

# Re-enter the line gently after seeing black again.
REACQUIRE_MS = 180
REACQUIRE_SPEED = 0.28
REACQUIRE_CORRECTION = 0.18

# Lost-line recovery: stronger and longer reverse.
LOST_BACK_SPEED = 0.58
LOST_BACK_CURVE = 0.16
LINE_LOST_STOP_MS = 7000

# Motor settings.
MIN_MOTOR_SPEED = 0.20
MAX_MOTOR_SPEED = 0.92
LEFT_TRIM = 1.00
RIGHT_TRIM = 1.00

LOOP_DELAY_MS = 8
RUN_TIMEOUT_MS = 0
