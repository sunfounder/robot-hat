class ``Music`` - notes and beats
=================================

Usage:

.. code-block:: python

    from robot_hat import Music, Buzzer

    m = Music()               # create an music object
    buzzer = Buzzer("P0")
    m.tempo(120)              # set current tempo to 120 beat per minute

    # play middle C, D, E, F ,G, A, B every 1 beat.
    buzzer.play(m.note("Middle C"), m.beat(1))
    buzzer.play(m.note("Middle D"), m.beat(1))
    buzzer.play(m.note("Middle E"), m.beat(1))
    buzzer.play(m.note("Middle F"), m.beat(1))
    buzzer.play(m.note("Middle G"), m.beat(1))
    buzzer.play(m.note("Middle A"), m.beat(1))
    buzzer.play(m.note("Middle B"), m.beat(1))

Constructors
------------

``class robot_hat.Music()`` Create an Music object. This allows you to
then get or control music!

Methods
-------

-  ``note`` - get frequency of the note. Input string must be in
   Constant ``NOTE``

   .. code-block:: python

       Music().note("Middle D")
       Music().note("High A#")

-  ``beat`` - get milisecond from beats. Input value can be float, like
   ``0.5`` as half beat, or ``0.25`` as quarter beat

   .. code-block:: python

       Music().beat(0.5)
       Music().beat(0.125)

-  ``tempo`` - get/set the tempo. input value is in bmp(beat per second)

   .. code-block:: python

       Music().tempo()
       Music().tempo(120)

-  ``play_tone_for`` - Play tone.Input is note and beat,like
   ``Music.note("Middle D"), Music.beat(0.5)``

   .. code-block:: python

       Music().play_tone_for(Music.note("Middle D"), Music.beat(0.5))


