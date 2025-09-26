from robot_hat.stt import Vosk as STT

WAKE_WORDS = [
    "hey robot",
]

stt = STT(language="en-us")
stt.set_wake_words(WAKE_WORDS)

print('Wake me with :"Hey robot"')
result = stt.wait_until_heard()
print("Wake word detected")
