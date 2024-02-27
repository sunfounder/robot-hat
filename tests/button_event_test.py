from robot_hat import Pin
import time

btn = Pin("D0") # IO17

def pressed_handler():
    print(f"Pressed - {time.time()}")

def released_handler():
    print(f"Released - {time.time()}")

def both_handler():
    print(f"xxx - {time.time()}")

btn.irq(handler=pressed_handler, trigger=Pin.IRQ_FALLING, bouncetime=20)
print(btn)
btn.irq(handler=released_handler, trigger=Pin.IRQ_RISING, bouncetime=10)
print(btn)
# btn.irq(handler=both_handler, trigger=Pin.IRQ_RISING_FALLING, bouncetime=10)
# print(btn)



while True:
    time.sleep(1)
