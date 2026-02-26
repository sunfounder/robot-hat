#!/usr/bin/env python3
from .pin import Pin
from .pwm import PWM
from .adc import ADC
from .i2c import I2C
import time
from typing import Union, List, Tuple
import threading
from .utils import constrain

class Ultrasonic():
    """
    Ultrasonic sensor module.

    Args:
        trig (Pin): Trigger pin object.
        echo (Pin): Echo pin object.
        timeout (float, optional): Timeout duration in seconds. Default is 0.02.

    Raises:
        TypeError: If trig or echo is not a Pin object.
    """
    SOUND_SPEED = 343.3 # ms
    """Sound speed in meters per second."""

    def __init__(self, trig, echo, timeout=0.02):
        """
        Initialize Ultrasonic sensor module.

        :param trig: Trigger pin object.
        :type trig: fusion_hat.Pin
        :param echo: Echo pin object.
        :type echo: fusion_hat.Pin
        :param timeout: Timeout duration in seconds. Default is 0.02.
        :type timeout: float
        """
        if not isinstance(trig, Pin):
            raise TypeError("trig must be fusion_hat.Pin object")
        if not isinstance(echo, Pin):
            raise TypeError("echo must be fusion_hat.Pin object")

        self.timeout = timeout

        trig.close()
        echo.close()
        self.trig = Pin(trig._pin_num)
        self.echo = Pin(echo._pin_num, mode=Pin.IN, pull=Pin.PULL_DOWN)

        self.thread_read_interval = 0.02
        self.thread = None
        self.thread_started = False
        self.thread_value = -1

    def read_raw(self):
        """
        Read raw distance value from ultrasonic sensor.

        Returns:
            float: Distance in centimeters. Returns -1 if timeout occurs,
                -2 if pulse start or end is 0, or any other error.
        """
        self.trig.off()
        time.sleep(0.001)
        self.trig.on()
        time.sleep(0.00001)
        self.trig.off()

        pulse_end = 0
        pulse_start = 0
        timeout_start = time.time()

        while self.echo.value() == 0:
            pulse_start = time.time()
            if pulse_start - timeout_start > self.timeout:
                return -1
        while self.echo.value() == 1:
            pulse_end = time.time()
            if pulse_end - timeout_start > self.timeout:
                return -1
        if pulse_start == 0 or pulse_end == 0:
            return -2

        during = pulse_end - pulse_start
        cm = round(during * self.SOUND_SPEED / 2 * 100, 2)
        return cm

    def read_with_retry(self, times=10):
        """
        Read distance value with retry mechanism.

        Args:
            times (int, optional): Number of retry attempts. Default is 10.

        Returns:
            float: Distance in centimeters. Returns -1 if all attempts fail.
        """
        for _ in range(times):
            value = self.read_raw()
            if value > 0:
                return value
        return -1

    def read(self):
        """
        Read distance value.

        Returns:
            float: Distance in centimeters. Returns -1 if thread is running,
                otherwise returns the last read value.
        """
        if self.thread is not None and self.thread_started:
            return self.thread_value
        else:
            return self.read_with_retry()

    def thread_read_loop(self):
        """
        Thread loop for reading distance value periodically.
        """
        while self.thread_started:
            self.thread_value = self.read_with_retry()
            time.sleep(self.thread_read_interval)

    def start_thread(self, interval=0.01):
        """
        Start the thread for reading distance value periodically.

        Args:
            interval (float, optional): Interval duration in seconds. Default is 0.01.
        """
        if self.thread is None:
            self.thread_started = True
            self.thread_read_interval = interval
            self.thread = threading.Thread(target=self.thread_read_loop, daemon=True)
            self.thread.start()
    
    def stop_thread(self):
        """
        Stop the thread for reading distance value.
        """
        self.thread_started = False
        if self.thread is not None:
            self.thread.join()
            self.thread = None

class ADXL345(I2C):
    """ADXL345 modules"""

    X = 0
    """X"""
    Y = 1
    """Y"""
    Z = 2
    """Z"""
    ADDR =  0x53
    _REG_DATA_X = 0x32  # X-axis data 0 (6 bytes for X/Y/Z)
    _REG_DATA_Y = 0x34  # Y-axis data 0 (6 bytes for X/Y/Z)
    _REG_DATA_Z = 0x36  # Z-axis data 0 (6 bytes for X/Y/Z)
    _REG_POWER_CTL = 0x2D  # Power-saving features control
    _AXISES = [_REG_DATA_X, _REG_DATA_Y, _REG_DATA_Z]

    def __init__(self, *args, address: int = ADDR, bus: int = 1, **kwargs):
        """
        Initialize ADXL345

        :param address: address of the ADXL345
        :type address: int
        """
        super().__init__(address=address, bus=bus, *args, **kwargs)
        self.address = address

    def read(self, axis: int = None) -> Union[float, List[float]]:
        """
        Read an axis from ADXL345

        :param axis: read value(g) of an axis, ADXL345.X, ADXL345.Y or ADXL345.Z, None for all axis
        :type axis: int
        :return: value of the axis, or list of all axis
        :rtype: float/list
        """
        if axis is None:
            return [self._read(i) for i in range(3)]
        else:
            return self._read(axis)

    def _read(self, axis: int) -> float:
        raw_2 = 0
        result = super().read()
        data = (0x08 << 8) + self._REG_POWER_CTL
        if result:
            self.write(data)
        self.mem_write(0, 0x31)
        self.mem_write(8, 0x2D)
        raw = self.mem_read(2, self._AXISES[axis])
        # 第一次读的值总是为0，所以多读取一次
        self.mem_write(0, 0x31)
        self.mem_write(8, 0x2D)
        raw = self.mem_read(2, self._AXISES[axis])
        if raw[1] >> 7 == 1:

            raw_1 = raw[1] ^ 128 ^ 127
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

    def __init__(self, r_pin: PWM, g_pin: PWM, b_pin: PWM, common: int = 1):
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

    def color(self, color: Union[str, Tuple[int, int, int], List[int], int]):
        """
        Write color to RGB LED

        :param color: color to write, hex string starts with "#", 24-bit int or tuple of (red, green, blue)
        :type color: str/int/tuple/list
        """
        if not isinstance(color, (str, int, tuple, list)):
            raise TypeError("color must be str, int, tuple or list")
        if isinstance(color, str):
            color = color.strip("#")
            color = int(color, 16)
        if isinstance(color, (tuple, list)):
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

    def __init__(self, buzzer: Union[PWM, Pin]):
        """
        Initialize buzzer

        :param pwm: PWM object for passive buzzer or Pin object for active buzzer
        :type pwm: robot_hat.PWM/robot_hat.Pin
        """
        if not isinstance(buzzer, (PWM, Pin)):
            raise TypeError(
                "buzzer must be robot_hat.PWM or robot_hat.Pin object")
        self.buzzer = buzzer
        self.buzzer.off()

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

    def freq(self, freq: float):
        """Set frequency of passive buzzer

        :param freq: frequency of buzzer, use Music.NOTES to get frequency of note
        :type freq: int/float
        :raise TypeError: if set to active buzzer
        """
        if isinstance(self.buzzer, Pin):
            raise TypeError("freq is not supported for active buzzer")
        self.buzzer.freq(freq)

    def play(self, freq: float, duration: float = None):
        """
        Play freq

        :param freq: freq to play, you can use Music.note() to get frequency of note
        :type freq: float
        :param duration: duration of each note, in seconds, None means play continuously
        :type duration: float
        :raise TypeError: if set to active buzzer
        """
        if isinstance(self.buzzer, Pin):
            raise TypeError("play is not supported for active buzzer")
        self.freq(freq)
        self.on()
        if duration is not None:
            time.sleep(duration/2)
            self.off()
            time.sleep(duration/2)


class Grayscale_Module(object):
    """3 channel Grayscale Module"""

    LEFT = 0
    """Left Channel"""
    MIDDLE = 1
    """Middle Channel"""
    RIGHT = 2
    """Right Channel"""

    REFERENCE_DEFAULT = [1000]*3

    def __init__(self, pin0: ADC, pin1: ADC, pin2: ADC, reference: int = None):
        """
        Initialize Grayscale Module

        :param pin0: ADC object or int for channel 0
        :type pin0: robot_hat.ADC/int
        :param pin1: ADC object or int for channel 1
        :type pin1: robot_hat.ADC/int
        :param pin2: ADC object or int for channel 2
        :type pin2: robot_hat.ADC/int
        :param reference: reference voltage
        :type reference: 1*3 list, [int, int, int]
        """
        self.pins = (pin0, pin1, pin2)
        for i, pin in enumerate(self.pins):
            if not isinstance(pin, ADC):
                raise TypeError(f"pin{i} must be robot_hat.ADC")
        self._reference = self.REFERENCE_DEFAULT

    def reference(self, ref: list = None) -> list:
        """
        Get Set reference value

        :param ref: reference value, None to get reference value
        :type ref: list
        :return: reference value
        :rtype: list
        """
        if ref is not None:
            if isinstance(ref, list) and len(ref) == 3:
                self._reference = ref
            else:
                raise TypeError("ref parameter must be 1*3 list.")
        return self._reference

    def read_status(self, datas: list = None) -> list:
        """
        Read line status

        :param datas: list of grayscale datas, if None, read from sensor
        :type datas: list
        :return: list of line status, 0 for white, 1 for black
        :rtype: list
        """
        if self._reference == None:
            raise ValueError("Reference value is not set")
        if datas == None:
            datas = self.read()
        return [0 if data > self._reference[i] else 1 for i, data in enumerate(datas)]

    def read(self, channel: int = None) -> list:
        """
        read a channel or all datas

        :param channel: channel to read, leave empty to read all. 0, 1, 2 or Grayscale_Module.LEFT, Grayscale_Module.CENTER, Grayscale_Module.RIGHT 
        :type channel: int/None
        :return: list of grayscale data
        :rtype: list
        """
        if channel == None:
            return [self.pins[i].read() for i in range(3)]
        else:
            return self.pins[channel].read()


class LineTracker(object):
    """Line Tracker"""
    LINE_DIFF = 200
    CLIFF_THRESHOLD = 120

    LINE_REFERENCE_UPDATE_RATE = 0.05

    def __init__(self, left: ADC, middle: ADC, right: ADC, slopes: list = None, offsets: list = None):
        """
        Initialize Line Tracker
        
        Args:
            left (ADC): ADC object for left sensor
            middle (ADC): ADC object for middle sensor
            right (ADC): ADC object for right sensor
        """
        self.left = left
        self.middle = middle
        self.right = right
        self.sensors = [left, middle, right]
        if slopes is None:
            slopes = [1, 1, 1]
        if offsets is None:
            offsets = [0, 0, 0]
        self.slopes = slopes
        self.offsets = offsets
        self.line_background_reference = 1000
        self.line_reference = 200
        self.cliff_threshold = self.CLIFF_THRESHOLD

    def read_channel(self, channel: int, raw: bool = False) -> int:
        """
        Read a channel

        Args:
            channel (int): channel to read, 0, 1, 2 or Grayscale_Module.LEFT, Grayscale_Module.CENTER, Grayscale_Module.RIGHT
            raw (bool): if True, return raw data, False to return calibrated data

        Returns:
            int: grayscale data
        """
        value = self.sensors[channel].read()
        if not raw:
            value = value * self.slopes[channel] + self.offsets[channel]
            value = round(value)
        return value

    def calibrate_data(self, data: list) -> list:
        """
        Calibrate grayscale data
        Args:
            data (list): list of grayscale data
        Returns:
            list: list of calibrated grayscale data
        """
        calibrated = []
        for i in range(3):
            value = data[i] * self.slopes[i] + self.offsets[i]
            value = int(round(value))
            calibrated.append(value)
        return calibrated

    def read(self, raw: bool = False) -> list:
        """
        Read line status

        Args:
            raw (bool): if True, return raw data, False to return calibrated data

        Returns:
            list: list of line status, 0 for white, 1 for black
        """
        return [self.read_channel(i, raw) for i in range(3)]

    def is_on_cliff(self, data: list = None) -> bool:
        """
        Check if robot is on cliff

        Args:
            data (list): list of grayscale data, leave empty to read from sensor

        Returns:
            bool: True if robot is on cliff, False otherwise
        """
        if data is None:
            left, middle, right = self.read()
        else:
            left, middle, right = data
        return left < self.cliff_threshold or middle < self.cliff_threshold or right < self.cliff_threshold

    def get_line_position(self, data: list = None):
        """
        Get line position

        Args:
            data (list): list of grayscale data, leave empty to read from sensor

        Returns:
            float: line position, -1 for left, 0 for center, 1 for right
        """

        if data is None:
            data = self.read()

        L, M, R = data

        # Calculate weight (grayscale value lower, weight higher)
        w_L = (self.line_background_reference - L) / (self.line_background_reference - self.line_reference)
        w_M = (self.line_background_reference - M) / (self.line_background_reference - self.line_reference)
        w_R = (self.line_background_reference - R) / (self.line_background_reference - self.line_reference)

        # contrain weight to 0-1
        w_L = constrain(w_L, 0, 1)
        w_M = constrain(w_M, 0, 1)
        w_R = constrain(w_R, 0, 1)

        # Calculate sum of weights
        sum_w = w_L + w_M + w_R

        # Return 0 if the difference is too small
        if sum_w < 0.2:
            return 0.0
        
        # Return 0 if the robot is not on the line
        if not self.is_on_line(data=data):
            return 0.0

        # Calculate position
        if (w_L >= 0.2 and w_M < 0.2 and w_R < 0.2):
            position = w_L - 1.8
        elif (w_R >= 0.2 and w_M < 0.2 and w_L < 0.2):
            position = 1.8 - w_R
        else:
            position = ( w_R -w_L )/ sum_w
            # Update background reference and line reference only at least two sensor is on line
            self.update_line_background_reference(data)
            self.update_line_reference(data)

        position = position / 1.5
        position = constrain(position, -1, 1)
        position = round(position, 2)
        return position

    def is_on_line(self, data: list = None) -> bool:
        """
        Check if robot is on line

        Args:
            data (list): list of grayscale data, leave empty to read from sensor

        Returns:
            bool: True if robot is on line, False otherwise
        """
        if data is None:
            data = self.read()

        if self.is_on_cliff(data=data):
            return False
        
        min_value = min(data)
        max_value = max(data)

        return max_value - min_value > self.LINE_DIFF

    def set_calibration_data(self, slopes: list, offsets: list):
        """
        Set calibration data
        Args:
            slopes (list): list of slopes
            offsets (list): list of offsets
        """
        self.slopes = slopes
        self.offsets = offsets

    def set_cliff_threshold(self, threshold: int):
        """
        Set cliff threshold
        Args:
            threshold (int): cliff threshold
        """
        self.cliff_threshold = threshold

    def get_calibration_data(self):
        """
        Get calibration data
        Returns:
            tuple: tuple of slopes and offsets
        """
        return self.slopes, self.offsets

    def calibrate(self, light_data: list, dark_data: list):
        """
        Calibrate line tracker
        Args:
            light_data (list): list of light data
            dark_data (list): list of dark data
        """
        # Find the maximum grayscale value and its index
        max_grayscale = max(light_data)
        max_index = light_data.index(max_grayscale)
        # Calculate the other twe with linear formula y=ax+b
        slopes = []
        offsets = []
        for i in range(3):
            # Use Max Value as reference, so no need to calibrate it
            if i == max_index:
                slopes.append(1)
                offsets.append(0)
            else:
                x1 = dark_data[i]
                y1 = dark_data[max_index]
                x2 = light_data[i]
                y2 = light_data[max_index]
                if x2 - x1 <= 0 or y2 - y1 <= 0:
                    raise ValueError(f"Black value should be less than white value., light_data: {light_data}, dark_data: {dark_data}")
                a = (y2 - y1) / (x2 - x1)
                b = y1 - a * x1
                slopes.append(round(a, 2))
                offsets.append(round(b, 2))
        
        # Set calibration data
        self.set_calibration_data(slopes, offsets)
        return slopes, offsets

    def update_line_background_reference(self, current_values):
        """ Update the line background value """
        max_val = max(current_values)
        keep_rate = 1 - self.LINE_REFERENCE_UPDATE_RATE
        update_rate = self.LINE_REFERENCE_UPDATE_RATE
        self.line_background_reference = keep_rate * self.line_background_reference + update_rate * max_val

    def update_line_reference(self, current_values):
        """ Update the line reference value """
        min_val = min(current_values)
        keep_rate = 1 - self.LINE_REFERENCE_UPDATE_RATE
        update_rate = self.LINE_REFERENCE_UPDATE_RATE
        self.line_reference = keep_rate * self.line_reference + update_rate * min_val
