 .. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

.. _class_pin:

class ``Pin``
===========================

**Example**

.. code-block:: python
    
    # Import Pin class
    from robot_hat import Pin

    # Create Pin object with numeric pin numbering and default input pullup enabled
    d0 = Pin(0, Pin.IN, Pin.PULL_UP)
    # Create Pin object with named pin numbering
    d1 = Pin('D1')

    # read value
    value0 = d0.value()
    value1 = d1.value()
    print(value0, value1)

    # write value
    d0.value(1) # force input to output
    d1.value(0)

    # set pin high/low
    d0.high()
    d1.off()

    # set interrupt
    led = Pin('LED', Pin.OUT)
    switch = Pin('SW', Pin.IN, Pin.PULL_DOWN)
    def onPressed(chn):
        led.value(not switch.value())
    switch.irq(handler=onPressed, trigger=Pin.IRQ_RISING_FALLING)

**API**

.. currentmodule:: robot_hat

.. autoclass:: Pin
    :show-inheritance:
    :special-members: __init__, __call__
    :members: