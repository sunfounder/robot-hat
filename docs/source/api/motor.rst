class ``Motor``
========================================

**Example**

.. code-block:: python
    
    # Import Motor class
    from robot_hat import Motor

    # Create Motor object
    motor = Motor()

    # Go forward
    motor.wheel(100, 0)
    motor.wheel(100, 1)

    # Go backward
    motor.wheel(-100, 0)
    motor.wheel(-100, 1)

    # Turn left or right depend on how your motor setup
    motor.wheel(100, 0)
    motor.wheel(-100, 1)
    # or like this
    motor.wheel(-100, 0)
    motor.wheel(100, 1)

**API**

.. currentmodule:: robot_hat

.. autoclass:: Motor
    :special-members: __init__
    :members: