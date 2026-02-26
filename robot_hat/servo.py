#!/usr/bin/env python3
from .pwm import PWM
from .utils import mapping, constrain
from typing import Optional


class Servo(PWM):
    """ Servo motor class

    Args:
        channel (int/str): PWM channel number(0-14/P0-P14)
        offset (float, optional): offset value(-20.0~20.0), leave it None to use default offset, defaults to 0.0
        min (float, optional): minimum angle(-90~90), leave it None to use default min angle, defaults to -90
        max (float, optional): maximum angle(-90~90), leave it None to use default max angle, defaults to 90
        *args: Pass to :class:`fusion_hat.pwm.PWM`
        **kwargs: Pass to :class:`fusion_hat.pwm.PWM`
    """

    MAX_PW = 2500
    MIN_PW = 500
    FREQ = 50
    PERIOD = 4095

    def __init__(self,channel, *args,
        offset: Optional[float]=0.0,
        min: Optional[float]=-90,
        max: Optional[float]=90,
        **kwargs):
        """
        Initialize the servo motor class

        :param channel: PWM channel number(0-14/P0-P14)
        :type channel: int/str
        """
        super().__init__(channel, *args, **kwargs)
        self.period(self.PERIOD)
        prescaler = self.CLOCK / self.FREQ / self.PERIOD
        self.prescaler(prescaler)
        self._offset = offset
        self._angle = 0
        self._min = min
        self._max = max

    def offset(self, offset: Optional[float]=None) -> float:
        """ Set the offset of the servo motor

        Args:
            offset (float, optional): offset value(-20.0~20.0), leave it None to get the offset value, defaults to None

        Returns:
            float: offset value(-20.0~20.0) if offset is None, else None
        """
        if offset is None:
            return self._offset
        offset = constrain(offset, -20.0, 20.0)
        self._offset = offset
        return self._offset

    def angle(self, angle: Optional[float|int]=None) -> float:
        """
        Set the angle of the servo motor

        Args:
            angle (float|int, optional): angle(-90~90), leave it None to get the angle value, defaults to None

        Returns:
            float: angle(-90~90) if angle is None, else None
        """
        if angle is None:
            return self._angle
        angle = constrain(angle, self._min, self._max)
        self._angle = angle
        calibrated_angle = angle + self._offset
        self._debug(f"Set angle to: {calibrated_angle}")
        self.set_raw_angle(calibrated_angle)
        return self._angle

    def set_raw_angle(self, angle: float) -> None:
        """ Set the angle of the servo motor

        Args:
            angle (float): angle(-90~90)
        """
        angle = constrain(angle, -90, 90)
        pulse_width = mapping(angle, -90, 90, self.MIN_PW, self.MAX_PW)
        pulse_width = int(pulse_width)
        self._debug(f"Pulse width: {pulse_width}")
        self.pulse_width_time(pulse_width)

    def pulse_width_time(self, pulse_width_time: float) -> None:
        """
        Set the pulse width of the servo motor

        Args:
            pulse_width_time (float): pulse width time(500~2500)
        """
        pulse_width_time = constrain(pulse_width_time, self.MIN_PW, self.MAX_PW)
        pwr = pulse_width_time / 20000
        self._debug(f"pulse width rate: {pwr}")
        value = int(pwr * self.PERIOD)
        self._debug(f"pulse width value: {value}")
        self.pulse_width(value)
