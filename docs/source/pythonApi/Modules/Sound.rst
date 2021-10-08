class ``Sound`` - sound sensor
==============================

**Usage**

.. code-block:: python

    from robot_hat import Sound, ADC

    pin = ADC("A0")
    sound = Sound(pin)                         # create a Sound object from a pin
    val = sound.read_raw()                     # read an analog value

    average_val = sound.read_raw(time = 100)   # read an average analog value

**Constructors**

``class robot_hat.Sound(pin)``: Create a Sound object associated with the given pin. This allows you to read analog values on that pin.

**Methods**

-  ``read_raw`` - Read the value on the analog pin and return it. The returned value will be between 0 and 4095.

.. code-block:: python

    Sound.read_raw()


