#!/usr/bin/env python3
import smbus, math
from .i2c import I2C

timer = [{"arr": 0}] * 4

class PWM(I2C):
    """Pulse width modulation (PWM)"""

    REG_CHN = 0x20
    """Channel register prefix"""
    REG_FRE = 0x30
    """Frequency register prefix"""
    REG_PSC = 0x40
    """Prescaler register prefix"""
    REG_ARR = 0x44
    """Period registor prefix"""

    ADDR = 0x14

    CLOCK = 72000000
    """Clock frequency"""

    def __init__(self, channel, debug="critical"):
        """
        Initialize PWM
        
        :param channel: PWM channel number(0-14/P0-P14)
        :type channel: int/str
        :param debug: debug level(critical, error, warning, info, debug)
        :type debug: str
        """
        super().__init__()
        if isinstance(channel, str):
            if channel.startswith("P"):
                channel = int(channel[1:])
                if channel > 14:
                    raise ValueError("channel must be in range of 0-14")
            else:
                raise ValueError("PWM channel should be between [P0, P11], not {0}".format(channel))
        try:
            self.send(0x2C, self.ADDR)
            self.send(0, self.ADDR)
            self.send(0, self.ADDR)
        except IOError:
            self.ADDR = 0x15

        self.debug = debug
        self._debug("PWM address: {:02X}".format(self.ADDR))
        self.channel = channel
        self.timer = int(channel/4)
        self.bus = smbus.SMBus(1)
        self._pulse_width = 0
        self._freq = 50
        self.freq(50)

    def i2c_write(self, reg, value):
        value_h = value >> 8
        value_l = value & 0xff
        self._debug("i2c write: [0x%02X, 0x%02X, 0x%02X, 0x%02X]"%(self.ADDR, reg, value_h, value_l))
        self.send([reg, value_h, value_l], self.ADDR)

    def freq(self, *freq):
        """
        Set/get frequency, leave blank to get frequency
        
        :param freq: frequency(0-65535)(Hz)
        :type freq: float
        :return: frequency
        :rtype: float
        """
        if len(freq) == 0:
            return self._freq
        else:
            self._freq = int(freq[0])
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
            for psc in range(st,st+10):
                arr = int(self.CLOCK/self._freq/psc)
                result_ap.append([psc, arr])
                result_acy.append(abs(self._freq-self.CLOCK/psc/arr))
            i = result_acy.index(min(result_acy))
            psc = result_ap[i][0]
            arr = result_ap[i][1]
            self._debug("prescaler: %s, period: %s"%(psc, arr))
            self.prescaler(psc)
            self.period(arr)

    def prescaler(self, *prescaler):
        """
        Set/get prescaler, leave blank to get prescaler
        
        :param prescaler: prescaler(0-65535)
        :type prescaler: float
        :return: prescaler
        :rtype: float
        """
        if len(prescaler) == 0:
            return self._prescaler
        else:
            self._prescaler = int(prescaler[0]) - 1
            reg = self.REG_PSC + self.timer
            self._debug("Set prescaler to: %s"%self._prescaler)
            self.i2c_write(reg, self._prescaler)

    def period(self, *arr):
        """
        Set/get period, leave blank to get period

        :param arr: period(0-65535)
        :type arr: float
        :return: period
        :rtype: float
        """
        global timer
        if len(arr) == 0:
            return timer[self.timer]["arr"]
        else:
            timer[self.timer]["arr"] = int(arr[0]) - 1
            reg = self.REG_ARR + self.timer
            self._debug("Set arr to: %s"%timer[self.timer]["arr"])
            self.i2c_write(reg, timer[self.timer]["arr"])

    def pulse_width(self, *pulse_width):
        """
        Set/get pulse width, leave blank to get pulse width
        
        :param pulse_width: pulse width(0-65535)
        :type pulse_width: float
        :return: pulse width
        :rtype: float
        """
        if len(pulse_width) == 0:
            return self._pulse_width
        else:
            self._pulse_width = int(pulse_width[0])
            reg = self.REG_CHN + self.channel
            self.i2c_write(reg, self._pulse_width)

    def pulse_width_percent(self, *pulse_width_percent):
        """
        Set/get pulse width percentage, leave blank to get pulse width percentage
        
        :param pulse_width_percent: pulse width percentage(0-100)
        :type pulse_width_percent: float
        :return: pulse width percentage
        :rtype: float
        """
        global timer
        if len(pulse_width_percent) == 0:
            return self._pulse_width_percent
        else:
            self._pulse_width_percent = pulse_width_percent[0]
            temp = self._pulse_width_percent / 100.0
            # print(temp)
            pulse_width = temp * timer[self.timer]["arr"]
            self.pulse_width(pulse_width)

        
def test():
    import time
    p = PWM(0)
    # p.debug = 'debug'
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
    p = PWM("P0")
    while True:
        p.pulse_width_percent(50)
        

if __name__ == '__main__':
    test2()