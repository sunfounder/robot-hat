# from robot_hat import PWM
# import time

# pwm = PWM(0)

# pwm.freq(50)
# pwm.period(4095)
# prescaler = pwm.CLOCK / 50 / 4095
# pwm.prescaler(prescaler)
# pwm.pulse_width_percent(50)
# time.sleep(1)

# ---------------------------------
# from robot_hat import Servo
# import time

# for i in range(9):
#     servo = Servo(i)
#     servo.angle(-20)

# ---------------------------------

from robot_hat import Servo
from time import sleep

servos = [Servo(i) for i in range(12)]

while True:
    for servo in servos:
        servo.angle(-20)
        sleep(0.01)
    for servo in servos:
        servo.angle(20)
        sleep(0.01)
