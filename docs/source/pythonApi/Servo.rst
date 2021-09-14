class ``Servo`` - 3-wire pwm servo driver
=========================================

**Usage**

.. code-block:: python

    from robot_hat import Servo, PWM

    pin = PWM("P0")
    ser = Servo(pin)                      # create a Servo object
    val = ser.angle(60)                   # set the servo angle

**Constructors**

``class robot_hat.Servo(pin)``: Create a Servo object associated with the given pin. This allows you to set the angle values.

Methods
-------

-  ``angle`` - set the angle values between -90 and 90.

.. code-block:: python

    Servo.angle(90)


