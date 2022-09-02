#!/usr/bin/env python3
from .basic import _Basic_class
from .pwm import PWM
from .pin import Pin
from .filedb import fileDB
import os

# user and User home directory
User = os.popen('echo ${SUDO_USER:-$LOGNAME}').readline().strip()
UserHome = os.popen('getent passwd %s | cut -d: -f 6' %
                    User).readline().strip()
config_file = '%s/.config/robot-hat/robot-hat.conf' % UserHome


class Motor():
    """Motor"""
    PERIOD = 4095
    PRESCALER = 10

    def __init__(self, pwm, dir, is_reversed=False):
        """
        Initialize a motor

        :param pwm: Motor speed control pwm pin
        :type pwm: robot_hat.pwm.PWM
        :param dir: Motor direction control pin
        :type dir: robot_hat.pin.Pin
        """
        self.pwm = pwm
        self.dir = dir
        self.pwm.period(self.PERIOD)
        self.pwm.prescaler(self.PRESCALER)
        self.pwm.pulse_width_percent(0)
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
            dir = dir + 1 & 1
        speed = abs(speed)
        self.pwm.pulse_width_percent(speed)
        self.dir.value(dir)

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
