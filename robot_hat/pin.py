#!/usr/bin/env python3
from .basic import _Basic_class
import gpiozero  # https://gpiozero.readthedocs.io/en/latest/installing.html
from gpiozero import OutputDevice, InputDevice, Button


class Pin(_Basic_class):
    """Pin manipulation class"""

    OUT = 0x01
    """Pin mode output"""
    IN = 0x02
    """Pin mode input"""

    PULL_UP = 0x11
    """Pin internal pull up"""
    PULL_DOWN = 0x12
    """Pin internal pull down"""
    PULL_NONE = None
    """Pin internal pull none"""

    IRQ_FALLING = 0x21
    """Pin interrupt falling"""
    IRQ_RISING = 0x22
    """Pin interrupt falling"""
    IRQ_RISING_FALLING = 0x23
    """Pin interrupt both rising and falling"""

    _dict = {
        "D0": 17,
        "D1": 4,  # Changed
        "D2": 27,
        "D3": 22,
        "D4": 23,
        "D5": 24,
        "D6": 25,  # Removed
        "D7": 4,  # Removed
        "D8": 5,  # Removed
        "D9": 6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW": 25,  # Changed
        "USER": 25,
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST": 5,  # Changed
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

        # parse pin
        if isinstance(pin, str):
            if pin not in self.dict().keys():
                raise ValueError(
                    f'Pin should be in {self._dict.keys()}, not "{pin}"')
            self._board_name = pin
            self._pin_num = self.dict()[pin]
        elif isinstance(pin, int):
            if pin not in self.dict().values():
                raise ValueError(
                    f'Pin should be in {self._dict.values()}, not "{pin}"')
            self._board_name = {i for i in self._dict if self._dict[i] == pin}
            self._pin_num = pin
        else:
            raise ValueError(
                f'Pin should be in {self._dict.keys()}, not "{pin}"')
        # setup
        self._value = 0
        self.gpio = None
        self.setup(mode, pull)
        self._info("Pin init finished.")

    def close(self):
        self.gpio.close()

    def deinit(self):
        self.gpio.close()
        self.gpio.pin_factory.close()

    def setup(self, mode, pull=None):
        """
        Setup the pin

        :param mode: pin mode(IN/OUT)
        :type mode: int
        :param pull: pin pull up/down(PUD_UP/PUD_DOWN/PUD_NONE)
        :type pull: int
        """
        # check mode
        if mode in [None, self.OUT, self.IN]:
            self._mode = mode
        else:
            raise ValueError(
                f'mode param error, should be None, Pin.OUT, Pin.IN')
        # check pull
        if pull in [self.PULL_NONE, self.PULL_DOWN, self.PULL_UP]:
            self._pull = pull
        else:
            raise ValueError(
                f'pull param error, should be None, Pin.PULL_NONE, Pin.PULL_DOWN, Pin.PULL_UP'
            )
        #
        if self.gpio != None:
            if self.gpio.pin != None:
                self.gpio.close()
        #
        if mode in [None, self.OUT]:
            self.gpio = OutputDevice(self._pin_num)
        else:
            if pull in [self.PULL_UP]:
                self.gpio = InputDevice(self._pin_num, pull_up=True)
            else:
                self.gpio = InputDevice(self._pin_num, pull_up=False)

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
                    f'Argument should be a pin dictionary like {{"my pin": ezblock.Pin.cpu.GPIO17}}, not {_dict}'
                )
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

    def value(self, value: bool = None):
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
            result = self.gpio.value
            self._debug(f"read pin {self.gpio.pin}: {result}")
            return result
        else:
            if self._mode in [self.IN]:
                self.setup(self.OUT)
            if bool(value):
                value = 1
                self.gpio.on()
            else:
                value = 0
                self.gpio.off()
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

    def irq(self, handler, trigger, bouncetime=200, pull=None):
        """
        Set the pin interrupt

        :param handler: interrupt handler callback function
        :type handler: function
        :param trigger: interrupt trigger(RISING, FALLING, RISING_FALLING)
        :type trigger: int
        :param bouncetime: interrupt bouncetime in miliseconds
        :type bouncetime: int
        """
        # check trigger
        if trigger not in [
                self.IRQ_FALLING, self.IRQ_RISING, self.IRQ_RISING_FALLING
        ]:
            raise ValueError(
                f'trigger param error, should be None, Pin.IRQ_FALLING, Pin.IRQ_RISING, Pin.IRQ_RISING_FALLING'
            )

        # check pull
        if pull in [self.PULL_NONE, self.PULL_DOWN, self.PULL_UP]:
            self._pull = pull
            if pull == self.PULL_UP:
                _pull_up = True
            else:
                _pull_up = False
        else:
            raise ValueError(
                f'pull param error, should be None, Pin.PULL_NONE, Pin.PULL_DOWN, Pin.PULL_UP'
            )
        #
        pressed_handler = None
        released_handler = None
        #
        if not isinstance(self.gpio, Button):
            if self.gpio != None:
                self.gpio.close()
            self.gpio = Button(pin=self._pin_num,
                               pull_up=_pull_up,
                               bounce_time=float(bouncetime / 1000))
            self._bouncetime = bouncetime
        else:
            if bouncetime != self._bouncetime:
                pressed_handler = self.gpio.when_pressed
                released_handler = self.gpio.when_released
                self.gpio.close()
                self.gpio = Button(pin=self._pin_num,
                                   pull_up=_pull_up,
                                   bounce_time=float(bouncetime / 1000))
                self._bouncetime = bouncetime
        #
        if trigger in [None, self.IRQ_FALLING]:
            pressed_handler = handler
        elif trigger in [self.IRQ_RISING]:
            released_handler = handler
        elif trigger in [self.IRQ_RISING_FALLING]:
            pressed_handler = handler
            released_handler = handler
        #
        if pressed_handler is not None:
            self.gpio.when_pressed = pressed_handler
        if released_handler is not None:
            self.gpio.when_released = released_handler

    def name(self):
        """
        Get the pin name

        :return: pin name
        :rtype: str
        """
        return f"GPIO{self._pin_num}"
