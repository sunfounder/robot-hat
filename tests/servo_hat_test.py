#!/usr/bin/env python3
from robot_hat import Servo, ADC
from robot_hat.utils import reset_mcu
from time import sleep

reset_mcu()
sleep(1)

adc0 = ADC(0)
adc1 = ADC(1)
adc2 = ADC(2)
adc3 = ADC(3)
adc4 = ADC(4)


if __name__ == '__main__':
    for i in range(16):
        print(f"Servo {i} set to zero")
        Servo(i).angle(10)
        sleep(0.1)
        Servo(i).angle(0)
        sleep(0.1)
    while True:
        v0 = adc0.read()
        v1 = adc1.read()
        v2 = adc2.read()
        v3 = adc3.read()
        v4 = adc4.read()
        print(v0, v1, v2, v3, v4)
        sleep(1)
