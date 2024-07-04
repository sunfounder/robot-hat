 .. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

module ``modules``
==================================================

.. currentmodule:: robot_hat.modules

class ``Ultrasonic``
-----------------------------------------

    **Example**

    .. code-block:: python

        # Import Ultrasonic and Pin class
        from robot_hat import Ultrasonic, Pin

        # Create Motor object
        us = Ultrasonic(Pin("D2"), Pin("D3"))

        # Read distance
        distance = us.read()
        print(f"Distance: {distance}cm")

    **API**

    .. autoclass:: Ultrasonic
        :special-members: __init__
        :members:

class ``ADXL345``
-----------------------------------------

    **Example**

    .. code-block:: python

        # Import ADXL345 class
        from robot_hat import ADXL345

        # Create ADXL345 object
        adxl = ADXL345()
        # or with a custom I2C address
        adxl = ADXL345(address=0x53)

        # Read acceleration of each axis
        x = adxl.read(adxl.X)
        y = adxl.read(adxl.Y)
        z = adxl.read(adxl.Z)
        print(f"Acceleration: {x}, {y}, {z}")

        # Or read all axis at once
        x, y, z = adxl.read()
        print(f"Acceleration: {x}, {y}, {z}")
        # Or print all axis at once
        print(f"Acceleration: {adxl.read()}")

    **API**

    .. autoclass:: robot_hat.ADXL345
        :show-inheritance:
        :special-members: __init__
        :members:

class ``RGB_LED``
-----------------------------------------

    **Example**

    .. code-block:: python

        # Import RGB_LED and PWM class
        from robot_hat import RGB_LED, PWM

        # Create RGB_LED object for common anode RGB LED
        rgb = RGB_LED(PWM(0), PWM(1), PWM(2), common=RGB_LED.ANODE)
        # or for common cathode RGB LED
        rgb = RGB_LED(PWM(0), PWM(1), PWM(2), common=RGB_LED.CATHODE)

        # Set color with 24 bit int
        rgb.color(0xFF0000) # Red
        # Set color with RGB tuple
        rgb.color((0, 255, 0)) # Green
        # Set color with RGB List
        rgb.color([0, 0, 255]) # Blue
        # Set color with RGB hex string starts with “#”
        rgb.color("#FFFF00") # Yellow

    **API**

    .. autoclass:: robot_hat.RGB_LED
        :special-members: __init__
        :members:

class ``Buzzer``
-----------------------------------------

    **Example**

    Imports and initialize

    .. code-block:: python

        # Import Buzzer class
        from robot_hat import Buzzer
        # Import Pin for active buzzer
        from robot_hat import Pin
        # Import PWM for passive buzzer
        from robot_hat import PWM
        # import Music class for tones
        from robot_hat import Music
        # Import time for sleep
        import time
    
        music = Music()
        # Create Buzzer object for passive buzzer
        p_buzzer = Buzzer(PWM(0))
        # Create Buzzer object for active buzzer
        a_buzzer = Buzzer(Pin("D0"))

    Active buzzer beeping

    .. code-block:: python

        while True:
            a_buzzer.on()
            time.sleep(0.5)
            a_buzzer.off()
            time.sleep(0.5)
    
    Passive buzzer Simple usage

    .. code-block:: python

        # Play a Tone for 1 second
        p_buzzer.play(music.note("C3"), duration=1)
        # take adventage of the music beat as duration
        # set song tempo of the beat value
        music.tempo(120, 1/4)
        # Play note with a quarter beat
        p_buzzer.play(music.note("C3"), music.beat(1/4))

    Passive buzzer Manual control

    .. code-block:: python

        # Play a tone
        p_buzzer.play(music.note("C4"))
        # Pause for 1 second
        time.sleep(1)
        # Play another tone
        p_buzzer.play(music.note("C5"))
        # Pause for 1 second
        time.sleep(1)
        # Stop playing
        p_buzzer.off()


    Play a song! Baby shark!

    .. code-block:: python

        music.tempo(120, 1/4)

        # Make a Shark-doo-doo function as is all about it
        def shark_doo_doo():
            p_buzzer.play(music.note("C5"), music.beat(1/8))
            p_buzzer.play(music.note("C5"), music.beat(1/8))
            p_buzzer.play(music.note("C5"), music.beat(1/8))
            p_buzzer.play(music.note("C5"), music.beat(1/16))
            p_buzzer.play(music.note("C5"), music.beat(1/16 + 1/16))
            p_buzzer.play(music.note("C5"), music.beat(1/16))
            p_buzzer.play(music.note("C5"), music.beat(1/8))

        # loop any times you want from baby to maybe great great great grandpa!
        for _ in range(3):
            print("Measure 1")
            p_buzzer.play(music.note("G4"), music.beat(1/4))
            p_buzzer.play(music.note("A4"), music.beat(1/4))
            print("Measure 2")
            shark_doo_doo()
            p_buzzer.play(music.note("G4"), music.beat(1/8))
            p_buzzer.play(music.note("A4"), music.beat(1/8))
            print("Measure 3")
            shark_doo_doo()
            p_buzzer.play(music.note("G4"), music.beat(1/8))
            p_buzzer.play(music.note("A4"), music.beat(1/8))
            print("Measure 4")
            shark_doo_doo()
            p_buzzer.play(music.note("C5"), music.beat(1/8))
            p_buzzer.play(music.note("C5"), music.beat(1/8))
            print("Measure 5")
            p_buzzer.play(music.note("B4"), music.beat(1/4))
            time.sleep(music.beat(1/4))



    **API**

    .. autoclass:: robot_hat.Buzzer
        :special-members: __init__
        :members:


class ``Grayscale_Module``
-----------------------------------------

    **Example**

    .. code-block:: python

        # Import Grayscale_Module and ADC class
        from robot_hat import Grayscale_Module, ADC
        
        # Create Grayscale_Module object, reference should be calculate from the value reads on white
        # and black ground, then take the middle as reference
        gs = Grayscale_Module(ADC(0), ADC(1), ADC(2), reference=2000)
        
        # Read Grayscale_Module datas
        datas = gs.read()
        print(f"Grayscale Module datas: {datas}")
        # or read a specific channel
        l = gs.read(gs.LEFT)
        m = gs.read(gs.MIDDLE)
        r = gs.read(gs.RIGHT)
        print(f"Grayscale Module left channel: {l}")
        print(f"Grayscale Module middle channel: {m}")
        print(f"Grayscale Module right channel: {r}")

        # Read Grayscale_Module simple states
        state = gs.read_status()
        print(f"Grayscale_Module state: {state}")

    **API**

    .. autoclass:: robot_hat.Grayscale_Module
        :special-members: __init__
        :members:
