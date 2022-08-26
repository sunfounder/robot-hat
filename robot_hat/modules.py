#!/usr/bin/env python3
from .pin import Pin
from .pwm import PWM
from .adc import ADC
from .i2c import I2C
from math import sqrt
import time

class Ultrasonic():
    """UltraSonic modules"""
    def __init__(self, trig, echo, timeout=0.02):
        """
        Initialize the ultrasonic class
        
        :param trig: trig pin
        :type trig: robot_hat.Pin
        :param echo: echo pin
        :type echo: robot_hat.Pin
        :param timeout: timeout in seconds
        :type timeout: float
        :raise ValueError: if trig or echo is not a Pin object
        """
        if not isinstance(trig, Pin):
            raise TypeError("trig must be robot_hat.Pin object")
        if not isinstance(echo, Pin):
            raise TypeError("echo must be robot_hat.Pin object")
        self.trig = trig
        self.echo = echo
        self.timeout = timeout

    def _read(self):
        self.trig.low()
        time.sleep(0.01)
        self.trig.high()
        time.sleep(0.00001)
        self.trig.low()
        pulse_end = 0
        pulse_start = 0
        timeout_start = time.time()
        while self.echo.value()==0:
            pulse_start = time.time()
            if pulse_start - timeout_start > self.timeout:
                return -1
        while self.echo.value()==1:
            pulse_end = time.time()
            if pulse_end - timeout_start > self.timeout:
                return -1
        during = pulse_end - pulse_start
        cm = round(during * 340 / 2 * 100, 2)
        return cm

    def read(self, times=10):
        """
        Read distance in cm
        
        :param times: times try to read
        :type times: int
        :return: distance in cm, -1 if timeout
        :rtype: float
        """
        for _ in range(times):
            a = self._read()
            if a != -1:
                return a
        return -1
                
class DS18X20():
    """DS18X20 modules"""

    FAHRENHEIT = 0
    """Fahrenheit unit"""
    CELSIUS = 1
    """Celsius unit"""

    def __init__(self, *args, **kargs):
        """Initialize the DS18X20 class"""
        pass
    
    def scan(self):
        """
        Scan for DS18X20
        
        :return: list of roms
        :rtype: list
        """
        import os
        roms = []
        for rom in os.listdir('/sys/bus/w1/devices'):
            if rom.startswith('28-'):
                roms.append(rom)
        return roms

    def convert_temp(self):
        pass
    
    def read_temp(self, rom):
        """
        Read temperature from DS18X20 with specified rom
        
        :param rom: rom of the DS18X20
        :type rom: str
        :return: temperature in degree Celsius
        :rtype: float
        """
        location = '/sys/bus/w1/devices/' + rom + '/w1_slave'
        with open(location) as f:
            text = f.read()
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        temperature = temperature / 1000
        return temperature

    def read(self, unit=CELSIUS):
        """
        Read temperature from all DS18X20s
        
        :param unit: unit of temperature, DS18X20.FAHRENHEIT or DS18X20.CELSIUS
        :type unit: int
        :return: temperature if only one sensor detected, list of temperatures if multiple sensors detected
        :rtype: float/list
        :raise ValueError: if no sensor detected
        """
        self.roms = self.scan()
        self.convert_temp()
        temps = []
        for rom in self.roms:
            temp = self.read_temp(rom)
            if unit == self.FAHRENHEIT:
                temp = 32 + temp * 1.8
            temps.append(temp)
        if len(temps) == 0:
            raise IOError("Cannot detect any DS18X20, please check the connection")
        elif len(temps) == 1:
            temps = temps[0]
        return temps

class ADXL345():
    """ADXL345 modules"""

    X = 0
    """X"""
    Y = 1
    """Y"""
    Z = 2
    """Z"""
    _REG_DATA_X       = 0x32 # X-axis data 0 (6 bytes for X/Y/Z)
    _REG_DATA_Y       = 0x34 # Y-axis data 0 (6 bytes for X/Y/Z)
    _REG_DATA_Z       = 0x36 # Z-axis data 0 (6 bytes for X/Y/Z)
    _REG_POWER_CTL    = 0x2D # Power-saving features control
    _AXISES = [_REG_DATA_X, _REG_DATA_Y, _REG_DATA_Z]

    def __init__(self, address=0x53):  
        """
        Initialize ADXL345
        
        :param address: address of the ADXL345
        :type address: int
        """
        self.i2c = I2C()
        self.address = address

    def read(self, axis):
        """
        Read an axis from ADXL345
        
        :param axis: axis to read, ADXL345.X, ADXL345.Y or ADXL345.Z
        :type axis: int
        :return: value of the axis
        :rtype: int
        """
        raw_2 = 0
        result = self.i2c._i2c_read_byte(self.address)
        send = (0x08<< 8) + self._REG_POWER_CTL
        if result:
            self.i2c.send(send, self.address)
        self.i2c.mem_write(0, 0x53, 0x31, timeout=1000)
        self.i2c.mem_write(8, 0x53, 0x2D, timeout=1000)
        raw = self.i2c.mem_read(2, self.address, self._AXISES[axis])
        # 第一次读的值总是为0，所以多读取一次
        self.i2c.mem_write(0, 0x53, 0x31, timeout=1000)
        self.i2c.mem_write(8, 0x53, 0x2D, timeout=1000)
        raw = self.i2c.mem_read(2, self.address, self._AXISES[axis])
        if raw[1]>>7 == 1:
            
            raw_1 = raw[1]^128 ^ 127
            raw_2 = (raw_1 + 1) * -1
        else:
            raw_2 = raw[1]
        g = raw_2 << 8 | raw[0]
        value = g / 256.0
        return value

class RGB_LED():
    """Simple 3 pin RGB LED"""

    ANODE = 1
    """Common anode"""
    CATHODE = 0
    """Common cathode"""

    def __init__(self, r_pin, g_pin, b_pin, common=1):
        """
        Initialize RGB LED

        :param r_pin: PWM object for red
        :type r_pin: robot_hat.PWM
        :param g_pin: PWM object for green
        :type g_pin: robot_hat.PWM
        :param b_pin: PWM object for blue
        :type b_pin: robot_hat.PWM
        :param common: RGB_LED.ANODE or RGB_LED.CATHODE, default is ANODE
        :type common: int
        :raise ValueError: if common is not ANODE or CATHODE
        :raise TypeError: if r_pin, g_pin or b_pin is not PWM object
        """
        if not isinstance(r_pin, PWM):
            raise TypeError("r_pin must be robot_hat.PWM object")
        if not isinstance(g_pin, PWM):
            raise TypeError("g_pin must be robot_hat.PWM object")
        if not isinstance(b_pin, PWM):
            raise TypeError("b_pin must be robot_hat.PWM object")
        if common not in (self.ANODE, self.CATHODE):
            raise ValueError("common must be RGB_LED.ANODE or RGB_LED.CATHODE")
        self.r_pin = r_pin
        self.g_pin = g_pin
        self.b_pin = b_pin
        self.common = common
    
    def write(self, color):
        """
        Write color to RGB LED
        
        :param color: color to write, hex string starts with "#", 24-bit int or tuple of (red, green, blue)
        :type color: str/int/tuple
        """
        if not isinstance(color, (str, int, tuple, list)):
            raise TypeError("color must be str, int, tuple or list")
        if isinstance(color, str):
            color = color.strip("#")
            color = int(color, 16)
        if isinstance(color, (turtle, list)):
            r, g, b = color
        if isinstance(color, int):
            r = (color & 0xff0000) >> 16
            g = (color & 0x00ff00) >> 8
            b = (color & 0x0000ff) >> 0

        if self.common == self.ANODE:
            r = 255-r
            g = 255-g
            b = 255-b
        
        r = r / 255.0 * 100.0
        g = g / 255.0 * 100.0
        b = b / 255.0 * 100.0

        self.r_pin.pulse_width_percent(r)
        self.g_pin.pulse_width_percent(g)
        self.b_pin.pulse_width_percent(b)

class Buzzer():
    """Buzzer"""

    def __init__(self, buzzer):
        """
        Initialize buzzer

        :param pwm: PWM object for passive buzzer or Pin object for active buzzer
        :type pwm: robot_hat.PWM/robot_hat.Pin
        """
        if not isinstance(buzzer, (PWM, Pin)):
            raise TypeError("buzzer must be robot_hat.PWM or robot_hat.Pin object")
        self.buzzer = buzzer
    
    def on(self):
        """Turn on buzzer"""
        if isinstance(self.buzzer, PWM):
            self.buzzer.pulse_width_percent(50)
        elif isinstance(self.buzzer, Pin):
            self.buzzer.on()
    
    def off(self):
        """Turn off buzzer"""
        if isinstance(self.buzzer, PWM):
            self.buzzer.pulse_width_percent(0)
        elif isinstance(self.buzzer, Pin):
            self.buzzer.off()
    
    def freq(self, freq):
        """Set frequency of passive buzzer
        
        :param freq: frequency of buzzer, use Music.NOTES to get frequency of note
        :type freq: int/float
        :raise TypeError: if set to active buzzer
        """
        if isinstance(self.buzzer, Pin):
            raise TypeError("freq is not supported for active buzzer")
        self.buzzer.freq(freq)
    
    def play(self, freq, duration=None):
        """
        Play notes

        :param args: notes to play, see play_note for details
        :type args: str/int/float
        :param duration: duration of each note, in ms, None means play continuously
        :type duration: float
        :raise TypeError: if set to active buzzer
        """
        if isinstance(self.buzzer, Pin):
            raise TypeError("play is not supported for active buzzer")
        self.freq(freq)
        self.on()
        if duration is not None:
            time.sleep(duration/1000.0)
            self.off()
            time.sleep(duration/1000.0)

class Sound():
    """Sound sensor"""
    def __init__(self, adc):
        """
        Initialize sound sensor

        :param adc: ADC object for sound sensor
        :type adc: robot_hat.ADC
        :raise TypeError: if adc is not ADC object
        """
        if not isinstance(adc, ADC):
            raise TypeError("adc must be robot_hat.ADC object")
        self.sensor = adc
    
    def read_raw(self):
        """Read raw value of sound sensor"""
        return self.sensor.read()
    
    def read(self, times=50):
        """
        Read value of sound sensor

        :param times: times to average
        :type times: int
        :return: average value of sound sensor
        :rtype: float
        """
        value_list = []
        for _ in range(times):
            value = self.read_raw()
            value_list.append(value)
        value = sum(value_list)/times
        return value

class Joystick():
    """Joystick"""
    THRESHOLD = 2047 / sqrt(2)
    def __init__(self, x, y, btn):
        """
        Initialize joystick

        :param x: ADC object for X axis
        :type x: robot_hat.ADC
        :param y: ADC object for Y axis
        :type y: robot_hat.ADC
        :param btn: ADC object for button
        :type btn: robot_hat.Pin
        """
        if not isinstance(x, ADC):
            raise TypeError("x must be robot_hat.ADC object")
        if not isinstance(y, ADC):
            raise TypeError("y must be robot_hat.ADC object")
        if not isinstance(btn, ADC):
            raise TypeError("btn must be robot_hat.Pin object")
        self.pins = [x, y, btn]
        self.pins[2].init(self.pins[2].IN, pull=self.pins[2].PULL_UP)
        self.is_reversed = [False, False, False]

    @property
    def is_x_reversed(self):
        """is X axis reversed"""
        return self.is_reversed[0]
    @property
    def is_y_reversed(self):
        """is Y axis reversed"""
        return self.is_reversed[1]
    @property
    def is_z_reversed(self):
        """is Z axis reversed"""
        return self.is_reversed[2]

    @is_x_reversed.setter
    def is_x_reversed(self, value):
        if not isinstance(value, bool):
            raise ValueError("reversed value must be bool, not %s(%s)"%(value, type(value)))
        self.is_reversed[0] = value
    @is_y_reversed.setter
    def is_y_reversed(self, value):
        if not isinstance(value, bool):
            raise ValueError("reversed value must be bool, not %s(%s)"%(value, type(value)))
        self.is_reversed[1] = value
    @is_z_reversed.setter
    def is_z_reversed(self, value):
        if not isinstance(value, bool):
            raise ValueError("reversed value must be bool, not %s(%s)"%(value, type(value)))
        self.is_reversed[2] = value
    
    def read(self, axis):
        """
        Read an axis value of joystick
        
        :param axis: axis to read, use Joystick.X, Joystick.Y, Joystick.Z, Joystick.BTN to get axis
        :type axis: int
        :return: value of axis
        :rtype: int
        :raise ValueError: if axis is not in Joystick.X, Joystick.Y, Joystick.Z
        """
        if axis not in (Joystick.X, Joystick.Y, Joystick.Z, Joystick.BTN):
            raise ValueError("axis must be in Joystick.X, Joystick.Y, Joystick.Z")
        pin = self.pins[axis]
        if axis == 2:
            value = pin.value()
            if self.is_reversed[2]:
                value = value + 1 & 1
        else:
            value = pin.read() - 2047
            if self.is_reversed[axis]:
                value = - value
        return value

    def read_status(self):
        """
        Read status of joystick
        
        :return: status of joystick, home, left, right, up, down, pressed
        :rtype: str
        """
        state = ['home', 'up', 'down', 'left', 'right', 'pressed']
        i = 0
        if self.read(1) < -self.THRESHOLD: # Y
            i = 2       #down
        elif self.read(1) > self.THRESHOLD: # Y
            i = 1       #up
        elif self.read(0) < -self.THRESHOLD: # X
            i = 3       #left
        elif self.read(0) > self.THRESHOLD: # X
            i = 4       #right
        elif self.read(2) == 0: # Bt
            i = 5       # Button pressed
        else:
            i = 0
        return state[i]

class Grayscale_Module(object):
    """3 channel Grayscale Module"""
    def __init__(self, pin0, pin1, pin2, reference=1000):
        """
        Initialize Grayscale Module

        :param pin0: ADC object or int for channel 0
        :type pin0: robot_hat.ADC/int
        :param pin1: ADC object or int for channel 1
        :type pin1: robot_hat.ADC/int
        :param pin2: ADC object or int for channel 2
        :type pin2: robot_hat.ADC/int
        :param reference: reference voltage
        :type reference: int
        """
        if isinstance(pin0, ADC):
            self.chn_0 = pin0
        else:
            self.chn_0 = ADC(pin0)
        if isinstance(pin1, ADC):
            self.chn_1 = pin1
        else:
            self.chn_1 = ADC(pin1)
        if isinstance(pin2, ADC):
            self.chn_2 = pin2
        else:
            self.chn_2 = ADC(pin2)
        self.reference = reference

    def get_line_status(self, data):
        """
        Get line status

        :param data: list of grayscale data
        :type data: list
        :return: line status, stop, forward, backward, left, right
        :rtype: str
        """
        if data[0] > self.reference and data[1] > self.reference and data[2] > self.reference:
            return 'stop'
            
        elif data[1] <= self.reference:
            return 'forward'
        
        elif data[0] <= self.reference:
            return 'right'

        elif data[2] <= self.reference:
            return 'left'

    def get_grayscale_data(self):
        """
        Get grayscale data
        
        :return: list of grayscale data
        :rtype: list
        """
        adc_value_list = []
        adc_value_list.append(self.chn_0.read())
        adc_value_list.append(self.chn_1.read())
        adc_value_list.append(self.chn_2.read())
        return adc_value_list
