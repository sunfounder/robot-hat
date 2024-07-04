 .. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

.. _on_board_mcu:

On-Board MCU
=======================

The Robot HAT comes with an AT32F413CBT7 microcontroller from Artery. It is an ARM Cortex-M4 processor with a maximum clock frequency of 200MHz. The microcontroller has 128KB of Flash memory and 32KB of SRAM.

The onboard PWM and ADC are driven by the microcontroller. 
Communication between the Raspberry Pi and the microcontroller is established via the I2C interface. 
The I2C address used for communication is 0x14 (7-bit address format).


Introduce
-----------------------

The on board MCU RESET pin is connected to Raspberry Pi GPIO 5, or ``MCURST`` for :py:class:`robot_hat.Pin`. The MCU using 7-bit address ``0x14``.

ADC
-----------------------

Register addresses is 3 byte, 0x170000 to 0x140000 are ADC channels 0 to 3.
The ADC precision is 12 bit, and the value is 0 to 4095.
See more details in :py:class:`robot_hat.ADC`.

.. table::

    +-------------------+-------------------------------+
    | Address           | Description                   |
    +===================+===============================+
    | ``0x170000``      | ADC channel 0                 |
    +-------------------+-------------------------------+
    | ``0x160000``      | ADC channel 1                 |
    +-------------------+-------------------------------+
    | ``0x150000``      | ADC channel 2                 |
    +-------------------+-------------------------------+
    | ``0x140000``      | ADC channel 3                 |
    +-------------------+-------------------------------+
    | ``0x130000``      | ADC channel 4 (Battery Level) |
    +-------------------+-------------------------------+

**Example:**

Read Channel 0 ADC value:

.. code-block:: python

    from smbus import SMBus
    bus = SMBus(1)

    # smbus only support 8 bit register address, so write 2 byte 0 first
    bus.write_word_data(0x14, 0x17, 0)
    msb = bus.read_byte(0x14)
    lsb = bus.read_byte(0x14)
    value = (msb << 8) | lsb


PWM
-----------------------

PWM have 1 byte register with 2 byte values.

Changing PWM Frequency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Frequency is defined with prescaler and period.

To set frequency first you need to define the period you want.
Like on Arduino, normaly is 255, or like PCA9685 is 4095.

CPU clock is 72MHz, Then you can calculate the prescaler from your desire frequency


    prescaler = 72MHz / (Period + 1) / Frequency - 1

Or if you don't care about the period, there's a way to calculate both period and prescaler from
frequency. See :py:func:`robot_hat.PWM.freq`.

Pulse width
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To control the channel pulse width is rather simple, just write the value to the register.

**But** what is the value? If you want to set the PWM to 50% pulse width, you need to know
exactly what the period is. Base on the above calculation, if you set the period to 4095,
then set pulse value to 2048 is about 50% pulse width.

.. table::

    +-------------------+----------------------------------+
    | Address           | Description                      |
    +===================+==================================+
    | ``0x20``          | Set PWM channel 0 **On Value**   |
    +-------------------+----------------------------------+
    | ``0x21``          | Set PWM channel 1 **On Value**   |
    +-------------------+----------------------------------+
    | ``0x22``          | Set PWM channel 2 **On Value**   |
    +-------------------+----------------------------------+
    | ``0x23``          | Set PWM channel 3 **On Value**   |
    +-------------------+----------------------------------+
    | ``0x24``          | Set PWM channel 4 **On Value**   |
    +-------------------+----------------------------------+
    | ``0x25``          | Set PWM channel 5 **On Value**   |
    +-------------------+----------------------------------+
    | ``0x26``          | Set PWM channel 6 **On Value**   |
    +-------------------+----------------------------------+
    | ``0x27``          | Set PWM channel 7 **On Value**   |
    +-------------------+----------------------------------+
    | ``0x28``          | Set PWM channel 8 **On Value**   |
    +-------------------+----------------------------------+
    | ``0x29``          | Set PWM channel 9 **On Value**   |
    +-------------------+----------------------------------+
    | ``0x2A``          | Set PWM channel 10 **On Value**  |
    +-------------------+----------------------------------+
    | ``0x2B``          | Set PWM channel 11 **On Value**  |
    +-------------------+----------------------------------+
    | ``0x2C``          | Set Motor 2 speed **On Value**   |
    +-------------------+----------------------------------+
    | ``0x2D``          | Set Motor 1 speed **On Value**   |
    +-------------------+----------------------------------+

Prescaler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Register from 0x40 is to set the PWM prescaler. ranges from 0~65535.
There are only 4 timers for all 14 channels. See `PWM Timer(IMPORTANT)`_

.. table::

    +-------------------+----------------------------------+
    | Address           | Description                      |
    +===================+==================================+
    | ``0x40``          | Set timer 0 **Prescaler**        |
    +-------------------+----------------------------------+
    | ``0x41``          | Set timer 1 **Prescaler**        |
    +-------------------+----------------------------------+
    | ``0x42``          | Set timer 2 **Prescaler**        |
    +-------------------+----------------------------------+
    | ``0x43``          | Set timer 3 **Prescaler**        |
    +-------------------+----------------------------------+

Period
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Register from 0x44 is to set the PWM period. ranges from 0~65535.
There are only 4 timers for all 14 channels. See `PWM Timer(IMPORTANT)`_

.. table::

    +-------------------+----------------------------------+
    | Address           | Description                      |
    +===================+==================================+
    | ``0x44``          | Set timer 0 **Period**           |
    +-------------------+----------------------------------+
    | ``0x45``          | Set timer 1 **Period**           |
    +-------------------+----------------------------------+
    | ``0x46``          | Set timer 2 **Period**           |
    +-------------------+----------------------------------+
    | ``0x47``          | Set timer 3 **Period**           |
    +-------------------+----------------------------------+

PWM Timer(IMPORTANT)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What is PWM Timer? PWM Timer is a tool to turn on and off the PWM channel for you.

The MCU only have 4 timers for PWM: which means you cannot set frequency on different channels
at with the same timer.

Example: if you set frequency on channel 0, channel 1, 2, 3 will be affected.
If you change channel 2 frequency, channel 0, 1, 3 will be override.

This happens like if you want to control both a passive buzzer (who changes frequency all the time)
and servo (who needs a fix frequency of 50Hz). Then you should seperate them into two different timer.

.. table::

    +---------------+-------------------+
    | Timer         | PWM Channel       |
    +===============+===================+
    | Timer 0       | 0, 1, 2, 3        |
    +---------------+-------------------+
    | Timer 1       | 4, 5, 6, 7        |
    +---------------+-------------------+
    | Timer 2       | 8, 9, 10, 11      |
    +---------------+-------------------+
    | Timer 3       | 12, 13(for motors)|
    +---------------+-------------------+

Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from smbus import SMBus
    bus = SMBus(1)

    # Set timer 0 period to 4095
    bus.write_word_data(0x14, 0x44, 4095)
    # Set frequency to 50Hz,
    freq = 50
    # Calculate prescaler
    prescaler = int(72000000 / (4095 + 1) / freq) - 1
    # Set prescaler
    bus.write_word_data(0x14, 0x40, prescaler)
    
    # Set channel 0 to 50% pulse width
    bus.write_word_data(0x14, 0x20, 2048)

Reset MCU
-----------------------------

Currently the firmware reads a fix 3 byte value, then it can return ADC values or control PWM.
Thats why ADC register need 3byte with the latter 2 byte is 0.

And if your program is interrupted in the middle of the communication, the firmware may stuck and offset the data. Even we have timeout on waiting on 3 byte datas.

If so, you need to reset the MCU. To reset it. You can use the robot_hat command:

.. code-block:: bash

    robot_hat reset_mcu

Or you can do it in your python code:

.. code-block:: python

    from robot_hat import reset_mcu
    reset_mcu()

Or you can just pull down the reset pin (GPIO 5) for 10 ms, then pull it back up for another 10ms, as that's what ``reset_mcu`` dose.

.. code-block:: python

    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.OUT)
    GPIO.output(5, GPIO.LOW)
    time.sleep(0.01)
    GPIO.output(5, GPIO.HIGH)
    time.sleep(0.01)
