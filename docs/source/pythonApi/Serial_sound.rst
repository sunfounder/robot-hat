class ``Serial_Sound`` - serial sound player
============================================

Usage:

.. code-block:: python

    from robot_hat import *

    ss = Serial_Sound(port="/dev/ttyS0")                     # create an sound player object from serial port and defaults to "/dev/ttyS0"
    ss.set_route(ss.ROUTE_SD)                  #set route SD card
    ss.play(0X00, 0X01)                    # play 01 file

Constructors
------------

``class ezblock.Serial_Sound()`` Create an sound player object with the
serial port.This allows you to play file.

Methods
-------

-  init - init the uart.

   .. code-block:: python

       Serial_Sound.init(port="/dev/ttyS0")  #defaults to "/dev/ttyS0"

-  write - send data to module.

   .. code-block:: python

       Serial_Sound.write(*data)

-  read - read data.

   .. code-block:: python

       Serial_Sound.read()

-  read\_data - read data from module.

   .. code-block:: python

       Serial_Sound.read_data(cmd)

-  play - set file to play.

   .. code-block:: python

       Serial_Sound.play(*num)  #File names are 8 bits high and 8 bits low

-  set\_route - set play route

   .. code-block:: python

       Serial_Sound.set_route(num) 

-  set\_module - set play module

   .. code-block:: python

       Serial_Sound.set_module(num) 

-  set\_loop\_time - set loop time

   .. code-block:: python

       Serial_Sound.set_loop_time(*num) #times are 8 bits high and 8 bits low

-  set\_volume

   .. code-block:: python

       Serial_Sound.set_volume(num) 

-  play\_route - appoint disc and route play

   .. code-block:: python

       Serial_Sound.play_route(num, str) # (0X01,/广告*/小米*???)

Const
-----

::

    CMD_HEAD = 0XAA
    QUERY_PALYSTATUS = 0X01 #查询播放状态
    PLAY = 0X02 #播放
    SUSPEND = 0X03 #暂停
    STOP = 0X04 #停止
    LAST = 0X05 #上一曲
    NEXT = 0X06 #下一曲
    APPOINT_SONG = 0X07 #指定曲目
    APPOINT_ROUTE = 0X08 #指定盘符指定路径
    QUERY_ONLINEROUTE = 0X09 #查询在线盘符
    QUERY_PALYROUTE = 0X0A #查询播放盘符
    ROUTE = 0X0B #设置路径
    QUERY_ALLSONG = 0X0C #查询总曲目
    QUERY_PALYSONG = 0X0D #查询当前曲目
    LAST_DIR = 0X0E #上一个目录
    NEXT_DIR = 0X0F #下一个目录
    END_PALY = 0X10 #结束播放
    QUERY_DIRFIR = 0X11 #查询目录首曲目
    QUERY_DIRALL = 0X12 #查询目录总曲目
    SET_VOLUME = 0X13 #设置音量
    ADD_VOLUME = 0X14 #音量加
    REDUCE_VOLUME = 0X15 #音量减
    APPOINT_SONG_INSERT = 0X16 #指定曲目插播
    MODE = 0X18
    SET_LOOP_TIME = 0X19 #设置循环次数
    QUERY_SONG_NAME = 0X1E #查询歌曲短名称
    APPOINT_REW = 0X22 #指定时间快退
    APPOINT_FAST = 0X23 #指定时间快进
    GET_SONG_TIME = 0X24 #获取当前曲目总时间

    ROUTE_U = 0X00   #盘符
    ROUTE_SD = 0X01
    ROUTE_FLASH = 0X02
    MODULE_ALL_LOOP = 0X00 #模式
    MODULE_SINGLE_LOOP = 0X01
    MODULE_SINGLE_STOP = 0X02
    MODULE_ALL_RANDOM = 0X03
    MODULE_DIR_LOOP = 0X04
    MODULE_DIR_RANDOM = 0X05
    MODULE_DIR_ORDER = 0X06
    MODELE_ORDER = 0X07

