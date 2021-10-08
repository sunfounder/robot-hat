Hardware Introduction
=========================

.. image:: img/picar_x_pic7.png

**Left/Right Motor Port**
    * 2-channel XH2.54 motor ports.
    * The left port is connected to GPIO 4 and the right port is connected to GPIO 5.
    * API: :ref:`class_motor`, ``0`` for left motor port, ``1`` for right motor port.

**I2C Pin**
    * 2-channel I2C pins from Raspberry Pi.
    * API: :ref:`class_i2c`

**PWM Pin**
    * 12-channel PWM pins, P0-P12.
    * API: :ref:`class_pwm`

**ADC Pin**
    * 4-channel ADC pins, A0-A3.
    * API: :ref:`class_adc`

**Digital Pin**
    * 4-channel digital pins, D0-D3.
    * API: :ref:`class_pin`

**Battery Indicator**
    * Two LEDs light up when the voltage is higher than 7.8V.
    * One LED lights up in the 6.7V to 7.8V range. 
    * Below 6.7V, both LEDs turn off.

**LED**
    * Set by your program. (Outputting 1 turns the LED on; Outputting 0 turns it off.)
    * API: :ref:`class_pin`, you can use ``Pin("LED")`` to define it.

**RST Button**
    * Short pressing RST Button causes program resetting.
    * Long press RST Button till the LED lights up then release, and you will disconnect the Bluetooth.

**USR Button**
    * The functions of USR Button can be set by your programming. (Pressing down leads to a input “0”; releasing produces a input “1”. ) 
    * API: :ref:`class_pin`, you can use ``Pin("SW")`` to define it.

**Power Switch**
    * Turn on/off the power of the robot HAT.
    * When you connect power to the power port, the Raspberry Pi will boot up. However, you will need to switch the power switch to ON to enable Robot HAT.

**Power Port**
    * 7-12V PH2.0 2pin power input.
    * Powering the Raspberry Pi and Robot HAT at the same time.

**Bluetooth Module**
    * Since the Raspberry Pi comes with Bluetooth in slave mode, there will be pairing problems when connecting with cell phones. To make it easier for the Raspberry Pi to connect to the Ezblock Studio, we added a separate Bluetooth module.
    * Ezblock Studio is a custom graphical programming application developed by SunFounder for Raspberry Pi, for more information please refer to: `Ezblock Studio 3 <https://docs.sunfounder.com/projects/ezblock3/en/latest/>`_.


**Bluetooth Indicator**
    * The Bluetooth indicator keeps turning on at a well Bluetooth connection, blink at a Bluetooth disconnection, blink fast at a signal transmission.    



