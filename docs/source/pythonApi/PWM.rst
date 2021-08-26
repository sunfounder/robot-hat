class ``PWM`` - pulse width modulation
======================================

Usage:

.. code-block:: python

    from robot_hat import PWM

    pwm = PWM('P0')                    # create an pwm object from a pin
    pwm.freq(50)                       # set freq 50Hz
    pwm.prescaler(2)                   # set prescaler 
    pwm.period(100)                    # set period 

    pwm.pulse_width(10)                # set pulse_width 
    pwm.pulse_width_percent(50)        # set pulse_width_percent 

Constructors
------------

``class robot_hat.PWM(channel)`` Create an PWM object associated with the
given pin. This allows you set up the pwm function on that pin.

Methods
-------

-  freq - set the pwm channel freq.

   .. code-block:: python

       PWM.freq(50)

-  prescaler - set the pwm channel prescaler.

   .. code-block:: python

       PWM.prescaler(50)

-  period - set the pwm channel period.

   .. code-block:: python

       PWM.period(100)

-  pulse\_width - set the pwm channel pulse\_width.

   .. code-block:: python

       PWM.pulse_width(10)

-  pulse\_width\_percent - set the pwm channel pulse\_width\_percent.

   .. code-block:: python

       PWM.pulse_width_percent(50)


