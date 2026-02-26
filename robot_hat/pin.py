#!/usr/bin/env python3
from .basic import _Basic_class
import lgpio
from .device import PIN

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
    """Pin interrupt rising"""
    IRQ_RISING_FALLING = 0x23
    """Pin interrupt both rising and falling"""

    _dict = PIN

    _chip = None

    def __init__(self, pin, mode=None, pull=None, active_state:bool=None, *args, **kwargs):
        """
        Initialize a pin

        :param pin: pin number of Raspberry Pi
        :type pin: int/str
        :param mode: pin mode(IN/OUT)
        :type mode: int
        :param pull: pin pull up/down(PUD_UP/PUD_DOWN/PUD_NONE)
        :type pull: int
        :param active_state: active state of pin,  
                            If True, when the hardware pin state is HIGH, the software pin is HIGH. 
                            If False, the input polarity is reversed
        :type active_state: bool or None
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

        # initialize lgpio chip
        if Pin._chip is None:
            Pin._chip = lgpio.gpiochip_open(0)

        # setup
        self._value = 0
        self._irq_handler = None
        self._irq_callback_id = None
        self._irq_trigger = None
        self._bouncetime = 200
        self._last_irq_time = 0
        self.setup(mode, pull, active_state)
        self._info("Pin init finished.")

    def close(self):
        if self._irq_callback_id is not None and Pin._chip is not None:
            try:
                lgpio.gpio_free(Pin._chip, self._pin_num)
            except:
                pass
            self._irq_callback_id = None

    def deinit(self):
        self.close()

    def setup(self, mode, pull=None, active_state=None):
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

        # configure pull-up/down
        pull_mode = lgpio.SET_PULL_NONE
        if pull == self.PULL_UP:
            pull_mode = lgpio.SET_PULL_UP
        elif pull == self.PULL_DOWN:
            pull_mode = lgpio.SET_PULL_DOWN

        # set mode
        if mode in [None, self.OUT]:
            lgpio.gpio_claim_output(Pin._chip, self._pin_num, 0, pull_mode)
        else:
            lgpio.gpio_claim_input(Pin._chip, self._pin_num, pull_mode)

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
            result = lgpio.gpio_read(Pin._chip, self._pin_num)
            self._debug(f"read pin {self._pin_num}: {result}")
            return result
        else:
            if self._mode in [self.IN]:
                self.setup(self.OUT)
            if bool(value):
                value = 1
            else:
                value = 0
            lgpio.gpio_write(Pin._chip, self._pin_num, value)
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
        else:
            raise ValueError(
                f'pull param error, should be None, Pin.PULL_NONE, Pin.PULL_DOWN, Pin.PULL_UP'
            )

        # cancel old callback if exists
        if self._irq_callback_id is not None:
            self._irq_callback_id.cancel()
            self._irq_callback_id = None

        # configure pull-up/down
        pull_mode = lgpio.SET_PULL_NONE
        if pull == self.PULL_UP:
            pull_mode = lgpio.SET_PULL_UP
        elif pull == self.PULL_DOWN:
            pull_mode = lgpio.SET_PULL_DOWN

        # set input mode with pull
        lgpio.gpio_claim_input(Pin._chip, self._pin_num, pull_mode)

        # store handler and trigger
        self._irq_handler = handler
        self._irq_trigger = trigger
        self._bouncetime = bouncetime

        # define edge
        edge = lgpio.BOTH_EDGES
        if trigger == self.IRQ_FALLING:
            edge = lgpio.FALLING_EDGE
        elif trigger == self.IRQ_RISING:
            edge = lgpio.RISING_EDGE

        # define callback function and store it to prevent garbage collection
        def _irq_callback(chip, gpio, level, tick):
            import time
            current_time = time.time() * 1000
            if current_time - self._last_irq_time < self._bouncetime:
                return
            self._last_irq_time = current_time

            # call handler
            self._irq_handler()

        self._irq_callback_func = _irq_callback

        # set up callback
        self._irq_callback_id = lgpio.callback(Pin._chip, self._pin_num, edge, self._irq_callback_func)

    def name(self):
        """
        Get the pin name

        :return: pin name
        :rtype: str
        """
        return f"GPIO{self._pin_num}"
