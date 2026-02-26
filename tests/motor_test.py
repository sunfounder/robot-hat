from robot_hat import Motor, PWM, Pin
from time import sleep

m1 = Motor("M1")
m2= Motor("M2")

try:
    while True:
        print("Moter 1")
        m1.power(-50)
        sleep(1)
        m1.power(50)
        sleep(1)
        m1.power(0)
        
        print("Moter 2")
        m2.power(-50)
        sleep(1)
        m2.power(50)
        sleep(1)
        m2.power(0)
finally:
    m1.stop()
    m2.stop()

