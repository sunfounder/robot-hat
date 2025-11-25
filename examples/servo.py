from robot_hat import Servo
import time



s1 = Servo(1)

def sweep():
    while True:
        for i in range(-90, 90, 1):
            s1.angle(i)
            time.sleep(0.01)
            print(f"{i}  ", end='\r')
        
        time.sleep(1)
        for i in range(90, -90, -1):
            s1.angle(i)
            time.sleep(0.01)
            print(f"{i}  ", end='\r')
        
        time.sleep(1)

sweep()

