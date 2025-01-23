from robot_hat import Servo
from time import sleep

servos = [Servo(i) for i in range(12)]

while True:
    for servo in servos:
        servo.angle(-20)
        sleep(0.1)
    for servo in servos:
        servo.angle(20)
        sleep(0.1)

