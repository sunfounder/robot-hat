from robot_hat import Robot,PWM,Servo,Music
from robot_hat.utils import reset_mcu
from time import sleep

reset_mcu()
sleep(0.01)


def fuc():
    rubo = Robot([10,11,12],3,init_angles=[10,45,-45])


if __name__ == "__main__":
    fuc()
