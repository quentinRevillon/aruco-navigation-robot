"""Emergency stop: cut power to both motors (e.g. after interrupting race.py).

Usage (on the Raspberry Pi):
    python stop_motors.py
"""
from robot.motors import MotorDriver

if __name__ == "__main__":
    MotorDriver().stop()
