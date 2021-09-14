class ``RGB_LED`` - rgb LED
===========================

**Usage**

.. code-block:: python

    from robot_hat import PWM, RGB_LED

    r = PWM("P0")
    g = PWM("P1")
    b = PWM("P2")

    rgb = RGB_LED(r, g, b)                       # Create a RGB_LED object
    val = rgb.write('#FFFFFF')                   # Write in the color in hexadecimal.

Constructors
------------

``class robot_hat.RGB_LED(Rpin, Gpin, Bpin)``: Create a ``RGB_LED`` object associated with the given pin. This allows you set the color of RGB LED. 
Input ``Rpin``, ``Gpin``, ``Bpin`` must be ``PWM`` object from ``robot_hat.PWM``.

**Methods**


-  ``write`` - Writing a specific color to the RGB LED, the color value is represented by hexadecimal for red, green and blue (RGB). Each color has a minimum value of 0 (00 in hexadecimal) and a maximum value of 255 (FF in hexadecimal). Hexadecimal values are written with a # sign followed by three or six hexadecimal characters.

.. code-block:: python

    RGB_LED.write(color)


