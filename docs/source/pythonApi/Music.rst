class ``Music`` - notes and beats
=================================

**Usage**

.. code-block:: python

    from robot_hat import Music, Buzzer

    m = Music()        # create a music object
    buzzer = Buzzer("P0")
    m.tempo(120)          # set current tempo to 120 beat per minute

    # play middle C, D, E, F ,G, A, B every 1 beat.
    buzzer.play(m.note("Middle C"), m.beat(1))
    buzzer.play(m.note("Middle D"), m.beat(1))
    buzzer.play(m.note("Middle E"), m.beat(1))
    buzzer.play(m.note("Middle F"), m.beat(1))
    buzzer.play(m.note("Middle G"), m.beat(1))
    buzzer.play(m.note("Middle A"), m.beat(1))
    buzzer.play(m.note("Middle B"), m.beat(1))

    song = './music/test.wav'
    
    m.music_set_volume(80)
    print('Music duration',m.sound_length(file_name))
    m.sound_play(song)

**Constructors**

``class robot_hat.Music()``: Create a Music object. This allows you to then get or control music!

**Methods**

-  ``note`` - Gets the frequency of the note. The input string must be the constant ``NOTE``.

.. code-block:: python

    Music.note("Middle D")
    Music.note("High A#")

-  ``beat`` - Get milisecond from beats. Input value can be float, like ``0.5`` as half beat, or ``0.25`` as quarter beat.

.. code-block:: python

    Music.beat(0.5)
    Music.beat(0.125)

-  ``tempo`` - Get/set the tempo, input value is in bmp(beat per second).

.. code-block:: python

    Music.tempo()
    Music.tempo(120)

-  ``play_tone_for`` - Play tone. Input is note and beat, like ``Music.note("Middle D"), Music.beat(0.5)``.

.. code-block:: python

    Music.play_tone_for(Music.note("Middle D"), Music.beat(0.5))

-  ``sound_play`` - Play music files.

.. code-block:: python
    
    sound_play(file_name)

-  ``background_music`` - Background music playback (file name, number of loops, starting position of music file, volume).

.. code-block:: python

    background_music(file_name, loops=-1, start=0.0, volume=50)

-  ``music_set_volume`` - Set volume
    
.. code-block:: python

    music_set_volume(value=50)

-  ``music_stop`` - stop
    
.. code-block:: python

    music_stop()

-  ``music_pause`` - pause
    
.. code-block:: python

    music_pause()

-  ``music_unpause`` - unpause
    
.. code-block:: python

    music_unpause()

-  ``sound_length`` - Return the duration of the music file.
    
.. code-block:: python

    len = sound_length(file_name)


