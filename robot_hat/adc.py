#!/usr/bin/env python3
from .i2c import I2C

class ADC(I2C):
    """
    Analog to digital converter
    """
    ADDR=0x14

    def __init__(self, chn):
        """
        Analog to digital converter

        :param chn: channel number (0-7/A0-A7)
        :type chn: int/str
        """
        super().__init__()
        if isinstance(chn, str):
            # If chn is a string, assume it's a pin name, remove A and convert to int
            if chn.startswith("A"):
                chn = int(chn[1:])
            else:
                raise ValueError("ADC channel should be between [A0, A7], not {0}".format(chn))
        # Make sure channel is between 0 and 7
        if chn < 0 or chn > 7:
            self._error('Incorrect channel range')
        chn = 7 - chn
        # Convert to Register value
        self.chn = chn | 0x10
        self.reg = 0x40 + self.chn
        # self.bus = smbus.SMBus(1)

    def read(self):
        """
        Read the ADC value

        :return: ADC value(0-4095)
        :rtype: int
        """
        # Write register address
        self._debug(f"Write 0x{self.chn:02X} to 0x{self.ADDR:02X}")
        self.send([self.chn, 0, 0], self.ADDR)

        # Read MSB value
        self._debug(f"Read from 0x{self.ADDR:02X}")
        value_h = self.recv(1, self.ADDR)[0]

        # Read LSB value
        self._debug(f"Read from 0x{self.ADDR:02X}")
        value_l = self.recv(1, self.ADDR)[0]

        # Combine MSB and LSB
        value = (value_h << 8) + value_l
        self._debug(f"Read value: {value}")
        return value

    def read_voltage(self):
        """
        Read the ADC value and convert to voltage

        :return: Voltage value(0-3.3(V))
        :rtype: float
        """
        # Read ADC value
        value = self.read()
        # Convert to voltage
        voltage = value * 3.3 / 4095
        self._debug(f"Read voltage: {voltage}")
        return voltage
