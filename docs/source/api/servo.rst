class ``Servo``
=============================

**Example**

.. code-block:: python
    
    # Import Servo and PWM class
    from robot_hat import Servo, PWM

    # Create Servo object with PWM object
    p0 = PWM('P0')
    servo0 = Servo(p0)
    # or in one line
    servo1 = Servo(PWM(1))

    # Set servo to position 0, here 0 is the center position,
    # angle ranges from -90 to 90
    servo0.angle(0)

    # Sweep servo from 0 to 180 degrees
    for i in range(-90, 91):
        servo0.angle(i)
        time.sleep(0.05)

    # Servos are all controls with pulse width, some
    # from 500 ~ 2500 like most from SunFounder.
    # You can directly set the pulse width

    # Set servo to 1500 pulse width (0 degree)
    servo0.set_pwm(1500)

**API**

.. currentmodule:: robot_hat

.. autoclass:: Servo
    :special-members: __init__
    :members: