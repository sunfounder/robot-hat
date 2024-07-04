 .. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

.. _class_motor:

module ``motor``
========================================

class ``Motors``
----------------------------------------

**Example**

Initilize

.. code-block:: python
    
    # Import Motor class
    from robot_hat import Motors

    # Create Motor object
    motors = Motors()

Directly control a motor. Motor 1/2 is according to PCB mark

.. code-block:: python

    # Motor 1 clockwise at 100% speed
    motors[1].speed(100)
    # Motor 2 counter-clockwise at 100% speed
    motors[2].speed(-100)
    # Stop all motors
    motors.stop()

Setup for high level control, high level control provides functions
from simple forword, backward, left, right, stop to more complex
like joystick control, motor directions calibration, etc.

.. note:: 
    All these setup only need to run once, and will save in a config file. Next time you load Motors class, it will load from config file.

.. code-block:: python

    # Setup left and right motors
    motors.set_left_id(1)
    motors.set_right_id(2)
    # Go forward and see if both motor directions are correct
    motors.forward(100)
    # if you found a motor is running in the wrong direction
    # Use these function to correct it
    motors.set_left_reverse()
    motors.set_right_reverse()
    # Run forward again and see if both motor directions are correct
    motors.forward(100)

Now control the robot

.. code-block:: python

    import time

    motors.forward(100)
    time.sleep(1)
    motors.backward(100)
    time.sleep(1)
    motors.turn_left(100)
    time.sleep(1)
    motors.turn_right(100)
    time.sleep(1)
    motors.stop()

**API**

.. currentmodule:: robot_hat

.. autoclass:: Motors
    :show-inheritance:
    :special-members: __init__, __getitem__
    :members:

class ``Motor``
----------------------------------------

**Example**

.. code-block:: python
    
    # Import Motor class
    from robot_hat import Motor, PWM, Pin

    # Create Motor object
    motor = Motor(PWM("P13"), Pin("D4"))

    # Motor clockwise at 100% speed
    motor.speed(100)
    # Motor counter-clockwise at 100% speed
    motor.speed(-100)

    # If you like to reverse the motor direction
    motor.set_is_reverse(True)

**API**

.. currentmodule:: robot_hat

.. autoclass:: Motor
    :show-inheritance:
    :special-members: __init__
    :members:
