 .. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

.. _class_music:

class ``Music``
========================================

.. warning::
    * You need to add ``sudo`` when running this script, in case the speaker doesn't work.
    * :ref:`faq_speaker`.

**Example**

Initialize

.. code-block:: python

    # Import Music class
    from robot_hat import Music

    # Create a new Music object
    music = Music()

Play tones

.. code-block:: python

    # You can directly play a frequency for specific duration in seconds
    music.play_tone_for(400, 1)

    # Or use note to get the frequency
    music.play_tone_for(music.note("Middle C"), 0.5)
    # and set tempo and use beat to get the duration in seconds
    # Which make's it easy to code a song according to a sheet!
    music.tempo(120)
    music.play_tone_for(music.note("Middle C"), music.beat(1))
    
    # Here's an example playing Greensleeves
    set_volume(80)
    music.tempo(60, 1/4)

    print("Measure 1")
    music.play_tone_for(music.note("G4"), music.beat(1/8))
    print("Measure 2")
    music.play_tone_for(music.note("A#4"), music.beat(1/4))
    music.play_tone_for(music.note("C5"), music.beat(1/8))
    music.play_tone_for(music.note("D5"), music.beat(1/8 + 1/16))
    music.play_tone_for(music.note("D#5"), music.beat(1/16))
    music.play_tone_for(music.note("D5"), music.beat(1/8))
    print("Measure 3")
    music.play_tone_for(music.note("C5"), music.beat(1/4))
    music.play_tone_for(music.note("A4"), music.beat(1/8))
    music.play_tone_for(music.note("F4"), music.beat(1/8 + 1/16))
    music.play_tone_for(music.note("G4"), music.beat(1/16))
    music.play_tone_for(music.note("A4"), music.beat(1/8))
    print("Measure 4")
    music.play_tone_for(music.note("A#4"), music.beat(1/4))
    music.play_tone_for(music.note("G4"), music.beat(1/8))
    music.play_tone_for(music.note("G4"), music.beat(1/8 + 1/16))
    music.play_tone_for(music.note("F#4"), music.beat(1/16))
    music.play_tone_for(music.note("G4"), music.beat(1/8))
    print("Measure 5")
    music.play_tone_for(music.note("A4"), music.beat(1/4))
    music.play_tone_for(music.note("F#4"), music.beat(1/8))
    music.play_tone_for(music.note("D4"), music.beat(1/4))
    music.play_tone_for(music.note("G4"), music.beat(1/8))
    print("Measure 6")
    music.play_tone_for(music.note("A#4"), music.beat(1/4))
    music.play_tone_for(music.note("C5"), music.beat(1/8))
    music.play_tone_for(music.note("D5"), music.beat(1/8 + 1/16))
    music.play_tone_for(music.note("D#5"), music.beat(1/16))
    music.play_tone_for(music.note("D5"), music.beat(1/8))
    print("Measure 7")
    music.play_tone_for(music.note("C5"), music.beat(1/4))
    music.play_tone_for(music.note("A4"), music.beat(1/8))
    music.play_tone_for(music.note("F4"), music.beat(1/8 + 1/16))
    music.play_tone_for(music.note("G4"), music.beat(1/16))
    music.play_tone_for(music.note("A4"), music.beat(1/8))
    print("Measure 8")
    music.play_tone_for(music.note("A#4"), music.beat(1/8 + 1/16))
    music.play_tone_for(music.note("A4"), music.beat(1/16))
    music.play_tone_for(music.note("G4"), music.beat(1/8))
    music.play_tone_for(music.note("F#4"), music.beat(1/8 + 1/16))
    music.play_tone_for(music.note("E4"), music.beat(1/16))
    music.play_tone_for(music.note("F#4"), music.beat(1/8))
    print("Measure 9")
    music.play_tone_for(music.note("G4"), music.beat(1/4 + 1/8))
    music.play_tone_for(music.note("G4"), music.beat(1/4 + 1/8))
    print("Measure 10")
    music.play_tone_for(music.note("F5"), music.beat(1/4 + 1/8))
    music.play_tone_for(music.note("F5"), music.beat(1/8))
    music.play_tone_for(music.note("E5"), music.beat(1/16))
    music.play_tone_for(music.note("D5"), music.beat(1/8))
    print("Measure 11")
    music.play_tone_for(music.note("C5"), music.beat(1/4))
    music.play_tone_for(music.note("A4"), music.beat(1/8))
    music.play_tone_for(music.note("F4"), music.beat(1/8 + 1/16))
    music.play_tone_for(music.note("G4"), music.beat(1/16))
    music.play_tone_for(music.note("A4"), music.beat(1/8))
    print("Measure 12")
    music.play_tone_for(music.note("A#4"), music.beat(1/4))
    music.play_tone_for(music.note("G4"), music.beat(1/8))
    music.play_tone_for(music.note("G4"), music.beat(1/8 + 1/16))
    music.play_tone_for(music.note("F#4"), music.beat(1/16))
    music.play_tone_for(music.note("G4"), music.beat(1/8))
    print("Measure 13")
    music.play_tone_for(music.note("A4"), music.beat(1/4))
    music.play_tone_for(music.note("F#4"), music.beat(1/8))
    music.play_tone_for(music.note("D4"), music.beat(1/4 + 1/8))
    print("Measure 14")
    music.play_tone_for(music.note("F5"), music.beat(1/4 + 1/8))
    music.play_tone_for(music.note("F5"), music.beat(1/8))
    music.play_tone_for(music.note("E5"), music.beat(1/16))
    music.play_tone_for(music.note("D5"), music.beat(1/8))
    print("Measure 15")
    music.play_tone_for(music.note("C5"), music.beat(1/4))
    music.play_tone_for(music.note("A4"), music.beat(1/8))
    music.play_tone_for(music.note("F4"), music.beat(1/8 + 1/16))
    music.play_tone_for(music.note("G4"), music.beat(1/16))
    music.play_tone_for(music.note("A4"), music.beat(1/8))
    print("Measure 16")
    music.play_tone_for(music.note("A#4"), music.beat(1/8 + 1/16))
    music.play_tone_for(music.note("A4"), music.beat(1/16))
    music.play_tone_for(music.note("G4"), music.beat(1/8))
    music.play_tone_for(music.note("F#4"), music.beat(1/8 + 1/16))
    music.play_tone_for(music.note("E4"), music.beat(1/16))
    music.play_tone_for(music.note("F#4"), music.beat(1/8))
    print("Measure 17")
    music.play_tone_for(music.note("G4"), music.beat(1/4 + 1/8))
    music.play_tone_for(music.note("G4"), music.beat(1/4 + 1/8))

Play sound

.. code-block:: python

    # Play a sound
    music.sound_play("file.wav", volume=50)
    # Play a sound in the background
    music.sound_play_threading("file.wav", volume=80)
    # Get sound length
    music.sound_length("file.wav")

Play Music

.. code-block:: python

    # Play music
    music.music_play("file.mp3")
    # Play music in loop
    music.music_play("file.mp3", loop=0)
    # Play music in 3 times
    music.music_play("file.mp3", loop=3)
    # Play music in starts from 2 second
    music.music_play("file.mp3", start=2)
    # Set music volume
    music.music_set_volume(50)
    # Stop music
    music.music_stop()
    # Pause music
    music.music_pause()
    # Resume music
    music.music_resume()

**API**

.. currentmodule:: robot_hat

.. autoclass:: Music
    :show-inheritance:
    :special-members: __init__
    :members:
