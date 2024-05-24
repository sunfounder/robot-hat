 .. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

.. _install_i2s:

Install ``i2samp.sh`` for the Speaker
==============================================

The ``i2samp.sh`` is a sophisticated Bash script specifically designed for setting up and configuring an I2S (Inter-IC Sound) amplifier on Raspberry Pi and similar devices. Licensed under the MIT license, it ensures compatibility with a range of hardware and operating systems, conducting thorough checks before proceeding with any installation or configuration.

If you want your speaker to work properly, you definitely need to install this script. 

The steps are as follows:

.. code-block::

    cd ~/robot-hat
    sudo bash i2samp.sh

Type ``y`` and press ``enter`` to continue running the script.

    .. image:: img/install_i2s1.png

Type ``y`` and press ``enter`` to run ``/dev/zero`` in the background.

    .. image:: img/install_i2s2.png

Type ``y`` and press ``enter`` to restart the Raspberry pi.

    .. image:: img/install_i2s2.png

.. warning::

    If there is no sound after restarting, you may need to run the ``i2samp.sh`` script several times.