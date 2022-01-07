#!/usr/bin/env python3
from .pwm import PWM
from .pin import Pin

class Motor():
    PERIOD = 4095
    PRESCALER = 10
    def __init__(self):

        self.left_rear_pwm_pin = PWM("P13")
        self.right_rear_pwm_pin = PWM("P12")
        self.left_rear_dir_pin = Pin("D4")
        self.right_rear_dir_pin = Pin("D5")

        self.motor_speed_pins = [self.left_rear_pwm_pin, self.right_rear_pwm_pin]

        #初始化PWM引脚
        for pin in self.motor_speed_pins:
            pin.period(self.PERIOD)
            pin.prescaler(self.PRESCALER)

    #Control motor direction and speed
    #motor 0 or 1,
    #dir   0 or 1
    #speed 0 ~ 100
    def wheel(self,speed,motor = -1):

        dir = 1 if speed > 0 else 0
        speed = abs(speed)

        if speed != 0:
            speed = int(speed /2 ) + 50

        if motor == 0:

            self.left_rear_dir_pin.value(dir)
            self.left_rear_pwm_pin.pulse_width_percent(speed)

        elif motor == 1:
            
            self.right_rear_dir_pin.value(dir)
            self.right_rear_pwm_pin.pulse_width_percent(speed)

        elif motor == -1:
            
            self.left_rear_dir_pin.value(dir)
            self.left_rear_pwm_pin.pulse_width_percent(speed)
            self.right_rear_dir_pin.value(dir)
            self.right_rear_pwm_pin.pulse_width_percent(speed)
