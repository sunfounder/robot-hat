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