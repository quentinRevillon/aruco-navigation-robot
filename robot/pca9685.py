"""I2C driver of the PCA9685 16-channel PWM chip on the Waveshare Motor Driver HAT.

Adapted from the Waveshare example code
(https://www.waveshare.com/wiki/Motor_Driver_HAT). Raspberry Pi only (I2C bus 1).

Usage:
    from robot.pca9685 import PCA9685
    pwm = PCA9685(0x40)
    pwm.set_pwm_freq(50)
    pwm.set_duty_cycle(0, 40)   # channel 0 at 40 %
    pwm.set_level(1, 1)         # channel 1 fully on
"""
import math
import time

from smbus2 import SMBus

MODE1 = 0x00
PRESCALE = 0xFE
LED0_ON_L = 0x06
OSCILLATOR_HZ = 25_000_000


class PCA9685:
    """One PCA9685 chip at a given I2C address."""

    def __init__(self, address):
        """Open I2C bus 1 and reset the chip."""
        self.bus = SMBus(1)
        self.address = address
        self.write(MODE1, 0x00)

    def write(self, register, value):
        """Write an 8-bit value to a register."""
        self.bus.write_byte_data(self.address, register, value)

    def read(self, register):
        """Read an unsigned byte from a register."""
        return self.bus.read_byte_data(self.address, register)

    def set_pwm_freq(self, freq):
        """Set the PWM frequency of all channels, in Hz."""
        prescale = math.floor(OSCILLATOR_HZ / 4096 / freq - 1 + 0.5)
        old_mode = self.read(MODE1)
        self.write(MODE1, (old_mode & 0x7F) | 0x10)  # sleep
        self.write(PRESCALE, prescale)
        self.write(MODE1, old_mode)
        time.sleep(0.005)
        self.write(MODE1, old_mode | 0x80)  # restart

    def set_pwm(self, channel, on, off):
        """Set the 12-bit on and off ticks of one channel."""
        base = LED0_ON_L + 4 * channel
        for offset, value in enumerate([on & 0xFF, on >> 8, off & 0xFF, off >> 8]):
            self.write(base + offset, value & 0xFF)

    def set_duty_cycle(self, channel, percent):
        """Set the duty cycle of one channel, in percent."""
        self.set_pwm(channel, 0, int(percent * (4096 // 100)))

    def set_level(self, channel, value):
        """Drive one channel fully on (1) or off (0)."""
        self.set_pwm(channel, 0, 4095 if value == 1 else 0)
