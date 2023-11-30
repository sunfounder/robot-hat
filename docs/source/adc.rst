.. _class_adc:

class ``ADC``
=========================================

**Example**

.. code-block:: python
    
    # Import ADC class
    from robot_hat import ADC

    # Create ADC object with numeric pin numbering
    a0 = ADC(0)
    # Create ADC object with named pin numbering
    a1 = ADC('A1')

    # Read ADC value
    value0 = a0.read()
    value1 = a1.read()
    voltage0 = a0.read_voltage()
    voltage1 = a1.read_voltage()
    print(f"ADC 0 value: {value0}")
    print(f"ADC 1 value: {value1}")
    print(f"ADC 0 voltage: {voltage0}")
    print(f"ADC 1 voltage: {voltage1}")

**API**

.. currentmodule:: robot_hat

.. autoclass:: ADC
    :show-inheritance:
    :special-members: __init__
    :members: