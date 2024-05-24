 .. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

FAQ
================

Q1: Can the battery be connected while providing power to the Raspberry Pi at the same time?
------------------------------------------------------------------------------------------------------------
A: Yes, the Robot HAT has a built-in anti-backflow diode that prevents the Raspberry Pi's power from flowing back into the Robot HAT.

Q2: Can the Robot HAT be used while charging?
--------------------------------------------------------
A: Yes, the Robot HAT can be used while charging. When charging, the input power is boosted by the charging chip to charge the batteries, while also providing power to the DC-DC step-down for external use. The charging power is approximately 10W. If the external power consumption is too high for an extended period, the batteries may supplement the power, similar to how a mobile phone charges while in use. However, it is important to be mindful of the battery's capacity to avoid draining it completely during simultaneous charging and usage.

.. _faq_speaker:

Q3: Why is there no sound from the speaker?
--------------------------------------------------

When your script is running but the speaker is not producing sound, there could be several reasons:

#. Check if the ``i2samp.sh`` script has been installed. For detailed instructions, please refer to: :ref:`install_i2s`.
#. When running scripts related to speakers, it's necessary to add ``sudo`` to obtain administrative privileges. For example, ``sudo python3 tts.py``.
#. Don't using Raspberry Pi's built-in programming tools, like Geany to run Speaker-related scripts. These tools run with standard user privileges, while hardware control, such as managing speakers, often requires higher permissions.
