.. _class_motor:

class ``Motor`` - motor control
===========================================

**Usage**

.. code-block:: python

    from robot_hat import Motor

    motor = Motor()                     # Create a motor object
    motor = motor.wheel(100)            # Set the motor speed to 100

**Constructors**

``class robot_hat.Motor()``: Create a motor object, you can use it to control the motors.

**Methods**

-  ``wheel`` - Control the speed and direction of the motor.

.. code-block:: python

    # The speed range is -100 to 100, and the positive and negative values represent the direction of rotation of the motor.
    motor.wheel(100)

    # The second parameter, filled with 0 or 1, is used to control a specific motor.
    motor.wheel(100,1)
