from robot_hat.stt import Vosk as STT

WAKE_WORDS = [
    "hey robot",
]

stt = STT(language="en-us")

print('Wake me with :"Hey robot"')
result = stt.wait_until_heard(WAKE_WORDS)
print("Wake word detected")
