class ``Ultrasonic`` - ultrasonic ranging sensor
================================================

**Usage**

.. code-block:: python

    from robot_hat import Ultrasonic, Pin

    trig = Pin("D0")
    echo = Pin("D1")

    ultrasonic = Ultrasonic(trig, echo)             # create an Ultrasonic object
    val = ultrasonic.read()                         # read an analog value

**Constructors**

``class robot_hat.Ultrasonic(trig, echo)``: Create a Ultrasonic object associated with the given pin. This allows you to then read distance value.

Methods
-------

-  ``read`` - Read distance values.

   .. code-block:: python

       Ultrasonic.read(trig, echo)


