from fusion_hat.utils import is_installed
from fusion_hat.utils import run_command

from .tts_engine import TTSEngine

class Pico2Wave(TTSEngine):
    """
    Pico2Wave TTS engine.
    """
    PICO2WAVE = 'pico2wave'

    SUPPORTED_LANGUAUE = [
        'en-US',
        'en-GB',
        'de-DE',
        'es-ES',
        'fr-FR',
        'it-IT',
    ]
    def __init__(self, *args, lang=None, **kwargs):
        super().__init__(*args, **kwargs)

        if not is_installed("pico2wave"):
            raise Exception("TTS engine: pico2wave is not installed.")
        
        self._lang = lang or 'en-US'

    def say(self, words):
        """
        Say words with pico2wave.

        :param words: words to say.
        :type words: str
        """
        self.log.debug(f'pico2wave: [{words}]')
        if not self._check_executable('pico2wave'):
            self.log.debug('pico2wave is busy. Pass')

        cmd = f'pico2wave -l {self._lang} -w /tmp/fusion-hat-pico2wave.wav "{words}" && aplay /tmp/tts.wav 2>/dev/null & '
        _, result = run_command(cmd)
        if len(result) != 0:
            raise (f'tts-pico2wave:\n\t{result}')
        self.log.debug(f'command: {cmd}')

    def set_lang(self, lang):
        """
        Set language.

        :param lang: language.
        :type lang: str
        """
        if lang not in self.SUPPORTED_LANGUAUE:
            raise ValueError(f'Language {lang} is not supported')
        self._lang = lang
