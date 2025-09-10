from robot_hat.tts import Piper
from robot_hat.utils import enable_speaker

tts = Piper()

enable_speaker()

tts.set_model('en_US-amy-low')
tts.say("Hi, I'm piper TTS. A fast and local neural text-to-speech engine that embeds espeak-ng for phonemization.")
