Hardware Introduction
=========================

.. image:: img/picar_x_pic7.png

**Left/Right Motor Port**
    * 2-channel motor pins, left motor port is connected to GPIO 4, right motor port connected to GPIO 5.
    * API: :ref:`class_motor`, ``0`` for left motor port, ``1`` for right motor port.

**I2C Pin**
    * 2-channel I2C Pins from Raspberry Pi.
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

**Bluetooth Indicator**
    * The Bluetooth indicator keeps turning on at a well Bluetooth connection, blink at a Bluetooth disconnection, blink fast at a signal transmission.    

**Battery Indicator**
    * The voltage ranging above 7.8V, two LEDs light up; ranging 6.7V~7.8V, one LED turns on; ranging below 6.7V, all LEDs turn off.

**LED**
    * Set by your program. (Outputting 1 turns the LED on; Outputting 0 turns it off.)
    * API: :ref:`class_pin`, you can use ``Pin("LED")`` to define it.

**RST Button**
    * Short pressing RST Button causes program resetting.
    * Long press RST Button till the LED lights up then release, and you will disconnect the Bluetooth.

**USR Button**
    * The functions of USR Button can be set by your programming. (Pressing down leads to a input “0”; releasing produces a input “1”. ) 
    * API: :ref:`class_pin`, you can use ``Pin("SW")`` to define it.




