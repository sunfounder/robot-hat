#!/usr/bin/env python3
from .basic import _Basic_class
import RPi.GPIO as GPIO


class Pin(_Basic_class):
    """Pin manipulation class"""

    OUT = GPIO.OUT
    """Pin mode output"""
    IN = GPIO.IN
    """Pin mode input"""
    IRQ_FALLING = GPIO.FALLING
    """Pin interrupt falling"""
    IRQ_RISING = GPIO.RISING
    """Pin interrupt falling"""
    IRQ_RISING_FALLING = GPIO.BOTH
    """Pin interrupt both rising and falling"""
    PULL_UP = GPIO.PUD_UP
    """Pin internal pull up"""
    PULL_DOWN = GPIO.PUD_DOWN
    """Pin internal pull down"""
    PULL_NONE = None
    """Pin internal pull none"""

    _dict = {
        "D0":  17,
        "D1":   4,  # Changed
        "D2":  27,
        "D3":  22,
        "D4":  23,
        "D5":  24,
        "D6":  25,  # Removed
        "D7":   4,  # Removed
        "D8":   5,  # Removed
        "D9":   6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW":  25,  # Changed
        "USER": 25,
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST":  5,  # Changed
        "CE": 8,
    }

    def __init__(self, pin, mode=None, pull=None, *args, **kwargs):
        """
        Initialize a pin

        :param pin: pin number of Raspberry Pi
        :type pin: int/str
        :param mode: pin mode(IN/OUT)
        :type mode: int
        :param pull: pin pull up/down(PUD_UP/PUD_DOWN/PUD_NONE)
        :type pull: int
        """
        super().__init__(*args, **kwargs)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        if isinstance(pin, str):
            if pin not in self.dict().keys():
                raise ValueError(
                    f'Pin should be in {self._dict.keys()}, not "{pin}"')
            self._board_name = pin
            self._pin = self.dict()[pin]
        elif isinstance(pin, int):
            if pin not in self.dict().values():
                raise ValueError(
                    f'Pin should be in {self._dict.values()}, not "{pin}"')
            self._board_name = {i for i in self._dict if self._dict[i] == pin}
            self._pin = pin
        else:
            raise ValueError(
                f'Pin should be in {self._dict.keys()}, not "{pin}"')
        self._value = 0
        self.setup(mode, pull=pull)
        self._info("Pin init finished.")

    def setup(self, mode, pull=None):
        """
        Setup the pin

        :param mode: pin mode(IN/OUT)
        :type mode: int
        :param pull: pin pull up/down(PUD_UP/PUD_DOWN/PUD_NONE)
        :type pull: int
        """
        self._pull = pull
        self._mode = mode
        if mode != None:
            if pull != None:
                GPIO.setup(self._pin, mode, pull_up_down=pull)
            else:
                GPIO.setup(self._pin, mode)

    def dict(self, _dict=None):
        """
        Set/get the pin dictionary

        :param _dict: pin dictionary, leave it empty to get the dictionary
        :type _dict: dict
        :return: pin dictionary
        :rtype: dict
        """
        if _dict == None:
            return self._dict
        else:
            if not isinstance(_dict, dict):
                raise ValueError(
                    f'Argument should be a pin dictionary like {{"my pin": ezblock.Pin.cpu.GPIO17}}, not {_dict}')
            self._dict = _dict

    def __call__(self, value):
        """
        Set/get the pin value

        :param value: pin value, leave it empty to get the value(0/1)
        :type value: int
        :return: pin value(0/1)
        :rtype: int
        """
        return self.value(value)

    def value(self, value=None):
        """
        Set/get the pin value

        :param value: pin value, leave it empty to get the value(0/1)
        :type value: int
        :return: pin value(0/1)
        :rtype: int
        """
        if value == None:
            if self._mode in [None, self.OUT]:
                self.setup(self.IN)
            result = GPIO.input(self._pin)
            self._debug(f"read pin {self._pin}: {result}")
            return result
        else:
            if self._mode in [None, self.IN]:
                self.setup(self.OUT)
            GPIO.output(self._pin, value)
            return value

    def on(self):
        """
        Set pin on(high)

        :return: pin value(1)
        :rtype: int
        """
        return self.value(1)

    def off(self):
        """
        Set pin off(low)

        :return: pin value(0)
        :rtype: int
        """
        return self.value(0)

    def high(self):
        """
        Set pin high(1)

        :return: pin value(1)
        :rtype: int
        """
        return self.on()

    def low(self):
        """
        Set pin low(0)

        :return: pin value(0)
        :rtype: int
        """
        return self.off()

    def irq(self, handler=None, trigger=None, bouncetime=200):
        """
        Set the pin interrupt

        :param handler: interrupt handler callback function
        :type handler: function
        :param trigger: interrupt trigger(RISING, FALLING, RISING_FALLING)
        :type trigger: int
        :param bouncetime: interrupt bouncetime in miliseconds
        :type bouncetime: int
        """
        self.setup(self.IN)
        GPIO.add_event_detect(self._pin, trigger,
                              callback=handler, bouncetime=bouncetime)

    def name(self):
        """
        Get the pin name

        :return: pin name
        :rtype: str
        """
        return f"GPIO{self._pin}"
