.. _class_i2c:

class ``I2C``
========================================

**Example**

.. code-block:: python

    # Import the I2C class
    from robot_hat import I2C

    # You can scan for available I2C devices
    print([f"0x{addr:02X}" for addr in I2C().scan()])
    # You should see at least one device address 0x14, which is the 
    # on board MCU for PWM and ADC

    # Initialize a I2C object with device address, for example
    # to communicate with on board MCU 0x14
    mcu = I2C(0x14)
    # Send ADC channel register to read ADC, 0x10 is Channel 0, 0x11 is Channel 1, etc.
    mcu.write([0x10, 0x00, 0x00])
    # Read 2 byte for MSB and LSB
    msb, lsb = mcu.read(2)
    # Convert to integer
    value = (msb << 8) + lsb
    # Print the value
    print(value)

For more information on the I2C protocol, see checkout adc.py and pwm.py

**API**

.. currentmodule:: robot_hat

.. autoclass:: I2C
    :show-inheritance:
    :special-members: __init__
    :members: