class ``FileDB``
======================

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
    print(value0, value1)


**API**

.. currentmodule:: robot_hat

.. autoclass:: fileDB
    :special-members: __init__
    :members: