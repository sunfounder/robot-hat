from robot_hat.modules import Ultrasonic
from robot_hat.pin import Pin
import time

ultrasonic = Ultrasonic(trig=Pin("D2"), echo=Pin("D3"))

while True:
    distance = ultrasonic.read()
    print(f"\r\x1b[KDistance: {distance} cm", end="", flush=True)
    time.sleep(0.2)
