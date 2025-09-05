from robot_hat.stt import Vosk

WAKE_WORDS = [
    "hey robot",
]

stt = Vosk(language="en-us")

print('Wake me with :"Hey robot"')
result = stt.wait_until_heard(WAKE_WORDS)
print("Wake word detected")
