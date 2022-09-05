#!/usr/bin/env python3
from .basic import _Basic_class
from .pwm import PWM
from .servo import Servo
import time
from .filedb import fileDB
import os

# user and User home directory
User = os.popen('echo ${SUDO_USER:-$LOGNAME}').readline().strip()
UserHome = os.popen('getent passwd %s | cut -d: -f 6' %
                    User).readline().strip()
config_file = '%s/.config/robot-hat/robot-hat.conf' % UserHome


class Robot(_Basic_class):
    """
    Robot class

    This class is for makeing a servo robot with Robot HAT

    There are servo initialization, all servo move in specific speed. servo offset and stuff. make it easy to make a robot.
    All Pi-series robot from SunFounder use this class. Check them out for more details.

    PiSloth: https://github.com/sunfounder/pisloth

    PiArm: https://github.com/sunfounder/piarm

    PiCrawler: https://github.com/sunfounder/picrawler
    """

    move_list = {}
    """Preset actions"""

    def __init__(self, pin_list, db=config_file, name=None, init_angles=None, init_order=None):
        """
        Initialize the robot class

        :param pin_list: list of pin number[0-11]
        :type pin_list: list
        :param db: config file path
        :type db: str
        :param name: robot name
        :type name: str
        :param init_angles: list of initial angles
        :type init_angles: list
        :param init_order: list of initialization order(Servos will init one by one in case of sudden huge current, pulling down the power supply voltage. default order is the pin list. in some cases, you need different order, use this parameter to set it.)
        :type init_order: list
        :type init_angles: list
        """
        self.servo_list = []
        self.pin_num = len(pin_list)

        if self.offset_value_name == None:
            self.offset_value_name = 'other'

        self.offset_value_name = f"{name}_servo_offset_list"
        # offset
        self.db = fileDB(db=db, mode='774', owner=User)
        temp = self.db.get(self.offset_value_name,
                           default_value=str(self.new_list(0)))
        temp = [float(i.strip()) for i in temp.strip("[]").split(",")]
        self.offset = temp

        # parameter init
        self.servo_positions = self.new_list(0)
        self.origin_positions = self.new_list(0)
        self.calibrate_position = self.new_list(0)
        self.direction = self.new_list(1)

        # servo init
        if None == init_angles:
            init_angles = [0]*self.pin_num
        elif len(init_angles) != self.pin_num:
            raise ValueError('init angels numbers do not match pin numbers ')

        if init_order == None:
            init_order = range(self.pin_num)

        for i in init_order:
            pwm = PWM(pin_list[i])
            servo = Servo(pwm)
            servo.angle(self.offset[i]+init_angles[i])
            self.servo_positions[i] = init_angles[i]
            self.servo_list[i] = servo
            time.sleep(0.15)

    def new_list(self, default_value):
        """
        Create a list of servo angles with default value

        :param default_value: default value of servo angles
        :type default_value: int or float
        :return: list of servo angles
        :rtype: list
        """
        _ = [default_value] * self.pin_num
        return _

    def servo_write_raw(self, angle_list):
        """
        Set servo angles to specific raw angles

        :param angle_list: list of servo angles
        :type angle_list: list
        """
        for i in range(self.pin_num):
            self.servo_list[i].angle(angle_list[i])

    def servo_write_all(self, angles):
        """
        Set servo angles to specific angles with original angle and offset

        :param angles: list of servo angles
        :type angles: list
        """
        rel_angles = []  # ralative angle to home
        for i in range(self.pin_num):
            rel_angles.append(
                self.direction[i] * (self.origin_positions[i] + angles[i] + self.offset[i]))
        self.servo_write_raw(rel_angles)

    def servo_move(self, targets, speed=50, bpm=None):
        """
        Move servo to specific angles with speed or bpm

        :param targets: list of servo angles
        :type targets: list
        :param speed: speed of servo move
        :type speed: int or float
        :param bpm: beats per minute
        :type bpm: int or float
        """
        '''
            calculate the max delta angle, multiply by 2 to define a max_step
            loop max_step times, every servo add/minus 1 when step reaches its adder_flag
        '''
        # sprint("Servo_move")
        speed = max(0, speed)
        speed = min(100, speed)
        step_time = 10  # ms
        delta = []
        absdelta = []
        max_step = 0
        steps = []

        for i in range(self.pin_num):
            value = targets[i] - self.servo_positions[i]
            delta.append(value)
            absdelta.append(abs(value))

        max_delta = int(1*max(absdelta))
        max_step = -9.9 * speed + 1000
        if bpm:
            max_step = 1 / bpm * 60 * 1000

        max_step = int(max_step / step_time)

        if max_delta != 0:
            for i in range(self.pin_num):
                step = float(delta[i])/max_step
                steps.append(step)

            for _ in range(max_step):
                start_timer = time.time()
                delay = step_time/1000
                for j in range(self.pin_num):
                    self.servo_positions[j] += steps[j]
                self.servo_write_all(self.servo_positions)

                servo_move_time = time.time() - start_timer
                delay = delay - servo_move_time
                delay = max(0, delay)
                time.sleep(delay)
        else:
            time.sleep(step_time/1000)

    def do_action(self, motion_name, step=1, speed=50):
        """
        Do prefix action with motion_name and step and speed

        :param motion_name: motion
        :type motion_name: str
        :param step: step of motion
        :type step: int
        :param speed: speed of motion
        :type speed: int or float
        """
        for _ in range(step):
            for motion in self.move_list[motion_name]:
                self.servo_move(motion, speed)

    def set_offset(self, offset_list):
        """
        Set offset of servo angles

        :param offset_list: list of servo angles
        :type offset_list: list
        """
        offset_list = [min(max(offset, -20), 20) for offset in offset_list]
        temp = str(offset_list)
        self.db.set(self.offset_value_name, temp)
        self.offset = offset_list

    def calibration(self):
        """Move all servos to home position"""
        self.servo_positions = self.calibrate_position
        self.servo_write_all(self.servo_positions)

    def reset(self):
        """Reset servo to original position"""
        self.servo_positions = self.new_list(0)
        self.servo_write_all(self.servo_positions)

    def soft_reset(self):
        temp_list = self.new_list(0)
        self.servo_write_all(temp_list)
