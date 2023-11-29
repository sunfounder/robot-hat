.. _class_pwm:

class ``PWM``
========================================

**Example**

.. code-block:: python
    
    # Import PWM class
    from robot_hat import PWM

    # Create PWM object with numeric pin numbering and default input pullup enabled
    p0 = PWM(0)
    # Create PWM object with named pin numbering
    p1 = PWM('P1')


    # Set frequency will automatically set prescaller and period
    # This is easy for device like Buzzer or LED, which you care
    # about the frequency and pulse width percentage.
    # this usually use with pulse_width_percent function.
    # Set frequency to 1000Hz
    p0.freq(1000)
    print(f"Frequence: {p0.freq()} Hz")
    print(f"Prescaler: {p0.prescaler()}")
    print(f"Period: {p0.period()}")
    # Set pulse width to 50%
    p0.pulse_width_percent(50)

    # Or set prescaller and period, will get a frequency from:
    # frequency = PWM.CLOCK / prescaler / period
    # With this setup you can tune the period as you wish.
    # set prescaler to 64
    p1.prescaler(64)
    # set period to 4096 ticks
    p1.period(4096)
    print(f"Frequence: {p1.freq()} Hz")
    print(f"Prescaler: {p1.prescaler()}")
    print(f"Period: {p1.period()}")
    # Set pulse width to 2048 which is also 50%
    p1.pulse_width(2048)

**API**

.. currentmodule:: robot_hat

.. autoclass:: PWM
    :show-inheritance:
    :special-members: __init__
    :members: