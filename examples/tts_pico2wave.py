from robot_hat.tts import Pico2Wave
from robot_hat.utils import enable_speaker

tts = Pico2Wave()
tts.set_lang('en-US')

enable_speaker()

tts.say("Hello world!")
