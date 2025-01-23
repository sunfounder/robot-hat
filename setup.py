#!/usr/bin/env python3
from os import path
import sys
import os

print('\033[0;33mThe "setup.py" installation method is planned to be abandoned.\n'
    'Please execute "install.py" to install.\n\033[0m')

if 'install' in sys.argv:
    here = path.abspath(path.dirname(__file__))
    os.chdir(here)
    args = ' '.join(sys.argv[1:])
    os.system(f'python3 install.py {args}')

    exit()

# necessary for pip3 install ./ , 
# if you need both `setup.py`` and `pyproject.toml`` to exist
from setuptools import setup
setup()

