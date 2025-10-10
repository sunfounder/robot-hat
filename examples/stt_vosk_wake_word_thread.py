from robot_hat.stt import Vosk as STT
import time

WAKE_WORDS = ["hey robot"]

stt = STT(language="en-us")
stt.set_wake_words(WAKE_WORDS)

while True:
    stt.start_listening_wake_words()

    while not stt.is_waked():
        print("Waiting for wake word...")
        time.sleep(3)
        
    print("Wake word detected")

