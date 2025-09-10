from robot_hat.tts import Piper

tts = Piper()

tts.set_model('en_US-amy-low')
tts.say("Hi, I'm piper TTS. A fast and local neural text-to-speech engine that embeds espeak-ng for phonemization.")
