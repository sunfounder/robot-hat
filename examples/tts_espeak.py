from robot_hat.tts import Espeak
from robot_hat.utils import enable_speaker

tts = Espeak()
tts.set_amp(100)
tts.set_speed(150)
tts.set_gap(1)
tts.set_pitch(80)

enable_speaker()

tts.say("Hello world!")
