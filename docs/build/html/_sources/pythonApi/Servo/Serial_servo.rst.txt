class ``Serial_Servo`` - serial servo driver
============================================

Usage:

.. code-block:: python

    from robot_hat import *

    import time
    ss = Serial_Servo(*)             # create an servo object from serial port and defaults to "/dev/ttyS0"
    ss.write_angle(0XFE,0,500)       # set the servo angle and running time
    time.sleep(1)
    ss.write_angle(0XFE,90,500)

Constructors
------------

``class robot_hat.Serial_Servo()`` Create an Servo object associated with
serial port. This allows you to set the angle values.

Methods
-------

-  init - init the uart.

   .. code-block:: python

       Serial_Servo.init(*)  #defaults to "/dev/ttyS0"

-  print\_hex\_list - output hex list

   .. code-block:: python

       Serial_Servo.print_hex_list(li)

-  to\_hex\_list - convert hex list

   .. code-block:: python

       Serial_Servo.to_hex_list(h)

-  flat\_list - Decomposition of multiple lists

   .. code-block:: python

       Serial_Servo.flat_list(li)

-  write

   .. code-block:: python

       Serial_Servo.write(id, cmd_type, data=[])

-  read

   .. code-block:: python

       Serial_Servo.read()

-  ping

   .. code-block:: python

       Serial_Servo.ping(id)

-  read\_data

   .. code-block:: python

       Serial_Servo.read_data(id, cmd, num)

-  write\_data

   .. code-block:: python

       Serial_Servo.write_data(id, cmd, value)

-  reg\_write

   .. code-block:: python

       Serial_Servo.reg_write(id, cmd, value)

-  action

   .. code-block:: python

       Serial_Servo.action()

-  sync\_write

   .. code-block:: python

       Serial_Servo.sync_write(id, cmd=[], *value)

-  reset

   .. code-block:: python

       Serial_Servo.reset(id)

-  write\_id - set id

   .. code-block:: python

       Serial_Servo.write_id(id)

-  convert\_angle\_time

   .. code-block:: python

       Serial_Servo.convert_angle_time(angle, time_run)

-  write\_angle

   .. code-block:: python

       Serial_Servo.write_angle(id, angle, time_run)    #angle rangle is 0-270

-  write\_all\_angle - Write several angles to several ID

   .. code-block:: python

       Serial_Servo.write_all_angle(*servos)

-  set\_mode

   .. code-block:: python

       Serial_Servo.set_mode(id, num)   #0X00 is motor mode 0X01 is servo mode

-  set\_motor\_dir

   .. code-block:: python

       Serial_Servo.set_motor_dir(id, num) #0X00 is counterclockwise 0X01 is clockwise

-  set\_motor\_speed

   .. code-block:: python

       Serial_Servo.set_motor_dir(id, num)  #speed rangle is 0-100

-  run - Write several angles to several ID

   .. code-block:: python

       Serial_Servo.run(*servos)

class Servo - Parameter judgement
=================================

Methods
-------

-  id

   .. code-block:: python

       Servo.id(*value)

-  angle

   .. code-block:: python

       Servo.angle(*value)

-  time

   .. code-block:: python

       Servo.time(*value)

-  mode

   .. code-block:: python

       Servo.mode(*value)

-  speed

   .. code-block:: python

       Servo.speed(*value)

Const
-----

::

    DATA_HEAD = [0xFF, 0xFF]
    RECEIVE_HEAD = [0xFF, 0xF5]

    PING = 0x01  # Query steering gear/Quick query steering gear status
    READ_DATA = 0x02  # Query the data of the specified address
    WRITE_DATA = 0x03  # Write data to the specified address
    REG_WRITE = 0x04  # (Asynchronous writing) Pre-write data to the specified address, and execute it after receiving the ACTION command. It is mainly used to control multiple servos to enable the servos to start at the same time
    ACTION = 0x05  # (Execute asynchronous write) Trigger execution of REG WRITE instruction
    RESET = 0x06  # Restore the register to the factory setting value
    SYNC_WRITE = 0x83  #(Synchronous Write)

    VERSION = 0x03  # 2 byte Record the servo software version information, the format is vA.B such as v1.28 =0x011C
    SERVO_ID = 0x05  # Servo ID number, valid range: 1~250 Note: 254 is the broadcast ID Uint8 default: 1
    PROTECT_TIME = 0x06  # Unit: /S The servo is blocked for a period of time to protect Uint8 default: 3
    MIN_ANGLE = 0x09  # 2 byte Minimum angle limit Uint16 default: 0
    MAX_ANGLE = 0x0B  # 2 byte Maximum angle limit Uint16 default: 4095
    MAX_TORQUE = 0x10  # 2 byte Maximum torque Uint16 default: 800
    SPEED = 0x12  # Speed ​​adjustment Uint8 default: 30
    UNLOAD = 0x13  # Uninstall condition Uint8 default: 0
    MID_POS = 0x14  # 2 byte position adjustment offset, positive number is adjusted to 4095 direction, negative number is adjusted to 0 direction Int16 default: 0
    SET_POS_1 = 0x16  # Set target location one
    SET_POS_2 = 0x18
    SET_POS_3 = 0x1A
    MODE = 0x3F # Servo/motor mode
    MOTOR_DIR = 0x40 # Motor mode direction
    TORQUE_SWITCH = 0x28 # Torque switch 0: Torque off Non 0: Torque on
    TARGET_POS = 0x2A # target location
    TIME_RUN = 0x2C # 2 byte running time
    CURRENT = 0x2E # 2 byte current current
    LOCK = 0x30 # Lock sign (emergency stop)
    CURRENT_POS = 0x38 # current position
    SPEED_RUN = 0x3A # Running speed
    RUN_POS_1 = 0x3C # Run target location one
    RUN_POS_2 = 0x3D # Run target position two
    RUN_POS_3 = 0x3E # Run target position three
    SPEED_ADJ = 0x41 # 2 byte speed adjustment

    BROADCAST_ID = 0xFE
    MOTOR = 0x00
    SERVO = 0x01

