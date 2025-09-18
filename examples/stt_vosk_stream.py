from robot_hat.stt import Vosk as STT

stt = STT(language="en-us")

while True:
    print("Say something")
    for result in stt.listen(stream=True):
        if result["done"]:
            print(f"final:   {result['final']}")
        else:
            print(f"partial: {result['partial']}", end="\r", flush=True)
