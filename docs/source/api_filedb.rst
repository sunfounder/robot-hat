 .. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

class ``FileDB``
======================

**Example**

.. code-block:: python
    
    # Import fileDB class
    from robot_hat import fileDB

    # Create fileDB object with a config file
    db = fileDB("./config")

    # Set some values
    db.set("apple", "10")
    db.set("orange", "5")
    db.set("banana", "13")

    # Read the values
    print(db.get("apple"))
    print(db.get("orange"))
    print(db.get("banana"))

    # Read an none existing value with a default value
    print(db.get("pineapple", default_value="-1"))

Now you can checkout the config file ``config`` in bash.

.. code-block:: bash

    cat config

**API**

.. currentmodule:: robot_hat

.. autoclass:: fileDB
    :show-inheritance:
    :special-members: __init__
    :members:
