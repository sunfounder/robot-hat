from robot_hat.stt import Vosk as STT

stt = STT(language="en-us")

while True:
    print("Say something")
    result = stt.listen(stream=False)
    print(result)