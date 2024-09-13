#!/usr/bin/env python3
import math
from .i2c import I2C

timer = [{"arr": 1}] * 7

class PWM(I2C):
    """Pulse width modulation (PWM)"""

    REG_CHN = 0x20
    """Channel register prefix"""
    REG_PSC = 0x40
    """Prescaler register prefix"""
    REG_ARR = 0x44
    """Period registor prefix"""
    REG_PSC2 = 0x50
    """Prescaler register prefix"""
    REG_ARR2 = 0x54
    """Period registor prefix"""

    ADDR = [0x14, 0x15, 0x16]

    CLOCK = 72000000.0
    """Clock frequency"""

    def __init__(self, channel, address=None, *args, **kwargs):
        """
        Initialize PWM

        :param channel: PWM channel number(0-19/P0-P19)
        :type channel: int/str
        """
        if address is None:
            super().__init__(self.ADDR, *args, **kwargs)
        else:
            super().__init__(address, *args, **kwargs)

        if isinstance(channel, str):
            if channel.startswith("P"):
                channel = int(channel[1:])
            else:
                raise ValueError(
                    f'PWM channel should be between [P0, P19], not "{channel}"')
        if isinstance(channel, int):
            if channel > 19 or channel < 0:
                raise ValueError(
                    f'channel must be in range of 0-19, not "{channel}"')

        self.channel = channel
        if channel < 16:
            self.timer = int(channel/4)
        elif channel == 16 or channel == 17:
            self.timer = 4
        elif channel == 18:
            self.timer = 5
        elif channel == 19:
            self.timer = 6

        self._pulse_width = 0
        self._freq = 50
        self.freq(50)

    def _i2c_write(self, reg, value):
        value_h = value >> 8
        value_l = value & 0xff
        self.write([reg, value_h, value_l])

    def freq(self, freq=None):
        """
        Set/get frequency, leave blank to get frequency

        :param freq: frequency(0-65535)(Hz)
        :type freq: float
        :return: frequency
        :rtype: float
        """
        if freq == None:
            return self._freq

        self._freq = int(freq)
        # [prescaler,arr] list
        result_ap = []
        # accuracy list
        result_acy = []
        # middle value for equal arr prescaler
        st = int(math.sqrt(self.CLOCK/self._freq))
        # get -5 value as start
        st -= 5
        # prevent negetive value
        if st <= 0:
            st = 1
        for psc in range(st, st+10):
            arr = int(self.CLOCK/self._freq/psc)
            result_ap.append([psc, arr])
            result_acy.append(abs(self._freq-self.CLOCK/psc/arr))
        i = result_acy.index(min(result_acy))
        psc = result_ap[i][0]
        arr = result_ap[i][1]
        self._debug(f"prescaler: {psc}, period: {arr}")
        self.prescaler(psc)
        self.period(arr)

    def prescaler(self, prescaler=None):
        """
        Set/get prescaler, leave blank to get prescaler

        :param prescaler: prescaler(0-65535)
        :type prescaler: int
        :return: prescaler
        :rtype: int
        """
        if prescaler == None:
            return self._prescaler

        self._prescaler = round(prescaler)
        self._freq = self.CLOCK/self._prescaler/timer[self.timer]["arr"]
        if self.timer < 4:
            reg = self.REG_PSC + self.timer
        else:
            reg = self.REG_PSC2 + self.timer - 4
        self._debug(f"Set prescaler to: {self._prescaler}")
        self._i2c_write(reg, self._prescaler-1)

    def period(self, arr=None):
        """
        Set/get period, leave blank to get period

        :param arr: period(0-65535)
        :type arr: int
        :return: period
        :rtype: int
        """
        global timer
        if arr == None:
            return timer[self.timer]["arr"]

        timer[self.timer]["arr"] = round(arr)
        self._freq = self.CLOCK/self._prescaler/timer[self.timer]["arr"]

        if self.timer < 4:
            reg = self.REG_ARR + self.timer
        else:
            reg = self.REG_ARR2 + self.timer - 4

        self._debug(f"Set arr to: {timer[self.timer]['arr']}")
        self._i2c_write(reg, timer[self.timer]["arr"])

    def pulse_width(self, pulse_width=None):
        """
        Set/get pulse width, leave blank to get pulse width

        :param pulse_width: pulse width(0-65535)
        :type pulse_width: float
        :return: pulse width
        :rtype: float
        """
        if pulse_width == None:
            return self._pulse_width

        self._pulse_width = int(pulse_width)
        reg = self.REG_CHN + self.channel
        self._i2c_write(reg, self._pulse_width)

    def pulse_width_percent(self, pulse_width_percent=None):
        """
        Set/get pulse width percentage, leave blank to get pulse width percentage

        :param pulse_width_percent: pulse width percentage(0-100)
        :type pulse_width_percent: float
        :return: pulse width percentage
        :rtype: float
        """
        global timer
        if pulse_width_percent == None:
            return self._pulse_width_percent

        self._pulse_width_percent = pulse_width_percent
        temp = self._pulse_width_percent / 100.0
        # print(temp)
        pulse_width = temp * timer[self.timer]["arr"]
        self.pulse_width(pulse_width)


def test():
    import time
    p = PWM(0, debug_level='debug')
    p.period(1000)
    p.prescaler(10)
    # p.pulse_width(2048)
    while True:
        for i in range(0, 4095, 10):
            p.pulse_width(i)
            print(i)
            time.sleep(1/4095)
        time.sleep(1)
        for i in range(4095, 0, -10):
            p.pulse_width(i)
            print(i)
            time.sleep(1/4095)
        time.sleep(1)


def test2():
    p = PWM("P0", debug_level='debug')
    p.pulse_width_percent(50)
    # while True:
    #     p.pulse_width_percent(50)


if __name__ == '__main__':
    test2()
