#!/usr/bin/env python3
from .i2c import I2C

class ADC_NEW_HAT(I2C):
    """
    Analog to digital converter
    """
    ADDR = [0x17]

    REG_ADC_START = 0x10
    REG_ADC_END = 0x19
    CHANNEL_NUM = 5

    def __init__(self, i2c, chn):
        """
        Analog to digital converter

        :param chn: channel number (0-4/A0-A4)
        :type chn: int/str
        """
        if isinstance(chn, str):
            # If chn is a string, assume it's a pin name, remove A and convert to int
            if chn.startswith("A"):
                chn = int(chn[1:])
            else:
                raise ValueError(
                    f'ADC channel should be between [A0, A4], not "{chn}"')
        # Make sure channel is between 0 and 4
        if chn < 0 or chn > self.CHANNEL_NUM - 1:
            raise ValueError(
                f'ADC channel should be between [0, 4], not "{chn}"')
        self.channel = chn
        self.reg_addr = self.REG_ADC_START + chn*2
        self.i2c = i2c

    def read(self):
        """
        Read the ADC value

        :return: ADC value(0-4095)
        :rtype: int
        """
        val_h, val_l = self.i2c._read_i2c_block_data(self.reg_addr, 2)
        val = (val_h << 8) | val_l
        return val

class ADC_OLD_HAT(I2C):
    """
    Analog to digital converter
    """
    ADDR = [0x14, 0x15, 0x16]

    REG_ADC_START = 0x10
    REG_ADC_END = 0x17
    CHANNEL_NUM = 8

    def __init__(self, i2c, chn):
        """
        Analog to digital converter

        :param chn: channel number (0-7/A0-A7)
        :type chn: int/str
        """
        if isinstance(chn, str):
            # If chn is a string, assume it's a pin name, remove A and convert to int
            if chn.startswith("A"):
                chn = int(chn[1:])
            else:
                raise ValueError(
                    f'ADC channel should be between [A0, A7], not "{chn}"')
        # Make sure channel is between 0 and 7
        if chn < 0 or chn > self.CHANNEL_NUM - 1:
            raise ValueError(
                f'ADC channel should be between [0, 7], not "{chn}"')
        chn = 7 - chn
        self.channel = chn
        self.reg_addr = self.REG_ADC_START + chn
        self.i2c = i2c

    def read(self):
        """
        Read the ADC value

        :return: ADC value(0-4095)
        :rtype: int
        """
        # Write register address
        self.i2c.write([self.chn, 0, 0])
        # Read values
        msb, lsb = self.i2c.read(2)

        # Combine MSB and LSB
        value = (msb << 8) + lsb
        self._debug(f"Read value: {value}")
        return value


class ADC(I2C):
    def __init__(self, chn, address=None, *args, **kwargs):
         
        if address is not None:
            super().__init__(address, *args, **kwargs)
            self.i2c_addr = self.address
        else:
            ADDR = ADC_OLD_HAT.ADDR + ADC_NEW_HAT.ADDR
            # print(ADDR, ADC_OLD_HAT.ADDR, ADC_NEW_HAT.ADDR)
            super().__init__(ADDR, *args, **kwargs)
            self.i2c_addr = self.address

        if self.i2c_addr in ADC_OLD_HAT.ADDR:
            self._adc = ADC_OLD_HAT(self, chn)
        elif self.i2c_addr in ADC_NEW_HAT.ADDR:
            self._adc = ADC_NEW_HAT(self, chn)
        else:
            raise ValueError("Invalid I2C address")

    def read(self):
        return self._adc.read()

    def read_voltage(self):
        """
        Read the ADC voltage

        :return: ADC voltage(0-3.3V)
        :rtype: float
        """
        val = self._adc.read()
        voltage = val * 3.3 / 4095
        return voltage
