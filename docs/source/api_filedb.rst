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
