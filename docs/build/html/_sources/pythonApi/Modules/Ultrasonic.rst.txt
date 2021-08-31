class ``Ultrasonic`` - ultrasonic ranging sensor
================================================

Usage:

.. code-block:: python

    from robot_hat import Ultrasonic, Pin

    trig = Pin("D0")
    echo = Pin("D1")

    ultrasonic = Ultrasonic(trig, echo)             # create an  Ultrasonic object from  pin
    val = ultrasonic.read()                         # read an analog value

Constructors
------------

``class robot_hat.Ultrasonic(trig, echo)`` Create an Ultrasonic object
associated with the given pin. This allows you to then read distance
values.

Methods
-------

-  read - Read the value on the analog pin and return it. The returned
   value will be between 0 and 4095.

   .. code-block:: python

       Ultrasonic.read(trig, echo)


