from robot_hat import Motor, PWM, Pin
from time import sleep

m0 = Motor(PWM('P13'), Pin('D4'))
m1= Motor(PWM('P12'), Pin('D5'))

try:
    while True:
        m0.speed(-50)
        m1.speed(-50)
        sleep(1)
        m0.speed(50)
        m1.speed(50)
        sleep(1)
        m0.speed(0)
        m1.speed(0)
finally:
    m0.speed(0)
    m1.speed(0)
    sleep(.1)

