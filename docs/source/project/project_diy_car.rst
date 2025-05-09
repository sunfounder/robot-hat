 .. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

DIY Car
==============

In addition to being suitable for simple experiments, the Robot HAT is ideal for use as a central controller in robotics, such as for smart cars.

In this project, we built a simple line-following car.

.. image:: img/diy_car.jpg

**Code**

.. code-block:: python

    from robot_hat import Motors, Pin
    import time

    # Create motor object
    motors = Motors()

    # Initialize line tracking sensor
    line_track = Pin('D0')

    def main():
        while True:
            # print("value", line_track.value())
            # time.sleep(0.01)
            if line_track.value() == 1:
                # If line is detected
                motors[1].speed(-60)  # Motor 1 forward
                motors[2].speed(20) # Motor 2 backward
                time.sleep(0.01)
            else:
                # If line is not detected
                motors[1].speed(-20) # Motor 1 backward
                motors[2].speed(60)  # Motor 2 forward
                time.sleep(0.01)

    def destroy():
        # Stop motors when Ctrl+C is pressed
        motors.stop()
        print("Motors stopped.")

    if __name__ == '__main__':
        try:
            main()
        except KeyboardInterrupt:
            destroy()
