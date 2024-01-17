#!/usr/bin/env python3
import time
import os
import re
from .pin import Pin


def set_volume(value):
    """
    Set volume

    :param value: volume(0~100)
    :type value: int
    """
    value = min(100, max(0, value))
    cmd = "sudo amixer -M sset 'PCM' %d%%" % value
    os.system(cmd)


def run_command(cmd):
    """
    Run command and return status and output

    :param cmd: command to run
    :type cmd: str
    :return: status, output
    :rtype: tuple
    """
    import subprocess
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    return status, result


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
    mcu_reset = Pin("MCURST")
    mcu_reset.off()
    time.sleep(0.01)
    mcu_reset.on()
    time.sleep(0.01)

    mcu_reset.close()


def get_battery_voltage():
    """
    Get battery voltage

    :return: battery voltage(V)
    :rtype: float
    """
    from .adc import ADC
    adc = ADC("A4")
    raw_voltage = adc.read_voltage()
    voltage = raw_voltage * 3
    return voltage
