
from .pin import Pin
import threading
import time

class LED:

    def __init__(self, pin: str="LED") -> None:
        self.led = Pin(pin, mode=Pin.OUT)
        self.blink_thread = None
        self.blink_running = False
        self.value = 0

    def on(self) -> None:
        self.blink_stop()
        self.led.on()
        self.value = 1

    def off(self) -> None:
        self.blink_stop()
        self.led.off()
        self.value = 0

    def toggle(self, skip_stop: bool=False) -> None:
        if not skip_stop:
            self.blink_stop()
        self.value = self.value + 1 & 1
        self.led.value(self.value)

    def blink(self, times: int=1, delay: float=0.1, pause: float=0) -> None:
        self.blink_stop()
        self.blink_thread = threading.Thread(name="LED Blink Thread", target=self.blink_loop, args=(times, delay, pause))
        self.blink_thread.start()

    def blink_loop(self, times: int=1, delay: float=0.1, pause: float=0) -> None:
        self.blink_running = True
        self.led.off()

        while self.blink_running:
            count = 0
            delay_start = time.time()
            while count < times:
                if time.time() - delay_start > delay:
                    delay_start = time.time()
                    self.toggle(skip_stop=True)
                    count += 0.5
                time.sleep(0.01)
            pause_start = time.time()
            while time.time() - pause_start < pause and self.blink_running:
                time.sleep(0.01)
            time.sleep(0.01)

    def blink_stop(self) -> None:
        if self.blink_running:
            self.blink_running = False
            self.blink_thread.join()

    def close(self) -> None:
        self.blink_stop()
        self.led.off()
        self.led.close()
