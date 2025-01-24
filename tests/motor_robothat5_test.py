from robot_hat import Motor, PWM, Pin
from time import sleep

m0 = Motor(PWM('P12'), PWM('P13'), mode=2)
m1 = Motor(PWM('P14'), PWM('P15'), mode=2)
m2 = Motor(PWM('P16'), PWM('P17'), mode=2)
m3 = Motor(PWM('P18'), PWM('P19'), mode=2)


try:
    while True:
        m0.speed(-50)
        m1.speed(-50)
        m2.speed(-50)
        m3.speed(-50)
        sleep(1)
        m0.speed(50)
        m1.speed(50)
        m2.speed(50)
        m3.speed(50)
        sleep(1)
        m0.speed(0)
        m1.speed(0)
        m2.speed(0)
        m3.speed(0)
finally:
    m0.speed(0)
    m1.speed(0)
    m2.speed(0)
    m3.speed(0)
    sleep(.1)

