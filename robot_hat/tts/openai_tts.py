from openai import AsyncOpenAI, OpenAI

from openai.helpers import LocalAudioPlayer
import asyncio
import os

from .tts_engine import TTSEngine

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

class OpenAI_TTS(TTSEngine):
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

    def __init__(self, *args,
        stream=False,
        voice=DEFAULT_VOICE,
        model=DEFAULT_MODEL,
        api_key=None,
        gain=3,
        **kwargs):
        super().__init__(*args, **kwargs)

        self._model = model or self.DEFAULT_MODEL
        self._voice = voice or self.DEFAULT_VOICE
        self._gain = gain
        self.stream = stream

        if api_key:
            self.set_api_key(api_key)
        else:
            if os.environ.get("OPENAI_API_KEY"):
                if self.stream:
                    self.client = AsyncOpenAI()
                else:
                    self.client = OpenAI()
                self.is_ready = True

    async def async_say(self, words, instructions=DEFAULT_INSTRUCTIONS):
        async with self.client.audio.speech.with_streaming_response.create(
            model=self._model,
            voice=self._voice,
            input=words,
            instructions=instructions,
            response_format="pcm",
        ) as response:
            await LocalAudioPlayer().play(response)

    def tts(self, words, output_file="/tmp/openai_tts.wav", instructions=DEFAULT_INSTRUCTIONS):

        """
        TTS.

        :param words: words to say.
        :type words: str
        :type gain: int
        """
        with self.client.audio.speech.with_streaming_response.create(
            model=self._model,
            voice=self._voice,
            input=words,
            instructions=instructions,
            response_format="wav",
        ) as response:
            response.stream_to_file(output_file)
        
        if self._gain > 1:
            old_output_file = output_file.replace('.wav', f'_old.wav')
            os.rename(output_file, old_output_file)
            volume_gain(old_output_file, output_file, self._gain)
            os.remove(old_output_file)

    def say(self, words, instructions=DEFAULT_INSTRUCTIONS):
        '''
        Say words.

        :param words: words to say.
        :type words: str
        :param instructions: instructions.
        :type instructions: str

        '''
        if not self.is_ready:
            raise ValueError('OpenAI TTS is not initialized, try set api key with OPENAI_API_KEY environment variable or with set_api_key method')

        if self.stream:
            asyncio.run(self.async_say(words, instructions))
        else:
            file_name = "/tmp/openai_tts.wav"
            self.tts(words, instructions=instructions, output_file=file_name)
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
        if self.stream:
            self.client = AsyncOpenAI(api_key=self._api_key)
        else:
            self.client = OpenAI(api_key=self._api_key)
        self.is_ready = True

    def set_gain(self, gain):
        """
        Set gain.

        :param gain: gain.
        :type gain: int
        """
        self._gain = gain
