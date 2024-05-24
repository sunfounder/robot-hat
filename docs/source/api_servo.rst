 .. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

.. _class_servo:

class ``Servo``
=============================

**Example**

.. code-block:: python
    
    # Import Servo class
    from robot_hat import Servo

    # Create Servo object with PWM object
    servo0 = Servo("P0")

    # Set servo to position 0, here 0 is the center position,
    # angle ranges from -90 to 90
    servo0.angle(0)

    # Sweep servo from 0 to 90 degrees, then 90 to -90 degrees, finally back to 0
    import time
    for i in range(0, 91):
        servo0.angle(i)
        time.sleep(0.05)
    for i in range(90, -91, -1):
        servo0.angle(i)
        time.sleep(0.05)
    for i in range(-90, 1):
        servo0.angle(i)
        time.sleep(0.05)


    # Servos are all controls with pulse width, some
    # from 500 ~ 2500 like most from SunFounder.
    # You can directly set the pulse width

    # Set servo to 1500 pulse width (-90 degree)
    servo0.pulse_width_time(500)
    # Set servo to 1500 pulse width (0 degree)
    servo0.pulse_width_time(1500)
    # Set servo to 1500 pulse width (90 degree)
    servo0.pulse_width_time(2500)

**API**

.. currentmodule:: robot_hat

.. autoclass:: Servo
    :show-inheritance:
    :special-members: __init__
    :members: