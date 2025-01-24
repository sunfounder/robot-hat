#!/usr/bin/env python3
"""
Robot Hat Library
"""
from .adc import ADC
from .filedb import fileDB
from .config import Config
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

from .device import Devices
__device__ = Devices()

def __usage__():
    print('''
Usage: robot_hat [option]

reset_mcu               reset mcu on robot-hat
enable_speaker          enable speaker
disable_speaker         disable speaker
version                 get robot-hat libray version
info                    get hat info
    ''')
    quit()

def get_firmware_version():
    ADDR = [0x14, 0x15]
    VERSSION_REG_ADDR = 0x05
    i2c = I2C(ADDR)
    version = i2c.mem_read(3, VERSSION_REG_ADDR)
    return version

def __main__():
    import sys
    import os
    if len(sys.argv) == 2:
        if sys.argv[1] == "reset_mcu":
            reset_mcu()
            print("Onboard MCU reset.")
        elif sys.argv[1] == "enable_speaker":
            print(f"Enable Robot-HAT speaker.")
            utils.enable_speaker()
        elif sys.argv[1] == "disable_speaker":
            print(f"Disable Robot-HAT speaker.")
            utils.disable_speaker()
        elif sys.argv[1] == "version":
            print(f"robot-hat library version: {__version__}")
        elif sys.argv[1] == "info":
            print(f'HAT name: {__device__.name}')
            print(f'PCB ID: O{__device__.product_id}V{__device__.product_ver}')
            print(f'Vendor: {__device__.vendor}')
            firmware_ver = get_firmware_version()
            firmware_ver = f'{firmware_ver[0]}.{firmware_ver[1]}.{firmware_ver[2]}'
            print(f"Firmare version: {firmware_ver}")
        else:
            print("\033[0;33mUnknown option.\033[0m")
            __usage__()
    else:
        __usage__()
