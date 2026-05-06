"""
Hackathon state IDs — align names with published challenge (S0..S4).
"""


class States:
    S0_CALIBRATE = 0
    S1_FOLLOW_LINE = 1
    S2_DETECT_OBSTACLE = 2
    S3_ENTER_BOX = 3
    S4_MANUAL_MAZE = 4
    S5_FINISH = 5
    ABORT = 99


# Timeouts (ms) — tune on practice course; values match THINK frozen-spec draft
LINE_LOST_MS = 250
OBSTACLE_CM = 18.0
BOX_ENTRY_MAX_MS = 8000
STUCK_MS = 20000
