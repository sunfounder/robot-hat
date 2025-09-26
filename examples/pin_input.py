from robot_hat import Pin

import time

pin = Pin('D3', mode=Pin.IN, pull=Pin.PULL_UP)

while True:
    print(pin.value())
    time.sleep(0.1)
