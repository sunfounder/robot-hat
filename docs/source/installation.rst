 .. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

Install the ``robot-hat`` Module
==========================================

``robot-hat`` is the supported library for the Robot HAT.

#. Update your system.

   Make sure you are connected to the Internet and update your system:

   .. raw:: html

      <run></run>

   .. code-block::

      sudo apt update
      sudo apt upgrade

   .. note::

      Python3 related packages must be installed if you are installing the **Lite** version OS.

      .. raw:: html

         <run></run>

      .. code-block::
        
         sudo apt install git python3-pip python3-setuptools python3-smbus

#. Type this command into the terminal to install the ``robot-hat`` package.

    .. raw:: html

        <run></run>

    .. code-block::

        cd ~/
        git clone -b v2.0 https://github.com/sunfounder/robot-hat.git
        cd robot-hat
        sudo python3 setup.py install

   .. note::
      Run ``setup.py`` to download some necessary components. You may have a network problem and the download may fail. At this point you may need to download again. In the following cases, type ``Y`` and press ``Enter`` to continue the process.

   .. image:: img/dowload_code.png