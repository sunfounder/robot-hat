
import speech_recognition as sr
from io import BytesIO
import os, sys
import wave
import logging

def redirect_error_2_null():
    # https://github.com/spatialaudio/python-sounddevice/issues/11

    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    return old_stderr

def cancel_redirect_error(stderr=None):
    if stderr is None:
        stderr = redirect_error_2_null() # ignore error print to ignore ALSA errors
    os.dup2(stderr, 2)
    os.close(stderr)

class Microphone:

    def __init__(self,
        dynamic_energy_adjustment_damping=0.16,
        dynamic_energy_ratio=1.6,
        pause_threshold=1,
        log=None
    ):
        self.log = log or logging.getLogger(__name__)

        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_adjustment_damping = dynamic_energy_adjustment_damping
        self.recognizer.dynamic_energy_ratio = dynamic_energy_ratio
        self.recognizer.pause_threshold = pause_threshold

    def listen(self, filename="/tmp/fusion_hat_mic_output.wav"):
        ''' Listen to the microphone and save the audio to the file.
        
        Args:
            filename (str, optional): The filename to save the audio. Defaults to "/tmp/fusion_hat_mic_output.wav".
        '''

        with sr.Microphone(chunk_size=8192) as source:
            cancel_redirect_error() # restore error print
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

            wav_data = BytesIO(audio.get_wav_data())
            wav_data.name = filename
            self.log.debug(f"Save audio to {filename}")
            
            with wave.open(filename, "wb") as wf:
                wf.setnchannels(1)  # 单声道
                wf.setsampwidth(audio.sample_width)  # 采样宽度（来自AudioData）
                wf.setframerate(audio.sample_rate)  # 采样率（来自AudioData）
                wf.writeframes(audio.get_wav_data())

    def set_dynamic_energy_adjustment_damping(self, value):
        self.recognizer.dynamic_energy_adjustment_damping = value

    def set_dynamic_energy_ratio(self, value):
        self.recognizer.dynamic_energy_ratio = value

    def set_pause_threshold(self, value):
        self.recognizer.pause_threshold = value

