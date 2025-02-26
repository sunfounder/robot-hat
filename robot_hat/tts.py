#!/usr/bin/env python3
from .basic import _Basic_class
from .utils import is_installed, run_command
from .music import Music
from distutils.spawn import find_executable


class TTS(_Basic_class):
    """Text to speech class"""
    _class_name = 'TTS'
    SUPPORTED_LANGUAUE = [
        'en-US',
        'en-GB',
        'de-DE',
        'es-ES',
        'fr-FR',
        'it-IT',
    ]
    """Supported TTS language for pico2wave"""

    ESPEAK = 'espeak'
    """espeak TTS engine"""
    ESPEAK_NG = 'espeak-ng'
    """espeak-ng TTS engine"""
    PICO2WAVE = 'pico2wave'
    """pico2wave TTS engine"""

    def __init__(self, engine=PICO2WAVE, lang=None, *args, **kwargs):
        """
        Initialize TTS class.

        :param engine: TTS engine, TTS.PICO2WAVE, TTS.ESPEAK, or TTS.ESPEAK_NG
        :type engine: str
        """
        super().__init__()
        self.engine = engine
        if (engine == self.ESPEAK or engine == self.ESPEAK_NG):
            if not is_installed(engine):
                raise Exception(f"TTS engine: {engine} is not installed.")
            self._amp = 100
            self._speed = 175
            self._gap = 5
            self._pitch = 50
            if lang == None:
                self._lang = "en-us"
            else:
                self._lang = lang
            self._supported_lang = _get_supported_lang_espeak(engine)
        elif (engine == self.PICO2WAVE):
            if not is_installed("pico2wave"):
                raise Exception("TTS engine: pico2wave is not installed.")
            if lang == None:
                self._lang = "en-US"
            else:
                self._lang = lang
            self._supported_lang = self.SUPPORTED_LANGUAUE

    def _check_executable(self, executable):
        executable_path = find_executable(executable)
        found = executable_path is not None
        return found

    def say(self, words):
        """
        Say words.

        :param words: words to say.
        :type words: str
        """
        words = words.replace("'", "\\'")
        eval(f"self.{self.engine.replace('-', '_')}('{words}')")

    def _espeak(self, engine, words):
        """
        Say words with espeak.

        :param words: words to say.
        :type words: str
        """
        self._debug(f'{engine}: [{words}]')
        if not self._check_executable(engine):
            self._debug(f'{engine} is busy. Pass')

        cmd = f'{engine} -v{self._lang} -a{self._amp} -s{self._speed} -g{self._gap} -p{self._pitch} "{words}" --stdout | aplay 2>/dev/null & '
        status, result = run_command(cmd)
        if len(result) != 0:
            raise (f'tts-espeak:\n\t{result}')
        self._debug(f'command: {cmd}')

    def espeak(self, words):
        self._espeak('espeak', words)

    def espeak_ng(self, words):
        self._espeak('espeak-ng', words)

    def pico2wave(self, words):
        """
        Say words with pico2wave.

        :param words: words to say.
        :type words: str
        """
        self._debug(f'pico2wave: [{words}]')
        if not self._check_executable('pico2wave'):
            self._debug('pico2wave is busy. Pass')

        cmd = f'pico2wave -l {self._lang} -w /tmp/tts.wav "{words}" && aplay /tmp/tts.wav 2>/dev/null & '
        status, result = run_command(cmd)
        if len(result) != 0:
            raise (f'tts-pico2wav:\n\t{result}')
        self._debug(f'command: {cmd}')

    def lang(self, *value):
        """
        Set/get language. leave empty to get current language.

        :param value: language.
        :type value: str
        """
        if len(value) == 0:
            return self._lang
        elif len(value) == 1:
            v = value[0]
            if v in self._supported_lang:
                self._lang = v
                return self._lang
        raise ValueError(
            f'Arguement "{value}" is not supported. run tts.supported_lang to get supported language type.'
        )

    def supported_lang(self):
        """
        Get supported language.

        :return: supported language.
        :rtype: list
        """
        return self._supported_lang

    def espeak_params(self, amp=None, speed=None, gap=None, pitch=None):
        """
        Set espeak parameters.

        :param amp: amplitude.
        :type amp: int
        :param speed: speed.
        :type speed: int
        :param gap: gap.
        :type gap: int
        :param pitch: pitch.
        :type pitch: int
        """
        if amp == None:
            amp = self._amp
        if speed == None:
            speed = self._speed
        if gap == None:
            gap = self._gap
        if pitch == None:
            pitch = self._pitch

        if amp not in range(0, 200):
            raise ValueError(f'Amp should be in 0 to 200, not "{amp}"')
        if speed not in range(80, 260):
            raise ValueError(f'speed should be in 80 to 260, not "{speed}"')
        if pitch not in range(0, 99):
            raise ValueError(f'pitch should be in 0 to 99, not "{pitch}"')
        self._amp = amp
        self._speed = speed
        self._gap = gap
        self._pitch = pitch

def _get_supported_lang_espeak(name):
    """
    Get supported language for espeak.

    :param name: espeak command name.
    :return: supported language.
    :rtype: list
    """
    status, result = run_command(f"{name} --voices")
    supported_lang = []
    if not status:
        first = True
        for line in result.split('\n'):
            if first or not line:
                first = False
                continue
            lang = [v for v in line.split() if v][1]
            supported_lang.append(lang)
    return supported_lang
