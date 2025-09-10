import requests
import os
import logging
import pyaudio
from ..utils import enable_speaker

def volume_gain(input_file, output_file, gain):
    import sox

    try:
        transform = sox.Transformer()
        transform.vol(gain)

        transform.build(input_file, output_file)

        return True
    except Exception as e:
        print(f"[ERROR] volume_gain err: {e}")
        return False

class OpenAI_TTS():
    """
    OpenAI TTS engine.
    """
    WHISPER = 'whisper'

    MODLES = [
        "tts-1",
        "tts-1-hd",
        "gpt-4o-mini-tts",
        "accent",
        "emotional-range",
        "intonation",
        "impressions",
        "speed-of-speech",
        "tone",
        "whispering",
    ]

    VOICES = [
        "alloy",
        "ash",
        "ballad",
        "coral",
        "echo",
        "fable",
        "nova",
        "onyx",
        "sage",
        "shimmer"
    ]

    DEFAULT_MODEL = 'tts-1'
    DEFAULT_VOICE = 'alloy'
    DEFAULT_INSTRUCTIONS = "Speak in a cheerful and positive tone."

    URL = "https://api.openai.com/v1/audio/speech"

    def __init__(self, *args,
        voice=DEFAULT_VOICE,
        model=DEFAULT_MODEL,
        api_key=None,
        gain=3,
        log=None):
        self.log = log or logging.getLogger(__name__)
        enable_speaker()

        self._model = model or self.DEFAULT_MODEL
        self._voice = voice or self.DEFAULT_VOICE
        self._gain = gain
        self.is_ready = False

        self.set_api_key(api_key)

    def tts(self, words, output_file="/tmp/openai_tts.wav", instructions=DEFAULT_INSTRUCTIONS, stream=False):
        """
        Request OpenAI TTS API.
        
        :param words: words to say.
        :type words: str
        :param output_file: output file.
        :type output_file: str
        :param instructions: instructions.
        :type instructions: str
        :param stream: whether to stream the audio.
        :type stream: bool
        :return: True if success.
        :rtype: bool
        """
        
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self._model,
            "input": words,
            "voice": self._voice,
            "response_format": "wav",
            "instructions": instructions,
        }
        
        try:
            response = requests.post(self.URL, json=data, headers=headers, stream=True)
            
            response.raise_for_status()
            
            if stream:
                self._stream_audio(response)
            else:
                with open(output_file, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                
                if self._gain > 1:
                    old_output_file = output_file.replace('.wav', f'_old.wav')
                    os.rename(output_file, old_output_file)
                    volume_gain(old_output_file, output_file, self._gain)
                    os.remove(old_output_file)

            return True
        
        except requests.exceptions.RequestException as e:
            self.log.error(f"请求发生错误: {e}")
            return False
        except IOError as e:
            self.log.error(f"文件操作错误: {e}")
            return False

    def _stream_audio(self, response):
        """流式播放音频"""
        p = pyaudio.PyAudio()
        
        stream = p.open(format=p.get_format_from_width(2),
                        channels=1,
                        rate=22050,
                        output=True)
        
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                stream.write(chunk)
        
        stream.stop_stream()
        stream.close()
        p.terminate()

    def say(self, words, instructions=DEFAULT_INSTRUCTIONS, stream=True):
        '''
        Say words.

        :param words: words to say.
        :type words: str
        :param instructions: instructions.
        :type instructions: str
        :param stream: whether to stream the audio.
        :type stream: bool
        '''
        if stream:
            self.tts(words, instructions=instructions, stream=True)
        else:
            file_name = "/tmp/openai_tts.wav"
            self.tts(words, instructions=instructions, output_file=file_name, stream=False)
            os.system(f'aplay {file_name}')
            os.remove(file_name)

    def set_voice(self, voice):
        """
        Set voice.

        :param voice: voice.
        :type voice: str
        """
        if voice not in self.VOICES:
            raise ValueError(f'Voice {voice} is not supported')
        self._voice = voice

    def set_model(self, model):
        """
        Set model.

        :param model: model.
        :type model: str
        """
        if model not in self.MODLES:
            raise ValueError(f'Model {model} is not supported')
        self._model = model

    def set_api_key(self, api_key):
        """
        Set api key.

        :param api_key: api key.
        :type api_key: str
        """
        self._api_key = api_key

    def set_gain(self, gain):
        """
        Set gain.

        :param gain: gain.
        :type gain: int
        """
        self._gain = gain
