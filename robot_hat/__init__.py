#!/usr/bin/env python3
"""
Robot Hat Library
"""
from .adc import ADC
from .filedb import fileDB
from .i2c import I2C
from .modules import *
from .music import Music
from .motor import Motor
from .pin import Pin
from .pwm import PWM
from .servo import Servo
from .switch import Switch
from .tts import TTS
from .utils import *
from .robot import Robot

import sys

def __usage__():
    print("Usage: robot_hat [reset_mcu]")
    quit()

def __main__():
    if len(sys.argv) == 2:
        if sys.argv[1] == "reset_mcu":
            reset_mcu()
            print("Onboard MCU reset.")
    else:
        __usage__()