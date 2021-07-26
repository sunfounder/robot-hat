class ``Joystick`` - 3-axis joystick
====================================

Usage:

.. code-block:: python

    from robot_hat import Joystick, ADC, Pin

    x_pin = ADC("A0")
    y_pin = ADC("A1")
    btn_pin = Pin("D1")

    joystick = Joystick(x_pin, y_pin, btn_pin)         # create an Joystick object from a pin
    val = joystick.read(0)                             # read an axis value
    status = joystick.read_status()                    # read the status of joystick

Constructors
------------

``class ezblock.Joystick(pin)`` Create an Joystick object associated
with the given pin. This allows you to then read values on that pin.

Methods
-------

-  read - Read the value on the given pin and return it.

   .. code-block:: python

       Joystick.read(Xpin, Ypin, Btpin)

-  read\_status - Read the value on the given pin and return it.

   .. code-block:: python

       Joystick.read_status()


