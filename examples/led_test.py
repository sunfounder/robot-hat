from robot_hat.led import LED
import time

led = LED()

print("On")
led.on()
time.sleep(2)
print("Off")
led.off()
time.sleep(2)
print("Blink delay 1 second")
led.blink(delay=1)
time.sleep(5)
print("Blink 3 times delay 0.1 second pause 0.5 second")
led.blink(times=3, delay=0.1, pause=0.5)
time.sleep(5)
print("Blink 2 times delay 0.2 second pause 1 second")
led.blink(times=2, delay=0.2, pause=1)
time.sleep(5)
print("Done")
led.close()