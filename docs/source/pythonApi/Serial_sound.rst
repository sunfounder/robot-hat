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

``class robot_hat.Serial_Sound()`` Create an sound player object with the
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

       Serial_Sound.play_route(num, str) # (0X01,str)

Const
-----

::

    CMD_HEAD = 0XAA
    QUERY_PALYSTATUS = 0X01 #Querying the Playing Status
    PLAY = 0X02 #play
    SUSPEND = 0X03 #suspended
    STOP = 0X04 #stop
    LAST = 0X05 #previous piece
    NEXT = 0X06 #next track
    APPOINT_SONG = 0X07 #Specify tracks
    APPOINT_ROUTE = 0X08 #Specify the drive letter to specify the path
    QUERY_ONLINEROUTE = 0X09 #Query online drive letter
    QUERY_PALYROUTE = 0X0A #Query play drive letter
    ROUTE = 0X0B #Set path
    QUERY_ALLSONG = 0X0C #Query total tracks
    QUERY_PALYSONG = 0X0D #Query current track
    LAST_DIR = 0X0E #Previous Directory
    NEXT_DIR = 0X0F #Next Directory
    END_PALY = 0X10 #End playing
    QUERY_DIRFIR = 0X11 #Query the first track in the catalog
    QUERY_DIRALL = 0X12 #Query catalog total tracks
    SET_VOLUME = 0X13 #Set volume
    ADD_VOLUME = 0X14 #Volume plus
    REDUCE_VOLUME = 0X15 #VOLUME DOWN
    APPOINT_SONG_INSERT = 0X16 #Specify track insertion
    MODE = 0X18
    SET_LOOP_TIME = 0X19 #Set the number of cycles
    QUERY_SONG_NAME = 0X1E #Query song short name
    APPOINT_REW = 0X22 #Rewind at specified time
    APPOINT_FAST = 0X23 #Specify time fast forward
    GET_SONG_TIME = 0X24 #Get the total time of the current track

    ROUTE_U = 0X00   #Drive letter
    ROUTE_SD = 0X01
    ROUTE_FLASH = 0X02
    MODULE_ALL_LOOP = 0X00 #model
    MODULE_SINGLE_LOOP = 0X01
    MODULE_SINGLE_STOP = 0X02
    MODULE_ALL_RANDOM = 0X03
    MODULE_DIR_LOOP = 0X04
    MODULE_DIR_RANDOM = 0X05
    MODULE_DIR_ORDER = 0X06
    MODELE_ORDER = 0X07

