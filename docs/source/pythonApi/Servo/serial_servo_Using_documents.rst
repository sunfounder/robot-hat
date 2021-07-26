Quick reference for the Serial Servo
====================================

Example
-------

-  The servo model

   .. code-block:: python

       from robot_hat import *
       import time
       ss = Serial_Servo()     # create an servo object from serial port and defaults to "/dev/ttyS0"
       servo1 = Servo(1)       #create an parameter object for ID1
       ss.run(servo1)   #Back to the original position
       servo1.angle(90)        #set servo1 rotation angle to 90°
       time.sleep(1)           #Waiting for the last instruction to complete
       ss.run(servo1)   #run servo

-  Several servo

   .. code-block:: python

       from robot_hat import *
       import time
       ss = Serial_Servo()     #create an servo object from serial port and defaults to "/dev/ttyS0"
       servo1 = Servo(1)       #create an parameter object for ID1
       servo2 = Servo(2)       #create an parameter object for ID2
       ss.run(servo1,servo2)   #Back to the original position
       servo1.angle(90)        #set servo1 rotation angle to 90°
       servo2.angle(90)        #set servo2 rotation angle to 90°
       time.sleep(1)           #Waiting for the last instruction to complete
       ss.run(servo1,servo2)   #run all servo

-  The motor model

   .. code-block:: python

       ss = Serial_Servo()     #create an servo object from serial port and defaults to "/dev/ttyS0"
       servo1 = Servo(1)       #create an parameter object for ID1
       servo2 = Servo(2)       #create an parameter object for ID2
       servo1.mode(ss.MOTOR)   #set servo1 model to motor
       servo2.mode(ss.MOTOR)   #set servo2 model to motor
       servo1.speed(50)        #set servo1 speed to 50 max is 100 and dir is Clockwise
       servo2.speed(-50)       #set servo2 speed to 50 and dir is Anti-clockwise
       ss.run(servo1,servo2)   #run all servo


