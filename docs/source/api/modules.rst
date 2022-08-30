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
        us = Ultrasonic(Pin(D2), Pin(D3))

        # Read distance
        distance = us.read()
        print(f"Distance: {distance}cm")

    **API**

    .. autoclass:: Ultrasonic
        :special-members: __init__
        :members:

class ``DS18X20``
---------------------------------------------

    **Example**

    .. code-block:: python

        # Import DS18X20 class
        from robot_hat import DS18X20

        # Create DS18X20 object
        ds = DS18X20()

        # Simply Read temperature
        temperature = ds.read()
        print(f"Celsuius Temperature: {temperature}°C")
        temperature = ds.read(ds.FAHRENHEIT)
        print(f"Fahrenheit Temperature: {temperature}°F")

        # If there are more than one sensor, you can read them all
        temperatures = ds.read()
        for i, temp in enumerate(temperatures):
            print(f"Sensor {i}: {temp}°C")

        # Or do it manually
        # Scan all sensors
        sensor_roms = ds.scan()
        for rom in sensor_roms:
            # Read temperature
            temperature = ds.read_temp(rom)
            print(f"Sensor {rom}: {temperature}°C")

    **API**

    .. autoclass:: robot_hat.DS18X20
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

        # Read acceleration
        x = adxl.read(adxl.X)
        y = adxl.read(adxl.Y)
        z = adxl.read(adxl.Z)
        print(f"Acceleration: {x}, {y}, {z}")

    **API**

    .. autoclass:: robot_hat.ADXL345
        :special-members: __init__
        :members:

class ``RGB_LED``
-----------------------------------------

    **Example**

    .. code-block:: python

        # Import RGB_LED and PWM class
        from robot_hat import RGB_LED, PWM

        # Create RGB_LED object
        rgb = RGB_LED(PWM(0), PWM(1), PWM(2))

        # Set color with 24 bit int
        rgb.set_color(0xFF0000) # Red
        # Set color with RGB tuple
        rgb.set_color((0, 255, 0)) # Green
        # Set color with RGB List
        rgb.set_color([0, 0, 255]) # Blue
        # Set color with RGB hex string starts with “#”
        rgb.set_color("#FFFF00") # Yellow

    **API**

    .. autoclass:: robot_hat.RGB_LED
        :special-members: __init__
        :members:

class ``Buzzer``
-----------------------------------------

    **Example**

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
    
        # Create Buzzer object for passive buzzer
        p_buzzer = Buzzer(PWM(0))
        # Create Buzzer object for active buzzer
        a_buzzer = Buzzer(Pin(0))

        # Active buzzer beeping
        while True:
            a_buzzer.on()
            time.sleep(0.5)
            a_buzzer.off()
            time.sleep(0.5)
    
        # Passive buzzer Simple usage
        # Play a Tone for 1 second
        p_buzzer.play(Music.NOTES["Low C"], duration=1)

        # Passive buzzer Manual control
        # Play a tone
        p_buzzer.play(Music.NOTES["Low C"])
        # Pause for 1 second
        time.sleep(1)
        # Play another tone
        p_buzzer.play(Music.NOTES["High C"])
        # Pause for 1 second
        time.sleep(1)
        # Stop playing
        p_buzzer.stop()

    **API**

    .. autoclass:: robot_hat.Buzzer
        :special-members: __init__
        :members:

class ``Sound``
-----------------------------------------

    **Example**

    .. code-block:: python

        # Import Sound and ADC class
        from robot_hat import Sound, ADC
        
        # Create Sound object
        s0 = Sound(ADC(0))

        # Read sound level
        level = s0.read()
        print(f"Sound level: {level}")

    **API**

    .. autoclass:: robot_hat.Sound
        :special-members: __init__
        :members:

class ``Joystick``
-----------------------------------------

    **Example**

    .. code-block:: python

        # Import Joystick, Pin and ADC class
        from robot_hat import Joystick, Pin, ADC
        
        # Create Joystick object
        js = Joystick(ADC(0), ADC(1), Pin(0))
        # If x, y or button is reversed, correct it
        js.is_x_reversed = True
        js.is_y_reversed = True
        js.is_btn_reversed = True

        # Read joystick position
        x = js.read(js.X)
        y = js.read(js.Y)
        btn = js.read(js.BTN)
        print(f"Joystick position: {x}, {y}, {btn}")

        # Read joystick simple states
        state = js.read_status()
        print(f"Joystick state: {state}")

    **API**

    .. autoclass:: robot_hat.Joystick
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
        datas = gs.get_grayscale_data()
        print(f"Grayscale_Module position: {datas}")

        # Read Grayscale_Module simple states
        state = gs.get_line_status()
        print(f"Grayscale_Module state: {state}")

    **API**

    .. autoclass:: robot_hat.Grayscale_Module
        :special-members: __init__
        :members:
