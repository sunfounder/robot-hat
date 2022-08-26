#!/usr/bin/env python3
from .basic import _Basic_class
from .utils import is_installed
from .music import Music
from distutils.spawn import find_executable

class TTS(_Basic_class):
    """Text to speech class"""
    _class_name = 'TTS'
    SUPPORTED_LANGUAUE = [
        'zh-CN',
        'en-US',
        'en-GB',
        'de-DE',
        'es-ES',
        'fr-FR',
        'it-IT',
    ]
    """Supported TTS language for pico2wave"""

    def __init__(self, engine='espeak'):
        """
        Initialize TTS class.
        
        :param engine: TTS engine, espeak or pico
        :type engine: str
        """
        super().__init__()
        self._lang = "en-US"
        self.engine = engine
        if (engine == "espeak"):
            if not is_installed("espeak"):
                raise Exception("TTS engine: espeak is not installed.")
            self._amp   = 100 
            self._speed = 175
            self._gap   = 5
            self._pitch = 50

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
        self.engine(words)

    def espeak(self, words):
        """
        Say words with espeak.
        
        :param words: words to say.
        :type words: str
        """
        self._debug('espeak:\n [%s]' % (words))
        if not self._check_executable('espeak'):
            self._debug('espeak is busy. Pass')

        cmd = 'espeak -a%d -s%d -g%d -p%d \"%s\" --stdout | aplay 2>/dev/null & ' % (self._amp, self._speed, self._gap, self._pitch, words)
        self.run_command(cmd)
        self._debug('command: %s' %cmd)

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
            if v in self.SUPPORTED_LANGUAUE:
                self._lang = v
                return self._lang
        raise ValueError("Arguement \"%s\" is not supported. run tts.supported_lang to get supported language type."%value)

    def supported_lang(self):
        """
        Get supported language.

        :return: supported language.
        :rtype: list
        """
        return self.SUPPORTED_LANGUAUE

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
            amp=self._amp
        if speed == None:
            speed=self._speed
        if gap == None:
            gap=self._gap
        if pitch == None:
            pitch=self._pitch

        if amp not in range(0, 200):
            raise ValueError('Amp should be in 0 to 200, not "{0}"'.format(amp))
        if speed not in range(80, 260):
            raise ValueError('speed should be in 80 to 260, not "{0}"'.format(speed))
        if pitch not in range(0, 99):
            raise ValueError('pitch should be in 0 to 99, not "{0}"'.format(pitch)) 
        self._amp   = amp
        self._speed = speed
        self._gap   = gap
        self._pitch = pitch
