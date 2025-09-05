from robot_hat.stt import Vosk

vosk = Vosk(language="en-us")

while True:
    print("Say something")
    result = vosk.listen(stream=False)
    print(result)