 .. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

class ``_Basic_class``
=========================================

``_Basic_class`` is a logger class for all class to log, so if you want to see
logs of a class, just add a debug argument to it.

**Example**

.. code-block:: python

    # See PWM log
    from robot_hat import PWM

    # init the class with a debug argument
    pwm = PWM(0, debug_level="debug")

    # run some functions and see logs
    pwm.freq(1000)
    pwm.pulse_width_percent(100)


**API**

.. currentmodule:: robot_hat.basic

.. autoclass:: _Basic_class
    :special-members: __init__
    :members: