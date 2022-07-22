#!/usr/bin/env python3
from .pwm import PWM
from .servo import Servo
import time
import math
from .filedb import fileDB
import os

# user and User home directory
User = os.popen('echo ${SUDO_USER:-$LOGNAME}').readline().strip()
UserHome = os.popen('getent passwd %s | cut -d: -f 6'%User).readline().strip()
# print(User)  # pi
# print(UserHome) # /home/pi
config_file = '%s/.config/robot-hat/robot-hat.conf'%UserHome


class Robot():
    move_list = {}
    PINS = [None, "P0","P1","P2","P3","P4","P5","P6","P7","P8","P9","P10","P11"]

    def __init__(self, pin_list, group=None, db=config_file, name=None, init_angles=None):
        
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
            for i in range(7,0,-2): 
                pwm = PWM(self.PINS[pin_list[i]])
                servo = Servo(pwm)
                servo.angle(self.offset[i]+init_angles[i])
                self.servo_positions[i]=init_angles[i]
                self.servo_list[i]= servo
                time.sleep(0.15)
            for i in range(0,7,2): 
                pwm = PWM(self.PINS[pin_list[i]])
                servo = Servo(pwm)
                servo.angle(self.offset[i]+init_angles[i])
                self.servo_positions[i]=init_angles[i]
                self.servo_list[i]= servo
                time.sleep(0.15)          

        for i, pin in enumerate(pin_list):
            pwm = PWM(self.PINS[pin])
            servo = Servo(pwm)
            servo.angle(self.offset[i]+init_angles[i])
            self.servo_positions[i]=init_angles[i]
            self.servo_list.append(servo)
            time.sleep(0.15)

    def new_list(self, default_value):
        _ = [default_value] * self.pin_num
        return _


    def angle_list(self, angle_list):
        for i in range(self.pin_num):
            self.servo_list[i].angle(angle_list[i])


    def servo_write_all(self, angles):
        rel_angles = []  # ralative angle to home
        for i in range(self.pin_num):
            rel_angles.append(self.direction[i] * (self.origin_positions[i] + angles[i] + self.offset[i]))
            # rel_angles.append(angles[i])
            # print(rel_angles)
        self.angle_list(rel_angles)


    def servo_move(self, targets, speed=50, bpm=None):
        '''
            calculate the max delta angle, multiply by 2 to define a max_step
            loop max_step times, every servo add/minus 1 when step reaches its adder_flag
        '''
        # sprint("Servo_move")
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
                #5~5005us
                if bpm != None:
                    time.sleep(step_delay)
                else:
                    t = (100-speed)*50+5
                    time.sleep(t/100000)
        else:
            t = (100-speed)*50+5
            time.sleep(t/50000)
            
    def servo_move2(self, targets, speed=50, bpm=None):
        '''
            calculate the max delta angle, multiply by 2 to define a max_step
            loop max_step times, every servo add/minus 1 when step reaches its adder_flag
        '''
        # sprint("Servo_move")
        speed = max(0, speed)
        speed = min(100, speed)
        step_time = 10 # ms
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
            
            
    def do_action(self,motion_name, step=1, speed=50):
        for _ in range(step):
            for motion in self.move_list[motion_name]:
                self.servo_move(motion, speed)

    def set_offset(self,offset_list):
        offset_list = [ min(max(offset, -20), 20) for offset in offset_list]
        temp = str(offset_list)
        self.db.set(self.list_name,temp)
        self.offset = offset_list
        # self.calibration()
        # self.reset()

    def calibration(self):
        self.servo_positions = self.calibrate_position
        self.servo_write_all(self.servo_positions)

    def reset(self,):
        self.servo_positions = self.new_list(0)
        self.servo_write_all(self.servo_positions)

    def soft_reset(self,):
        temp_list = self.new_list(0)
        self.servo_write_all(temp_list)
