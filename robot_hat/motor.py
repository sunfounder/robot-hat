#!/usr/bin/env python3
from .basic import _Basic_class
from .pwm import PWM
from .pin import Pin
from .filedb import fileDB

class Motor():
    """Motor"""
    PERIOD = 4095
    PRESCALER = 10
    DEFAULT_FREQ = 100 # Hz

    '''
    motor mode 1: (TC1508S)
                pin_a: PWM    pin_b: IO
    forward      pwm            1
    backward     pwm            0
    stop         0              x

    motor mode 2: (TC618S)
                pin_a: PWM    pin_b: PWM
    forward      pwm            0
    backward     0             pwm
    stop         0              0
    brake        1              1
    '''

    def __init__(self, pwm, dir, is_reversed=False, mode=None, freq=DEFAULT_FREQ):
        """
        Initialize a motor

        :param pwm: Motor speed control pwm pin
        :type pwm: robot_hat.pwm.PWM
        :param dir: Motor direction control pin
        :type dir: robot_hat.pin.Pin
        """
        if mode == None:
            from . import __device__
            self.mode = __device__.motor_mode
        else:
            self.mode = mode

        # mode 1: (TC1508S)
        if self.mode == 1:
            if not isinstance(pwm, PWM):
                raise TypeError("pin_a must be a class PWM")
            if not isinstance(dir, Pin):
                raise TypeError("pin_b must be a class Pin")

            self.pwm = pwm
            self.dir = dir
            self.freq = freq
            self.pwm.freq(self.freq)
            self.pwm.pulse_width_percent(0)
        # mode 2: (TC618S)
        elif self.mode == 2:
            if not isinstance(pwm, PWM):
                raise TypeError("pin_a must be a class PWM")
            if not isinstance(dir, PWM):
                raise TypeError("pin_b must be a class PWM")

            self.freq = freq
            self.pwm_a = pwm
            self.pwm_a.freq(self.freq)
            self.pwm_a.pulse_width_percent(0)
            self.pwm_b = dir
            self.pwm_b.freq(self.freq)
            self.pwm_b.pulse_width_percent(0)
        # unkowned mode
        else:
            raise ValueError("Unkown motors mode")

        self._speed = 0
        self._is_reverse = is_reversed

    def speed(self, speed=None):
        """
        Get or set motor speed

        :param speed: Motor speed(-100.0~100.0)
        :type speed: float
        """
        if speed is None:
            return self._speed

        dir = 1 if speed > 0 else 0
        if self._is_reverse:
            # dir = dir + 1 & 1
            dir = dir ^ 1 # XOR
        speed = abs(speed)

        # mode 1: (TC1508S)
        if self.mode == 1:
            self.pwm.pulse_width_percent(speed)
            self.dir.value(dir)
        # mode 2: (TC618S)
        elif self.mode ==2:
            if dir == 1:
                self.pwm_a.pulse_width_percent(speed)
                self.pwm_b.pulse_width_percent(0)
            else:
                self.pwm_a.pulse_width_percent(0)
                self.pwm_b.pulse_width_percent(speed)
        # unkowned mode
        else:
            raise ValueError("Unkown motors mode")
        

    def set_is_reverse(self, is_reverse):
        """
        Set motor is reversed or not

        :param is_reverse: True or False
        :type is_reverse: bool
        """
        self._is_reverse = is_reverse


class Motors(_Basic_class):
    """Motors"""

    DB_FILE = "motors.db"

    MOTOR_1_PWM_PIN = "P13"
    MOTOR_1_DIR_PIN = "D4"
    MOTOR_2_PWM_PIN = "P12"
    MOTOR_2_DIR_PIN = "D5"
    config_file = "/opt/robot_hat/default_motors.config"
    def __init__(self, db=config_file, *args, **kwargs):
        """
        Initialize motors with robot_hat.motor.Motor

        :param db: config file path
        :type db: str
        """
        super().__init__(*args, **kwargs)

        self.db = fileDB(db=db, mode='774', owner=User)
        self.left_id = int(self.db.get("left", default_value=0))
        self.right_id = int(self.db.get("right", default_value=0))
        left_reversed = bool(self.db.get(
            "left_reverse", default_value=False))
        right_reversed = bool(self.db.get(
            "right_reverse", default_value=False))

        self.motors = [
            Motor(PWM(self.MOTOR_1_PWM_PIN), Pin(self.MOTOR_1_DIR_PIN)),
            Motor(PWM(self.MOTOR_2_PWM_PIN), Pin(self.MOTOR_2_DIR_PIN))
        ]
        if self.left_id != 0:
            self.left.set_is_reverse(left_reversed)
        if self.right_id != 0:
            self.right.set_is_reverse(right_reversed)

    def __getitem__(self, key):
        """Get specific motor"""
        return self.motors[key-1]

    def stop(self):
        """Stop all motors"""
        for motor in self.motors:
            motor.speed(0)

    @property
    def left(self):
        """left motor"""
        if self.left_id not in range(1, 3):
            raise ValueError(
                "left motor is not set yet, set it with set_left_id(1/2)")
        return self.motors[self.left_id-1]

    @property
    def right(self):
        """right motor"""
        if self.left_id not in range(1, 3):
            raise ValueError(
                "left motor is not set yet, set it with set_left_id(1/2)")
        return self.motors[self.right_id-1]

    def set_left_id(self, id):
        """
        Set left motor id, this function only need to run once
        It will save the motor id to config file, and load
        the motor id when the class is initialized

        :param id: motor id (1 or 2)
        :type id: int
        """
        if id not in range(1, 3):
            raise ValueError("Motor id must be 1 or 2")
        self.left_id = id
        self.db.set("left", id)

    def set_right_id(self, id):
        """
        Set right motor id, this function only need to run once
        It will save the motor id to config file, and load
        the motor id when the class is initialized

        :param id: motor id (1 or 2)
        :type id: int
        """
        if id not in range(1, 3):
            raise ValueError("Motor id must be 1 or 2")
        self.right_id = id
        self.db.set("right", id)

    def set_left_reverse(self):
        """
        Set left motor reverse, this function only need to run once
        It will save the reversed status to config file, and load
        the reversed status when the class is initialized

        :return: if currently is reversed
        :rtype: bool
        """
        is_reversed = bool(self.db.get("left_reverse", default_value=False))
        is_reversed = not is_reversed
        self.db.set("left_reverse", is_reversed)
        self.left.set_is_reverse(is_reversed)
        return is_reversed

    def set_right_reverse(self):
        """
        Set right motor reverse, this function only need to run once
        It will save the reversed status to config file, and load
        the reversed status when the class is initialized

        :return: if currently is reversed
        :rtype: bool
        """
        is_reversed = bool(self.db.get("right_reverse", default_value=False))
        is_reversed = not is_reversed
        self.db.set("right_reverse", is_reversed)
        self.right.set_is_reverse(is_reversed)
        return is_reversed

    def speed(self, left_speed, right_speed):
        """
        Set motor speed

        :param left_speed: left motor speed(-100.0~100.0)
        :type left_speed: float
        :param right_speed: right motor speed(-100.0~100.0)
        :type right_speed: float
        """
        self.left.speed(left_speed)
        self.right.speed(right_speed)

    def forward(self, speed):
        """
        Forward

        :param speed: Motor speed(-100.0~100.0)
        :type speed: float
        """
        self.speed(speed, speed)

    def backward(self, speed):
        """
        Backward

        :param speed: Motor speed(-100.0~100.0)
        :type speed: float
        """
        self.speed(-speed, -speed)

    def turn_left(self, speed):
        """
        Left turn

        :param speed: Motor speed(-100.0~100.0)
        :type speed: float
        """
        self.speed(-speed, speed)

    def turn_right(self, speed):
        """
        Right turn

        :param speed: Motor speed(-100.0~100.0)
        :type speed: float
        """
        self.speed(speed, -speed)
