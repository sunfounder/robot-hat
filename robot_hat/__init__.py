#!/usr/bin/env python3
"""
Robot Hat Library
"""
import importlib.util
import warnings

from .version import __version__
from .device import Devices

__device__ = Devices()

#: Python modules the library itself needs at import time.  When one of them
#: is missing the heavy imports below are skipped, so that 'robot_hat doctor'
#: can still run and tell the user what to install.
IMPORT_MODULES = ("smbus2", "lgpio", "pyaudio", "pygame")

_missing = [name for name in IMPORT_MODULES if importlib.util.find_spec(name) is None]

if _missing:
    warnings.warn(
        "robot_hat: missing python module(s): %s. The library cannot be imported "
        "until they are installed - run 'robot_hat doctor' to check the "
        "installation." % ", ".join(_missing),
        stacklevel=2,
    )
else:
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
    from .utils import *
    from .robot import Robot


def __usage__():
    print('''
Usage: robot_hat [command]

doctor                  check the Robot HAT installation
speaker                 speaker control (enable/disable/test/setup)
info                    get hat info
version                 get robot-hat library version
scan_i2c                scan the I2C bus
reset_mcu               reset mcu on robot-hat
update                  update the library with install.sh
    ''')
    quit()


def get_firmware_version():
    from .i2c import I2C
    ADDR = [0x14, 0x15]
    VERSSION_REG_ADDR = 0x05
    i2c = I2C(ADDR)
    version = i2c.mem_read(3, VERSSION_REG_ADDR)
    return version


def __main__():
    """
    Entry point of the 'robot_hat' command.

    See :func:'robot_hat._cli.main' for the available commands.
    """
    from ._cli import main
    main()
