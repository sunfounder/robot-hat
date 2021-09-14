class ``Buzzer`` - passive buzzer
=================================

**Usage**

.. code-block:: python

    from robot_hat import PWM, Buzzer, Music

    pwm = PWM("A0")                 # create a pwm object
    buzzer = Buzzer(pwm)            # create a Buzzer object with PWM object
    music = Music()                 # create music object

    buzzer.play(music.note("Low C"), music.beat(1))   # play low C for 1 beat
    buzzer.play(music.note("Middle C#"))              # play middle C sharp
    buzzer.off()                                      # turn buzzer off

**Constructors**


``class robot_hat.Buzzer(pwm)``: Create a Buzzer object associated with the given pwm object. This will allow you to control the buzzer.

**Methods**


-  ``on`` - Turn the buzzer on with a square wave.

.. code-block:: python

    Buzzer.on()

-  ``off`` - Turn the buzzer off.

.. code-block:: python

    Buzzer.off()

-  ``freq`` - Set the frequency of the square wave.

.. code-block:: python

    Buzzer.freq(frequency)

-  ``play`` - Make the buzzer sound at a specific frequency and stop at a ms delay time.

.. code-block:: python

    Buzzer.play(freq, ms)
    Buzzer.play(freq)


