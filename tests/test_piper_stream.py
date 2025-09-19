from robot_hat.tts import Piper
import time

tts = Piper(model='en_US-amy-low')

word = "Hi, I'm piper TTS. A fast and local neural text-to-speech engine that embeds espeak-ng for phonemization."

print("Say with stream")
start = time.time()
tts.say(word)
end = time.time()
print(f"Time taken: {end - start}")

print("====================================================")

print("Say without stream")
start = time.time()
tts.say(word, stream=False)
end = time.time()
print(f"Time taken: {end - start}")
