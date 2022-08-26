#!/usr/bin/env python3
from .basic import _Basic_class
import time

class Servo(_Basic_class):
    """Servo motor class"""
    MAX_PW = 2500
    MIN_PW = 500
    _freq = 50
    def __init__(self, pwm, debug="error"):
        """
        Initialize the servo motor class
        
        :param pwm: PWM object
        :type pwm: robot_hat.PWM
        :param debug: debug level(critical, error, warning, info, debug)
        :type debug: str
        """
        super().__init__()
        self.debug = debug
        self.pwm = pwm
        self.pwm.period(4095)
        prescaler = int(float(self.pwm.CLOCK) /self.pwm._freq/self.pwm.period())
        self.pwm.prescaler(prescaler)

    def angle(self, angle):
        """
        Set the angle of the servo motor
        
        :param angle: angle(-90~90)
        :type angle: float
        """
        if not (isinstance(angle, int) or isinstance(angle, float)):
            raise ValueError("Angle value should be int or float value, not %s"%type(angle))
        if angle < -90:
            angle = -90
        if angle > 90:
            angle = 90
        self._debug(f"Set angle to: {angle}")
        High_level_time = self.map(angle, -90, 90, self.MIN_PW, self.MAX_PW)
        self._debug(f"High_level_time: {High_level_time}")
        pwr =  High_level_time / 20000
        self._debug(f"pulse width rate: {pwr}")
        value = int(pwr*self.pwm.period())
        self._debug(f"pulse width value: {value}")
        self.pwm.pulse_width(value)

    def set_pwm(self,pwm_value):
        """
        Set the pulse width of the servo motor
        
        :param pwm_value: pulse width(500~2500)
        :type pwm_value: float
        """
        if pwm_value > self.MAX_PW:
            pwm_value =  self.MAX_PW 
        if pwm_value < self.MIN_PW:
            pwm_value = self.MIN_PW

        self.pwm.pulse_width(pwm_value)

def test():
    from robot_hat import PWM
    print("Test")
    p = PWM("P0")
    s0 = Servo(p)
    s0.debug = "debug"
    s0.angle(90)
    
if __name__ == "__main__":
    test()