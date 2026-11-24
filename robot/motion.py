"""Open-loop moves calibrated on the floor of the arena.

The robot has no wheel encoders: distances and angles are converted into
motor-on durations measured experimentally.

Usage (on the Raspberry Pi):
    from robot.motors import MotorDriver
    from robot.motion import move_forward, turn
    motors = MotorDriver()
    move_forward(motors, 1.0)   # 1 m straight ahead
    turn(motors, -90)           # quarter turn to the left
"""
import time

FORWARD_SPEED = 50  # duty cycle, percent
FORWARD_SPEED_M_S = 0.33  # measured ground speed at FORWARD_SPEED
TURN_SPEED = 30  # duty cycle, percent
TURN_PULSE_S = 0.05  # duration of one rotation pulse (and of the pause after it)
DEGREES_PER_PULSE = 4.6  # measured rotation per pulse


def move_forward(motors, distance):
    """Drive straight for a distance in metres, then stop."""
    motors.move(forward=FORWARD_SPEED, turn=0)
    time.sleep(distance / FORWARD_SPEED_M_S)
    motors.stop()


def turn(motors, angle):
    """Rotate on the spot by an angle in degrees (positive = right) with short pulses."""
    direction = 1 if angle > 0 else -1
    for _ in range(int(abs(angle) / DEGREES_PER_PULSE)):
        motors.move(forward=0, turn=TURN_SPEED * direction)
        time.sleep(TURN_PULSE_S)
        motors.stop()
        time.sleep(TURN_PULSE_S)
