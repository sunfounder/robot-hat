from robot_hat.tts import Espeak

tts = Espeak()
tts.set_amp(100)
tts.set_speed(150)
tts.set_gap(1)
tts.set_pitch(80)

tts.say("Hello world!")
