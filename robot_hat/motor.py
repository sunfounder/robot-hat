#!/usr/bin/env python3
from .pwm import PWM
from .pin import Pin

class Motor():
    """Motor"""
    PERIOD = 4095
    PRESCALER = 10
    DEFAULT_FREQ = 100 # Hz
    """Default PWM frequency"""
    DEFAULT_MAX = 100 # %
    """Default maximum motor power"""
    DEFAULT_MIN = 0 # %
    """Default minimum motor power"""

    MOTOR_PINS = {
        'M1': ['P13', 'D4'],
        'M2': ['P12', 'D5'],
    }

    def __init__(self, motor: str, freq=DEFAULT_FREQ, min=DEFAULT_MIN, max=DEFAULT_MAX, is_reversed=False) -> None:
        self.motor = motor

        self.pwm = PWM(self.MOTOR_PINS[self.motor][0])
        self.dir = Pin(self.MOTOR_PINS[self.motor][1], Pin.OUT)

        self.freq = freq
        self.max = max
        self.min = min
        self._is_reverse = is_reversed

        self.pwm.freq(self.freq)
        self.pwm.pulse_width_percent(0)

        self._power = 0

    def power(self, power=None):
        """
        Get or set motor power

        Args:
            power (float): Motor power(-100.0~100.0)
        """
        if power is None:
            return self._power

        dir = 1 if power > 0 else 0
        if self._is_reverse:
            # dir = dir + 1 & 1
            dir = dir ^ 1 # XOR
        power = abs(power)
        if power != 0:
            power = max(self.min, min(self.max, power))

        self.pwm.pulse_width_percent(power)
        self.dir.value(dir)

    def set_is_reverse(self, is_reverse):
        """
        Set motor is reversed or not

        :param is_reverse: True or False
        :type is_reverse: bool
        """
        self._is_reverse = is_reverse

    def stop(self) -> None:
        """Stop motor"""
        self.power(0)
