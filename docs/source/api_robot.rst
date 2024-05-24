 .. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

.. _class_robot:

class ``Robot``
========================================

**Example**

.. code-block:: python

    # Import Robot class
    from robot import Robot

    # Create a robot(PiSloth)
    robot = Robot(pin_list=[0, 1, 2, 3], name="pisloth")

    robot.move_list["forward"] = [
        [0, 40, 0, 15],
        [-30, 40, -30, 15],
        [-30, 0, -30, 0],

        [0, -15, 0, -40],
        [30, -15, 30, -40],
        [30, 0, 30, 0],
        ]
    
    robot.do_action("forward", step=3, speed=90)

**API**

.. currentmodule:: robot_hat

.. autoclass:: Robot
    :show-inheritance:
    :special-members: __init__
    :members: