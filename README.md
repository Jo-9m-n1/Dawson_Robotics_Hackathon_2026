# Starter - Pico2 Navigation Challenge

Educational starter for Dawson Robotics Hackathon 2026.

## Quick start

1. Read [TOOLCHAIN.md](./TOOLCHAIN.md).
2. Flash MicroPython on the Pico 2.
3. Copy the Yahboom `pico_car.py` library file to the Pico.
4. Copy `main.py`, `states.py`, `sensors.py`, and `motors.py` to the Pico.
5. Tune thresholds in `states.py` (`LINE_LOST_MS`, `OBSTACLE_CM`, etc.) on the practice course.

## Kit assumptions

This starter is written for the Yahboom Pico Robot kit:

- Motors use `pico_car().Car_Run(...)`, `Car_Back(...)`, and `Car_Stop()`.
- The four tracking sensors are GPIO 2, 3, 4, and 5 from left to right.
- On the tracking sensor, black reads `0` and white reads `1`.
- Ultrasonic distance uses `ultrasonic().Distance_accurate()`.
- The YahboomRobot app uses Bluetooth UART on TX 16 and RX 17 at 9600 baud.
- Basic app commands are two bytes: `A#` forward, `B#` back, `C#` left, `D#` right, and `0#` stop.

## Challenge states

- `S1_FOLLOW_LINE`: follow the opening line.
- `S2_DETECT_OBSTACLE`: use ultrasonic distance to detect the end-of-line obstacle.
- `S3_ENTER_BOX`: leave the line and enter the boxed area.
- `S4_MANUAL_MAZE`: navigate toward the finish using manual app control.
- `S5_FINISH`: stop at the finish.

## License

MIT - see [LICENSE](./LICENSE).
