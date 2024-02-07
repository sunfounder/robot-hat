#!/usr/bin/env python3
from .i2c import I2C


class ADC(I2C):
    """
    Analog to digital converter
    """
    ADDR = [0x14, 0x15]

    def __init__(self, chn, address=None, *args, **kwargs):
        """
        Analog to digital converter

        :param chn: channel number (0-7/A0-A7)
        :type chn: int/str
        """
        if address is not None:
            super().__init__(address, *args, **kwargs)
        else:
            super().__init__(self.ADDR, *args, **kwargs)
        self._debug(f'ADC device address: 0x{self.address:02X}')

        if isinstance(chn, str):
            # If chn is a string, assume it's a pin name, remove A and convert to int
            if chn.startswith("A"):
                chn = int(chn[1:])
            else:
                raise ValueError(
                    f'ADC channel should be between [A0, A7], not "{chn}"')
        # Make sure channel is between 0 and 7
        if chn < 0 or chn > 7:
            raise ValueError(
                f'ADC channel should be between [0, 7], not "{chn}"')
        chn = 7 - chn
        # Convert to Register value
        self.chn = chn | 0x10

    def read(self):
        """
        Read the ADC value

        :return: ADC value(0-4095)
        :rtype: int
        """
        # Write register address
        self.write([self.chn, 0, 0])
        # Read values
        msb, lsb = super().read(2)

        # Combine MSB and LSB
        value = (msb << 8) + lsb
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
