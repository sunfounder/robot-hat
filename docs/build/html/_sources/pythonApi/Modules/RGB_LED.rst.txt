class ``RGB_LED`` - rgb LED
===========================

Usage:

.. code-block:: python

    from robot_hat import PWM, RGB_LED

    r = PWM("P0")
    g = PWM("P1")
    b = PWM("P2")

    rgb = RGB_LED(r, g, b)                       # create an RGB_LED object from a pin
    val = rgb.write('#FFFFFF')                   # write value of value

Constructors
------------

``class robot_hat.RGB_LED(Rpin, Gpin, Bpin)`` Create an RGB\_LED object
associated with the given pin. This allows you set the color of an RGB
LED module. Input ``Rpin``, ``Gpin``, ``Bpin`` must be ``PWM`` object
from ``ezblock.PWM``.

Methods
-------

-  write - Read the value on the analog pin and return it. The returned
   value will be between 0 and 4095.

   .. code-block:: python

       RGB_LED.write(color)


