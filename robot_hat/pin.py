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
        "BOARD_TYPE": 12,
    }

    _dict_1 = {
        "D0":  17,
        "D1":  18,
        "D2":  27,
        "D3":  22,
        "D4":  23,
        "D5":  24,
        "D6":  25,
        "D7":  4,
        "D8":  5,
        "D9":  6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21, 
        "SW":  19,
        "USER": 19,        
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST": 21,

    }

    _dict_2 = {
        "D0":  17,
        "D1":   4, # Changed
        "D2":  27,
        "D3":  22,
        "D4":  23,
        "D5":  24,
        "D6":  25, # Removed
        "D7":   4, # Removed
        "D8":   5, # Removed
        "D9":   6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,     
        "SW":  25, # Changed
        "USER": 25,
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST":  5, # Changed
    }

    def __init__(self, *value):
        """
        Initialize a pin
        
        :param pin: pin number of Raspberry Pi
        :type pin: int/str
        :param mode: pin mode(IN/OUT)
        :type mode: int
        :param pull: pin pull up/down(PUD_UP/PUD_DOWN/PUD_NONE)
        :type pull: int
        """
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.check_board_type()

        if len(value) > 0:
            pin = value[0]
        if len(value) > 1:
            mode = value[1]
        else:
            mode = None
        if len(value) > 2:
            setup = value[2]
        else:
            setup = None
        if isinstance(pin, str):
            try:
                self._board_name = pin
                self._pin = self.dict()[pin]
            except Exception as e:
                print(e)
                self._error('Pin should be in %s, not %s' % (self._dict.keys(), pin))
        elif isinstance(pin, int):
            self._pin = pin
        else:
            self._error('Pin should be in %s, not %s' % (self._dict.keys(), pin))
        self._value = 0
        self.init(mode, pull=setup)
        self._info("Pin init finished.")
        
    def check_board_type(self):
        type_pin = self.dict()["BOARD_TYPE"]
        GPIO.setup(type_pin, GPIO.IN)
        if GPIO.input(type_pin) == 0:
            self._dict = self._dict_1
        else:
            self._dict = self._dict_2

    def init(self, mode, pull=PULL_NONE):
        """
        Initialize the pin
        
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

    def dict(self, *_dict):
        """
        Set/get the pin dictionary
        
        :param _dict: pin dictionary, leave it empty to get the dictionary
        :type _dict: dict
        :return: pin dictionary
        :rtype: dict
        """
        if len(_dict) == 0:
            return self._dict
        else:
            if isinstance(_dict, dict):
                self._dict = _dict
            else:
                self._error(
                    'argument should be a pin dictionary like {"my pin": ezblock.Pin.cpu.GPIO17}, not %s' % _dict)

    def __call__(self, value):
        """
        Set/get the pin value
        
        :param value: pin value, leave it empty to get the value(0/1)
        :type value: int
        :return: pin value(0/1)
        :rtype: int
        """
        return self.value(value)

    def value(self, *value):
        """
        Set/get the pin value

        :param value: pin value, leave it empty to get the value(0/1)
        :type value: int
        :return: pin value(0/1)
        :rtype: int
        """
        if len(value) == 0:
            if self._mode in [None, self.OUT]:
                self.mode(self.IN)
            result = GPIO.input(self._pin)
            self._debug("read pin %s: %s" % (self._pin, result))
            return result
        else:
            value = value[0]
            if self._mode in [None, self.IN]:
                self.mode(self.OUT)
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

    def mode(self, *value):
        """
        Set/get the pin mode, leave argument to get the mode
        
        :param mode: pin mode(IN/OUT)
        :type mode: int
        :param pull: pin pull up/down(PUD_UP/PUD_DOWN/PUD_NONE)
        :type pull: int
        :return: tuple of pin mode and pull up/down(mode, pull)
        :rtype: tuple
        """
        if len(value) > 0:
            self._mode = value[0]
            if len(value) == 1:
                GPIO.setup(self._pin, self._mode)
            elif len(value) == 2:
                self._pull = value[1]
                GPIO.setup(self._pin, self._mode, self._pull)
        return (self._mode, self._pull)

    def pull(self):
        """
        Get the pin pull up/down
        
        :return: pin pull up/down(PUD_UP/PUD_DOWN/PUD_NONE)
        :rtype: int
        """
        return self._pull

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
        self.mode(self.IN)
        GPIO.add_event_detect(self._pin, trigger, callback=handler, bouncetime=bouncetime)

    def name(self):
        """
        Get the pin name

        :return: pin name
        :rtype: str
        """
        return "GPIO%s"%self._pin
