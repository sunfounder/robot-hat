#!/usr/bin/env python3
"""
Robot Hat Library
"""
from .adc import ADC
from .filedb import fileDB
from .i2c import I2C
from .modules import *
from .music import Music
from .motor import Motor, Motors
from .pin import Pin
from .pwm import PWM
from .servo import Servo
from .tts import TTS
from .utils import *
from .robot import Robot
from .version import __version__

def __usage__():
    print('''
    Usage: robot_hat [option]

    reset_mcu               reset mcu on robot-hat
    enable_speaker          enable speaker (drive high gpio 20)
    disable_speaker         disable speaker (drive low gpio 20)
    ''')
    quit()


def __main__():
    import sys
    import os
    if len(sys.argv) == 2:
        if sys.argv[1] == "reset_mcu":
            reset_mcu()
            print("Onboard MCU reset.")
        elif sys.argv[1] == "enable_speaker":
            print("Enable Speaker.")
            os.popen("pinctrl set 20 op dh")
        elif sys.argv[1] == "disable_speaker":
            print("Enable Speaker.")
            os.popen("pinctrl set 20 op dl")
    else:
        __usage__()
