.. _class_pin:


class ``Pin`` - control I/O pins
================================

**Usage**

.. code-block:: python

    from robot_hat import Pin

    pin = Pin("D0")                      # create an Pin object from a pin
    val = pin.value()                    # read the value on the digital pin

    pin.value(0)                         # set gpio to low level

**Constructors**

``class robot_hat.Pin(value)`` 
A pin is the basic object to control I/O pins. It has methods to set the mode of the pin (input, output, etc) and methods to get and set the digital logic level.

**Methods**

-  ``value`` - Read or set the value on the digital pin, the value is 0/1.

.. code-block:: python

    Pin.value() #Without parameters, read gpio level, high level returns 1, low level returns

    Pin.value(0)  # set to low level    
    Pin.value(1)  # set to high level

-  Set the value to the digital pin, same as ``value``.

.. code-block:: python

    Pin.on() # set to high level
    #off() - set to low level
    #high() - set to high level
    #low() - set to low level

-  ``mode`` - Setup gpio mode to IN/OUT.

.. code-block:: python
    
    Pin.mode(GPIO.IN)  # set gipo to INPUT mode

**Availble Pins**

-  ``"D0"``: The Digital pin 0.
-  ``"D1"``: The Digital pin 1.
-  ``"D2"``: The Digital pin 2.
-  ``"D3"``: The Digital pin 3.
-  ``"D4"``: The left motor pin.
-  ``"D5"``: The right motor pin.
-  ``"D6"``
-  ``"D7"``
-  ``"D8"``
-  ``"D9"``
-  ``"SW"``: The USR button.
-  ``"LED"``: The LED on the board.

