#!/usr/bin/env python3

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import sys
import os
import time
import threading

sys.path.append('./robot_hat')
from version import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='robot_hat',
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,

    description='Library for SunFounder Robot Hat',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/sunfounder/robot-hat',

    # Author details
    author='SunFounder',
    author_email='service@sunfounder.com',

    # Choose your license
    license='GNU',
    zip_safe=False,
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords='python raspberry pi GPIO sunfounder',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['tests', 'docs']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[ ],
    
    
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'robot_hat=robot_hat:__main__',
        ],
    },
)

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
        time.sleep(0.1)
    # status
    if status == 0 or status == None or result == "":
        print('Done')
    else:
        print('Error')
        errors.append("%s error:\n  Status:%s\n  Error:%s" %
                      (msg, status, result))


APT_INSTALL_LIST = [
    'python3-smbus',
    "i2c-tools",
    "espeak",
    "python3-pyaudio",
    'libsdl2-dev',
    'libsdl2-mixer-dev',
]

PIP_INSTALL_LIST = [
    'RPi.GPIO',
    'spidev',
    'pyserial',
    "gpiozero",
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
                

