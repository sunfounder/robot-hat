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