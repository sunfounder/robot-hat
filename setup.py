#!/usr/bin/env python3
import sys
from setuptools import setup
import time
import threading

# if len(sys.argv) > 1 and sys.argv[1] == 'install':
#     tip = '''\
# "setup.py install" is deprecated.Please use the following to install:
#         sudo python3 install.py
# '''
#     print(f'{tip}')
#     sys.exit(1)
# else:
#     setup()

setup()

def run_command(cmd=""):
    import subprocess
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    return status, result

errors = []
at_work_tip_sw = False
def working_tip():
    char = ['/', '-', '\\', '|']
    i = 0
    global at_work_tip_sw
    while at_work_tip_sw:  
            i = (i+1)%4 
            sys.stdout.write('\033[?25l') # cursor invisible
            sys.stdout.write('%s\033[1D'%char[i])
            sys.stdout.flush()
            time.sleep(0.5)

    sys.stdout.write(' \033[1D')
    sys.stdout.write('\033[?25h') # cursor visible 
    sys.stdout.flush()    
        

def do(msg="", cmd=""):
    print(" - %s... " % (msg), end='', flush=True)
    # at_work_tip start 
    global at_work_tip_sw
    at_work_tip_sw = True
    _thread = threading.Thread(target=working_tip)
    _thread.daemon = True
    _thread.start()
    # process run
    status, result = run_command(cmd)
    # print(status, result)
    # at_work_tip stop
    at_work_tip_sw = False
    while _thread.is_alive():
        time.sleep(0.01)
    # status
    if status == 0 or status == None or result == "":
        print('Done')
    else:
        print('Error')
        errors.append("%s error:\n  Status:%s\n  Error:%s" %
                      (msg, status, result))

APT_INSTALL_LIST = [
    'raspi-config',
    "i2c-tools",
    "espeak",
    'libsdl2-dev',
    'libsdl2-mixer-dev',
]

PIP_INSTALL_LIST = [
    'smbus2',
    'gpiozero',
    'pyaudio',
    'spidev',
    'pyserial',
    'pillow',
    "'pygame>=2.1.2'",
]

if sys.argv[1] == 'install':
    try:
        # Install dependency 
        # =============================
        print("Install dependencies with apt:")
        # update apt
        do(msg="update apt",
            cmd='sudo apt update')
        #
        for dep in APT_INSTALL_LIST:
            do(msg=f"install {dep}",
                cmd=f'sudo apt install {dep} -y')
        #
        do(msg="install pico2wave",
            cmd='wget http://ftp.us.debian.org/debian/pool/non-free/s/svox/libttspico0_1.0+git20130326-9_armhf.deb'
            +' && wget http://ftp.us.debian.org/debian/pool/non-free/s/svox/libttspico-utils_1.0+git20130326-9_armhf.deb'
            +' && sudo apt-get install -f ./libttspico0_1.0+git20130326-9_armhf.deb ./libttspico-utils_1.0+git20130326-9_armhf.deb -y')
        
        # =============================
        print("Install dependencies with pip3:")
        # check whether pip has the option "--break-system-packages"
        _is_bsps = ''
        status, _ = run_command("pip3 help install|grep break-system-packages")
        if status == 0: # if true
            _is_bsps = "--break-system-packages"
            print("\033[38;5;8m pip3 install with --break-system-packages\033[0m")
        # update pip
        do(msg="update pip3",
            cmd=f'python3 -m pip install --upgrade pip {_is_bsps}'
        )
        #
        for dep in PIP_INSTALL_LIST:
            do(msg=f"install {dep}",
                cmd=f'sudo pip3 install {dep} {_is_bsps}')
        
        # Setup interfaces
        # =============================
        print("Setup interfaces")
        do(msg="turn on I2C",
            cmd='sudo raspi-config nonint do_i2c 0')
        do(msg="turn on SPI",
            cmd='sudo raspi-config nonint do_spi 0')
        # Report error
        # =============================
        if len(errors) == 0:
            print("Finished")
        else:
            print("\n\nError happened in install process:")
            for error in errors:
                print(error)
            print("Try to fix it yourself, or contact service@sunfounder.com with this message")
            sys.exit(1)

    except KeyboardInterrupt:
        print("Canceled.")
    except Exception as e:
        print(e)
    finally:
        sys.stdout.write('\033[?25h') # cursor visible 
        sys.stdout.flush()


