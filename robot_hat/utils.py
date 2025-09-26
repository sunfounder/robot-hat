#!/usr/bin/env python3
import time
import os
import sys
import re
from .pin import Pin


# color:
# https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007
# 1;30:gray 31:red, 32:green, 33:yellow, 34:blue, 35:purple, 36:dark green, 37:white
GRAY = '1;30'
RED = '0;31'
GREEN = '0;32'
YELLOW = '0;33'
BLUE = '0;34'
PURPLE = '0;35'
DARK_GREEN = '0;36'
WHITE = '0;37'

_adc_obj = None

def print_color(msg, end='\n', file=sys.stdout, flush=False, color=''):
    print('\033[%sm%s\033[0m'%(color, msg), end=end, file=file, flush=flush)

def info(msg, end='\n', file=sys.stdout, flush=False):
    print_color(msg, end=end, file=file, flush=flush, color=WHITE)

def debug(msg, end='\n', file=sys.stdout, flush=False):
    print_color(msg, end=end, file=file, flush=flush, color=GRAY)

def warn(msg, end='\n', file=sys.stdout, flush=False):
    print_color(msg, end=end, file=file, flush=flush, color=YELLOW)

def error(msg, end='\n', file=sys.stdout, flush=False):
    print_color(msg, end=end, file=file, flush=flush, color=RED)

def set_volume(value):
    """
    Set volume

    :param value: volume(0~100)
    :type value: int
    """
    value = min(100, max(0, value))
    cmd = "sudo amixer -M sset 'PCM' %d%%" % value
    os.system(cmd)


def command_exists(cmd):
    import subprocess
    try:
        subprocess.check_output(['which', cmd], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False


def run_command(cmd, user=None, group=None):
    """
    Run command and return status and output

    :param cmd: command to run
    :type cmd: str
    :return: status, output
    :rtype: tuple
    """
    import subprocess
    p = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        user=user,
        group=group)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    return status, result

def command_exists(cmd):
    import subprocess
    try:
        subprocess.check_output(['which', cmd], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def is_installed(cmd):
    """
    Check if command is installed

    :param cmd: command to check
    :type cmd: str
    :return: True if installed
    :rtype: bool
    """
    status, _ = run_command(f"which {cmd}")
    if status in [0, ]:
        return True
    else:
        return False


def mapping(x, in_min, in_max, out_min, out_max):
    """
    Map value from one range to another range

    :param x: value to map
    :type x: float/int
    :param in_min: input minimum
    :type in_min: float/int
    :param in_max: input maximum
    :type in_max: float/int
    :param out_min: output minimum
    :type out_min: float/int
    :param out_max: output maximum
    :type out_max: float/int
    :return: mapped value
    :rtype: float/int
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def get_ip(ifaces=['wlan0', 'eth0']):
    """
    Get IP address

    :param ifaces: interfaces to check
    :type ifaces: list
    :return: IP address or False if not found
    :rtype: str/False
    """
    if isinstance(ifaces, str):
        ifaces = [ifaces]
    for iface in list(ifaces):
        search_str = 'ip addr show {}'.format(iface)
        result = os.popen(search_str).read()
        com = re.compile(r'(?<=inet )(.*)(?=\/)', re.M)
        ipv4 = re.search(com, result)
        if ipv4:
            ipv4 = ipv4.groups()[0]
            return ipv4
    return False


def reset_mcu():
    """
    Reset mcu on Robot Hat.

    This is helpful if the mcu somehow stuck in a I2C data
    transfer loop, and Raspberry Pi getting IOError while
    Reading ADC, manipulating PWM, etc.
    """
    from .pin import Pin
    pin = Pin("MCURST")
    pin.off()
    time.sleep(0.01)
    pin.on()
    time.sleep(0.01)
    pin.close()

def get_battery_voltage():
    """
    Get battery voltage

    :return: battery voltage(V)
    :rtype: float
    """
    global _adc_obj
    from .adc import ADC

    if not isinstance(_adc_obj, ADC):
        _adc_obj = ADC("A4")
    raw_voltage = _adc_obj.read_voltage()
    voltage = raw_voltage * 3
    return voltage

def get_username():
    return os.popen('echo ${SUDO_USER:-$LOGNAME}').readline().strip()

def set_pin(pin: int, value: bool):
    """
    Set pin value

    :param pin: pin number
    :type pin: int
    :param value: pin value
    :type value: bool
    """
    from . import __device__
    pincmd = ''
    if command_exists("pinctrl"):
        pincmd = 'pinctrl'
    elif command_exists("raspi-gpio"):
        pincmd = 'raspi-gpio'
    else:
        error("Can't find `pinctrl` or `raspi-gpio` to enable speaker")
        return

    cmd = f"{pincmd} set {pin} op {'dh' if value else 'dl'}"
    debug(cmd)
    run_command(cmd)

def enable_speaker():
    """
    Enable speaker
    """
    from . import __device__
    set_pin(__device__.spk_en, True)
    # play a short sound to fill data and avoid the speaker overheating
    run_command(f"play -n trim 0.0 0.5 2>/dev/null")

def disable_speaker():
    """
    Disable speaker
    """
    from . import __device__
    set_pin(__device__.spk_en, False)

def check_executable(executable):
    """
    Check if executable is installed

    :param executable: executable name
    :type executable: str
    :return: True if installed
    :rtype: bool
    """
    from distutils.spawn import find_executable
    executable_path = find_executable(executable)
    found = executable_path is not None
    return found

def redirect_error_2_null():
    # https://github.com/spatialaudio/python-sounddevice/issues/11

    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    return old_stderr

def cancel_redirect_error(old_stderr):
    os.dup2(old_stderr, 2)
    os.close(old_stderr)

class ignore_stderr():
    def __init__(self):
        self.old_stderr = redirect_error_2_null()
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        cancel_redirect_error(self.old_stderr)
