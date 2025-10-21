from sunfounder_voice_assistant.tts import Piper as _Piper
from sunfounder_voice_assistant.tts import Pico2Wave as _Pico2Wave
from sunfounder_voice_assistant.tts import Espeak as _Espeak
from sunfounder_voice_assistant.tts import OpenAI_TTS as _OpenAI_TTS

from .utils import enable_speaker

class Piper(_Piper):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        enable_speaker()

class Pico2Wave(_Pico2Wave):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        enable_speaker()

class Espeak(_Espeak):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        enable_speaker()

class OpenAI_TTS(_OpenAI_TTS):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        enable_speaker()

