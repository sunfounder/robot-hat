 .. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

.. _class_tts:

class ``TTS``
==================================================

.. warning::
    * You need to add ``sudo`` when running this script, in case the speaker doesn't work.
    * :ref:`faq_speaker`.

**Example**

.. code-block:: python

    # Import TTS class
    from robot_hat import TTS

    # Initialize TTS class
    tts = TTS(lang='en-US')
    # Speak text
    tts.say("Hello World")
    # show all supported languages
    print(tts.supported_lang())


**API**

.. currentmodule:: robot_hat

.. autoclass:: TTS
    :show-inheritance:
    :special-members: __init__
    :members:
