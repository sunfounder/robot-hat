#!/usr/bin/env python3
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


class Robot():
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
    PINS = [None, "P0", "P1", "P2", "P3", "P4",
            "P5", "P6", "P7", "P8", "P9", "P10", "P11"]

    def __init__(self, pin_list, db=config_file, name=None, init_angles=None):
        """
        Initialize the robot class

        :param pin_list: list of pin number[1-12]
        :type pin_list: list
        :param db: config file path
        :type db: str
        :param name: robot name
        :type name: str
        :param init_angles: list of initial angles
        :type init_angles: list
        """
        self.servo_list = []
        self.pin_num = len(pin_list)
        self.list_name = name

        if self.list_name == None:
            if self.pin_num == 12:
                self.list_name = 'spider_servo_offset_list'
            elif self.pin_num == 3:
                self.list_name = 'piarm_servo_offset_list'
            elif self.pin_num == 4:
                self.list_name = 'sloth_servo_offset_list'
            elif self.pin_num == 8:
                self.list_name = 'pidog_servo_offset_list'
            else:
                self.list_name = 'other'

        # offset
        self.db = fileDB(db=db, mode='774', owner=User)
        temp = self.db.get(self.list_name, default_value=str(self.new_list(0)))
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

        if name == 'feet':
            self.servo_list = [None]*8
            # 0 - 8 ， 4567
            for i in range(7, 0, -2):
                pwm = PWM(self.PINS[pin_list[i]])
                servo = Servo(pwm)
                servo.angle(self.offset[i]+init_angles[i])
                self.servo_positions[i] = init_angles[i]
                self.servo_list[i] = servo
                time.sleep(0.15)
            for i in range(0, 7, 2):
                pwm = PWM(self.PINS[pin_list[i]])
                servo = Servo(pwm)
                servo.angle(self.offset[i]+init_angles[i])
                self.servo_positions[i] = init_angles[i]
                self.servo_list[i] = servo
                time.sleep(0.15)

        for i, pin in enumerate(pin_list):
            pwm = PWM(self.PINS[pin])
            servo = Servo(pwm)
            servo.angle(self.offset[i]+init_angles[i])
            self.servo_positions[i] = init_angles[i]
            self.servo_list.append(servo)
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

    def angle_list(self, angle_list):
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
        self.angle_list(rel_angles)

    def servo_move(self, targets, speed=50, bpm=None):
        '''
        Move servo to specific angles with speed or bpm

        :param targets: list of servo angles
        :type targets: list
        :param speed: speed of servo move
        :type speed: int or float
        :param bpm: beats per minute
        :type bpm: int or float
        '''
        '''
        Calculate the max delta angle, multiply by 2 to define a max_step
        loop max_step times, every servo add/minus 1 when step reaches its adder_flag
        '''
        speed = max(0, speed)
        speed = min(100, speed)
        delta = []
        absdelta = []
        max_step = 0
        steps = []

        for i in range(self.pin_num):
            value = targets[i] - self.servo_positions[i]
            delta.append(value)
            absdelta.append(abs(value))

        max_step = int(1*max(absdelta))
        if max_step != 0:
            for i in range(self.pin_num):
                step = float(delta[i])/max_step
                steps.append(step)

            if bpm != None:
                step_time = 1 / bpm * 60
                step_delay = step_time / max_step
            for _ in range(max_step):
                for j in range(self.pin_num):
                    self.servo_positions[j] += steps[j]
                self.servo_write_all(self.servo_positions)
                # 5~5005us
                if bpm != None:
                    time.sleep(step_delay)
                else:
                    t = (100-speed)*50+5
                    time.sleep(t/100000)
        else:
            t = (100-speed)*50+5
            time.sleep(t/50000)

    def servo_move2(self, targets, speed=50, bpm=None):
        """
        Move servo to specific angles with speed or bpm,
        servo_move2 move faster than servo_move.

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
        self.db.set(self.list_name, temp)
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
