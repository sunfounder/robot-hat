from fusion_hat.utils import is_installed
from fusion_hat.utils import is_installed, run_command
from .tts_engine import TTSEngine

class Espeak(TTSEngine):

    ESPEAK = 'espeak'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not is_installed("espeak"):
            raise Exception("TTS engine: espeak is not installed.")
        self._amp = 100
        self._speed = 175
        self._gap = 5
        self._pitch = 50
        self._lang = 'en-US'

    def say(self, words):
        """
        Say words with espeak.

        :param words: words to say.
        :type words: str
        """
        self.log.debug(f'espeak: [{words}]')
        if not self._check_executable('espeak'):
            self.log.debug('espeak is busy. Pass')

        cmd = f'espeak -a{self._amp} -s{self._speed} -g{self._gap} -p{self._pitch} "{words}" --stdout | aplay 2>/dev/null & '
        _, result = run_command(cmd)
        if len(result) != 0:
            raise (f'tts-espeak:\n\t{result}')
        self.log.debug(f'command: {cmd}')

    def set_amp(self, amp):
        if amp not in range(0, 200):
            raise ValueError(f'Amp should be in 0 to 200, not "{amp}"')
        self._amp = amp

    def set_speed(self, speed):
        if speed not in range(80, 260):
            raise ValueError(f'speed should be in 80 to 260, not "{speed}"')
        self._speed = speed

    def set_gap(self, gap):
        if gap not in range(0, 200):
            raise ValueError(f'gap should be in 0 to 200, not "{gap}"')
        self._gap = gap

    def set_pitch(self, pitch):
        if pitch not in range(0, 99):
            raise ValueError(f'pitch should be in 0 to 99, not "{pitch}"')
        self._pitch = pitch

    def set_lang(self, lang):
        if lang not in self.SUPPORTED_LANGUAUE:
            raise ValueError(f'lang should be in {self.SUPPORTED_LANGUAUE}, not "{lang}"')
        self._lang = lang

