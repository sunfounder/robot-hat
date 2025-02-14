#!/usr/bin/env python3
import math
from .i2c import I2C

timer = [{"arr": 1} for _ in range(7)]

class PWM_NEW_HAT(I2C):

    ADDR = [0x17]
    CLOCK = 72000000.0

    # 3 timer2 for 12 channels
    REG_PSC_START = 0x40
    REG_PSC_END = 0x49

    REG_ARR_START = 0x50
    REG_ARR_END = 0x59

    REG_CCP_START = 0x60
    REG_CCP_END = 0x77

    CHANNEL_NUM = 12

    def __init__(self, channel, addr=ADDR[0]):
        """
        Initialize PWM

        :param channel: PWM channel number(0-11/P0-P11)
        :type channel: int/str
        """
        super().__init__(addr)
        print(f"PWM_NEW_HAT aaaaaaaaaaaaaaaaaaa {channel}")
        if isinstance(channel, str):
            if channel.startswith("P"):
                channel = int(channel[1:])
            else:
                raise ValueError(
                    f'PWM channel should be between [P0, P11], not "{channel}"')
        if isinstance(channel, int):
            if channel < 0 or channel > self.CHANNEL_NUM - 1:
                raise ValueError(
                    f'channel must be in range of 0-11, not "{channel}"')
        self.channel = channel

        if channel < 4:
            self.timer_index = 0
        elif channel < 8:
            self.timer_index = 1
        else:
            self.timer_index = 2

        self.psc_reg_addr = self.REG_PSC_START + self.timer_index
        self.arr_reg_addr = self.REG_ARR_START + self.timer_index
        self.ccp_reg_addr = self.REG_CCP_START + self.channel * 2
        self.psc = 0
        self.arr = 0
        self.ccp = 0
        self.duty_cycle = 0.0
        self._freq = 50
        self.freq(50)
        self.pulse_width(0)

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
        # Calculate arr and frequency errors
        psc_arr = []
        freq_errors = []
        # --- calculate the prescaler and period ---
        # frequency = CLOCK / (arr + 1) / (psc + 1)
        assumed_psc = int(math.sqrt(self.CLOCK/self._freq)) # assumed prescaler, start from square root
        assumed_psc -= 5
        if assumed_psc < 0:
            assumed_psc = 0
        # Calculate arr and frequency errors
        for psc in range(assumed_psc, assumed_psc+10):
            arr = int(self.CLOCK/self._freq/psc)
            psc_arr.append((psc, arr))
            freq_errors.append(abs(self._freq - self.CLOCK/psc/arr))
        # Find the best match
        best_match = freq_errors.index(min(freq_errors))
        psc, arr = psc_arr[best_match]
        self.psc = int(psc) - 1
        self.arr = int(arr) - 1
        self.prescaler(self.psc)
        self.period(self.arr)

    def prescaler(self, psc=None):
        """
        Set/get prescaler, leave blank to get prescaler

        :param psc: prescaler(0-65535)
        :type psc: int
        :return: prescaler
        :rtype: int
        """
        if psc == None:
            return self.psc

        self.psc = int(psc)
        self._freq = self.CLOCK/(self.psc+1)/(self.arr+1)
        psc_h = (self.psc >> 8) & 0xff
        psc_l = self.psc & 0xff
        data = [self.psc_reg_addr, psc_h, psc_l]
        self.write(data)

    def period(self, arr=None):
        """
        Set/get period, leave blank to get period

        :param arr: period(0-65535)
        :type arr: int
        :return: period
        :rtype: int
        """
        if arr == None:
            return self.arr

        self.arr = int(arr)
        self._freq = self.CLOCK/(self.psc+1)/(self.arr+1)
        self.duty_cycle = round(self.ccp / self.arr * 100, 2)
        arr_h = (self.arr >> 8) & 0xff
        arr_l = self.arr & 0xff
        data = [self.arr_reg_addr, arr_h, arr_l]
        self.write(data)

    def pulse_width(self, ccp=None):
        """
        Set/get pulse width, leave blank to get pulse width

        :param ccp: pulse width(0-65535)
        :type ccp: float
        :return: pulse width
        :rtype: float
        """
        if ccp == None:
            return self.ccp

        self.ccp = int(ccp)
        self.duty_cycle = round(self.ccp / self.arr * 100, 2)
        cpp_h = (self.ccp >> 8) & 0xff
        ccp_l = self.ccp & 0xff
        data = [self.ccp_reg_addr, cpp_h, ccp_l]
        self.write(data)

    def pulse_width_percent(self, duty_cycle=None):
        """
        Set/get pulse width percentage, leave blank to get pulse width percentage

        :param duty_cycle: pulse width percentage(0-100)
        :type duty_cycle: float
        :return: pulse width percentage
        :rtype: float
        """
        if duty_cycle == None:
            return duty_cycle

        self.duty_cycle = round(duty_cycle, 2)
        self.ccp = int(self.arr * duty_cycle / 100)
        cpp_h = (self.ccp >> 8) & 0xff
        ccp_l = self.ccp & 0xff
        data = [self.ccp_reg_addr, cpp_h, ccp_l]
        self.write(data)

class PWM_OLD_HAT():
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

    def __init__(self, channel, addr=ADDR[0]):
        """
        Initialize PWM

        :param channel: PWM channel number(0-19/P0-P19)
        :type channel: int/str
        """
        super().__init__(addr)
        print(f"PWM_OLD_HAT aaaaaaaaaaaaaaaaaaa {channel}")
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
            self.timer_index = int(channel/4)
        elif channel == 16 or channel == 17:
            self.timer_index = 4
        elif channel == 18:
            self.timer_index = 5
        elif channel == 19:
            self.timer_index = 6

        if self.timer_index < 4:
            self.psc_reg_addr = self.REG_PSC + self.timer_index
        else:
            self.psc_reg_addr = self.REG_PSC2 + self.timer_index - 4

        if self.timer_index < 4:
            self.arr_reg_addr = self.REG_ARR + self.timer_index
        else:
            self.arr_reg_addr = self.REG_ARR2 + self.timer_index - 4
        self.ccp_reg_addr = self.REG_CHN + self.channel

        self.psc = 0
        self.arr = 0
        self.ccp = 0
        self.duty_cycle = 0.0
        self._freq = 50
        self.freq(50)
        self.pulse_width(0)

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
        # Calculate arr and frequency errors
        psc_arr = []
        freq_errors = []
        # --- calculate the prescaler and period ---
        # frequency = CLOCK / (arr + 1) / (psc + 1)
        assumed_psc = int(math.sqrt(self.CLOCK/self._freq)) # assumed prescaler, start from square root
        assumed_psc -= 5
        if assumed_psc < 0:
            assumed_psc = 0
        # Calculate arr and frequency errors
        for psc in range(assumed_psc, assumed_psc+10):
            arr = int(self.CLOCK/self._freq/psc)
            psc_arr.append((psc, arr))
            freq_errors.append(abs(self._freq - self.CLOCK/psc/arr))
        # Find the best match
        best_match = freq_errors.index(min(freq_errors))
        psc, arr = psc_arr[best_match]
        self.psc = int(psc) - 1
        self.arr = int(arr) - 1
        self.prescaler(self.psc)
        self.period(self.arr)

    def prescaler(self, psc=None):
        """
        Set/get prescaler, leave blank to get prescaler

        :param psc: prescaler(0-65535)
        :type psc: int
        :return: prescaler
        :rtype: int
        """
        if psc == None:
            return self.psc

        self.psc = int(psc)
        self._freq = self.CLOCK/(self.psc+1)/(self.arr+1)
        psc_h = (self.psc >> 8) & 0xff
        psc_l = self.psc & 0xff
        data = [self.psc_reg_addr, psc_h, psc_l]
        self.write(data)

    def period(self, arr=None):
        """
        Set/get period, leave blank to get period

        :param arr: period(0-65535)
        :type arr: int
        :return: period
        :rtype: int
        """
        if arr == None:
            return self.arr

        self.arr = int(arr)
        self._freq = self.CLOCK/(self.psc+1)/(self.arr+1)
        self.duty_cycle = round(self.ccp / self.arr * 100, 2)
        arr_h = (self.arr >> 8) & 0xff
        arr_l = self.arr & 0xff
        data = [self.arr_reg_addr, arr_h, arr_l]
        self.write(data)

    def pulse_width(self, ccp=None):
        """
        Set/get pulse width, leave blank to get pulse width

        :param ccp: pulse width(0-65535)
        :type ccp: float
        :return: pulse width
        :rtype: float
        """
        if ccp == None:
            return self.ccp

        self.ccp = int(ccp)
        self.duty_cycle = round(self.ccp / self.arr * 100, 2)
        cpp_h = (self.ccp >> 8) & 0xff
        ccp_l = self.ccp & 0xff
        data = [self.ccp_reg_addr, cpp_h, ccp_l]
        self.write(data)

    def pulse_width_percent(self, duty_cycle=None):
        """
        Set/get pulse width percentage, leave blank to get pulse width percentage

        :param duty_cycle: pulse width percentage(0-100)
        :type duty_cycle: float
        :return: pulse width percentage
        :rtype: float
        """
        if duty_cycle == None:
            return duty_cycle

        self.duty_cycle = round(duty_cycle, 2)
        self.ccp = int(self.arr * duty_cycle / 100)
        cpp_h = (self.ccp >> 8) & 0xff
        ccp_l = self.ccp & 0xff
        data = [self.ccp_reg_addr, cpp_h, ccp_l]
        self.write(data)


_i2c = I2C(ADDR)
i2c_addr =  _i2c.a
if i2c_addr in PWM_OLD_HAT.ADDR:
    cls = PWM_OLD_HAT
    pwm = super().__new__(PWM_OLD_HAT)
    pwm.__init__(chn, i2c_addr)
    PWM = PWM_OLD_HAT
elif i2c_addr in PWM_NEW_HAT.ADDR:
    cls = PWM_NEW_HAT
    pwm = super().__new__(PWM_NEW_HAT)
    pwm.__init__(chn, i2c_addr)
    return pwm

class PWM():

    # def __new__(cls, chn, address=None, *args, **kwargs):
    #     if address is not None:
    #         i2c_addr = address
    #     else:
    #         ADDR = PWM_OLD_HAT.ADDR + PWM_NEW_HAT.ADDR
    #         _i2c = I2C(ADDR)
    #         i2c_addr =  _i2c.address

    #     if i2c_addr in PWM_OLD_HAT.ADDR:
    #         cls = PWM_OLD_HAT
    #         pwm = super().__new__(PWM_OLD_HAT)
    #         pwm.__init__(chn, i2c_addr)
    #         return pwm
    #     elif i2c_addr in PWM_NEW_HAT.ADDR:
    #         cls = PWM_NEW_HAT
    #         pwm = super().__new__(PWM_NEW_HAT)
    #         pwm.__init__(chn, i2c_addr)
    #         return pwm
    #     else:
    #         raise ValueError("Invalid address")

    def __init__(self, chn, address=None, *args, **kwargs):
        super().__init__(chn, address, *args, **kwargs)
        print('eeeeeeeeeeeeeeeeeeeeeee')

    # def freq(self, freq=None):
    #     return self._pwm.freq(freq)

    # def prescaler(self, psc=None):
    #     return self._pwm.prescaler(psc)

    # def period(self, arr=None):
    #     return self._pwm.period(arr)

    # def pulse_width(self, ccp=None):
    #     return self._pwm.pulse_width(ccp)

    # def pulse_width_percent(self, duty_cycle=None):
    #     return self._pwm.pulse_width_percent(duty_cycle)

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
