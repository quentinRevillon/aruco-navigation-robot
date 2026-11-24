"""Differential drive of the two DC motors through the Waveshare Motor Driver HAT.

Usage (on the Raspberry Pi):
    from robot.motors import MotorDriver
    motors = MotorDriver()
    motors.move(forward=40, turn=0)    # straight ahead at 40 % duty cycle
    motors.move(forward=0, turn=30)    # spin right on the spot
    motors.stop()
"""
from robot.pca9685 import PCA9685

LEFT, RIGHT = 0, 1
# (PWM channel, IN1 channel, IN2 channel) of each motor on the HAT
CHANNELS = {LEFT: (0, 1, 2), RIGHT: (5, 3, 4)}
LEFT_TRIM = 1.025  # the left motor is slightly slower: boost it to drive straight


class MotorDriver:
    """Owns the PCA9685 chip that powers both motors."""

    def __init__(self):
        """Initialise the PWM chip at its default HAT address (0x40, 50 Hz)."""
        self.pwm = PCA9685(0x40)
        self.pwm.set_pwm_freq(50)

    def run(self, motor, speed):
        """Run one motor at a signed speed.

        Args:
            motor: LEFT or RIGHT.
            speed: duty cycle in percent, negative to go backwards; saturated at 100.
        """
        pwm_channel, in1, in2 = CHANNELS[motor]
        self.pwm.set_duty_cycle(pwm_channel, min(abs(speed), 100))
        self.pwm.set_level(in1, int(speed < 0))
        self.pwm.set_level(in2, int(speed >= 0))

    def move(self, forward, turn):
        """Combine a forward speed and a turn speed (positive turns right), in percent."""
        self.run(LEFT, (forward + turn) * LEFT_TRIM)
        self.run(RIGHT, forward - turn)

    def stop(self):
        """Cut power to both motors."""
        self.pwm.set_duty_cycle(CHANNELS[LEFT][0], 0)
        self.pwm.set_duty_cycle(CHANNELS[RIGHT][0], 0)
