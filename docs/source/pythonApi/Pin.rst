class ``Pin`` - control I/O pins
================================

Usage:

.. code-block:: python

    from robot_hat import Pin

    pin = Pin("D0")                      # create an Pin object from a pin
    val = pin.value()                    # read an analog value

Constructors
------------

``class robot_hat.Pin(value)`` A pin is the basic object to control I/O
pins. It has methods to set the mode of the pin (input, output, etc) and
methods to get and set the digital logic level.

Methods
-------

-  value - Read the value on the analog pin and return it. The returned
   value will be between 0 and 4095.

   .. code-block:: python

       Pin.value()

Availble pins
-------------

-  ``"D0"``
-  ``"D1"``
-  ``"D2"``
-  ``"D3"``
-  ``"D4"``
-  ``"D5"``
-  ``"D6"``
-  ``"D7"``
-  ``"D8"``
-  ``"D9"``
-  ``"SW"``
-  ``"LED"``

