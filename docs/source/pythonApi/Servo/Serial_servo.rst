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

``class ezblock.Serial_Servo()`` Create an Servo object associated with
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

       Serial_Servo.set_mode(id, num)   #0X00为电机模式 0X01为舵机模式

-  set\_motor\_dir

   .. code-block:: python

       Serial_Servo.set_motor_dir(id, num) #0X00为逆时针 0X01为顺时针

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

    PING = 0x01  # 查询舵机/快速查询舵机状态
    READ_DATA = 0x02  # 查询指定地址的数据
    WRITE_DATA = 0x03  # 向指定地址写数据
    REG_WRITE = 0x04  # (异步写) 向指定地址预写数据，等收到 ACTION 指令后才执行，主要用于控制多个舵机 时能让舵机同时启动
    ACTION = 0x05  # (执行异步写) 触发执行 REG WRITE 指令
    RESET = 0x06  # 把寄存器恢复为出厂设定值
    SYNC_WRITE = 0x83  #(同步写)

    VERSION = 0x03  # 2 byte 记录舵机软件版本信息, 格式为 vA.B 如 v1.28 =0x011C
    SERVO_ID = 0x05  # 舵机自身 ID 号，有效范围:1~250 注: 254 为广播 ID Uint8 default: 1
    PROTECT_TIME = 0x06  # 单位:/S 舵机堵转一段时间后保护 Uint8 default: 3
    MIN_ANGLE = 0x09  # 2 byte 最小角度限制 Uint16 default: 0
    MAX_ANGLE = 0x0B  # 2 byte 最大角度限制 Uint16 default: 4095
    MAX_TORQUE = 0x10  # 2 byte 最大扭矩 Uint16 default: 800
    SPEED = 0x12  # 速度调整 Uint8 default: 30
    UNLOAD = 0x13  # 卸载条件 Uint8 default: 0
    MID_POS = 0x14  # 2 byte 位置调整偏移量，正数往 4095 方向调整， 负数往 0 方向调整 Int16 default: 0
    SET_POS_1 = 0x16  # 设定目标位置一
    SET_POS_2 = 0x18
    SET_POS_3 = 0x1A
    MODE = 0x3F # 舵机/电机模式
    MOTOR_DIR = 0x40 # 电机模式方向
    TORQUE_SWITCH = 0x28 # 扭矩开关 0:扭矩关闭 非 0:扭矩打开
    TARGET_POS = 0x2A # 目标位置
    TIME_RUN = 0x2C # 2 byte 运行时间
    CURRENT = 0x2E # 2 byte 当前电流
    LOCK = 0x30 # 锁标志(急 停)
    CURRENT_POS = 0x38 # 当前位置
    SPEED_RUN = 0x3A # 运行速度
    RUN_POS_1 = 0x3C # 运行目标位置一
    RUN_POS_2 = 0x3D # 运行目标位置二
    RUN_POS_3 = 0x3E # 运行目标位置三
    SPEED_ADJ = 0x41 # 2 byte 速度调整

    BROADCAST_ID = 0xFE
    MOTOR = 0x00
    SERVO = 0x01

