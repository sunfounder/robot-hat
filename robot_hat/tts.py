from .basic import _Basic_class
from .music import Music
from distutils.spawn import find_executable
import json

class TTS(_Basic_class):
    _class_name = 'TTS'
    SUPPORTED_LANGUAUE = [
        'en-US', # 英语(美国) English-United States
        'en-GB', # 英语(英国) English-United Kingdom
        'de-DE', # 德语(德国) Germany-Deutsch
        'es-ES', # 西班牙语(西班牙) España-Español
        'fr-FR', # 法语(法国) France-Le français
        'it-IT', # 意大利语(意大利) Italia-lingua italiana
    ]

    def __init__(self, data=None):
        super().__init__()
        try:
            self._lang = "en-US"    # 默认语言:英语(美国) default language: English-United States
            self.engine = "pico2wave"   # default tts engine: pico2wave
            self.url = None
            self.token = None

            if(isinstance(data, dict)):
                if 'engine' in data:
                    self.engine = data['engine']
                if 'url' in data:
                    self.url = data['url']
                if 'token' in data:
                    self.token = data['token']

                if self.engine == "espeak":
                    self._amp   = 100
                    self._speed = 175
                    self._gap   = 5
                    self._pitch = 50
                elif self.engine == "gtts" or self.engine == "polly":
                    import requests
                    import base64
                    self.requests = requests
                    self.base64 = base64

        except Exception as e:
            print(e)

    def _check_executable(self, executable):
        executable_path = find_executable(executable)
        found = executable_path is not None
        return found

    def say(self, words:str):
        if  str(words).strip() == '':
            print('tts.say is missing parameters')
            print("tts.say is missing parameters")
        eval(f"self.{self.engine}(words)")

    def lang(self, *value):
        '''
        Set language
        '''
        if len(value) == 0:
            return self._lang
        elif len(value) == 1:
            v = value[0]
            if v in self.SUPPORTED_LANGUAUE:
                self._lang = v
                return self._lang
        raise ValueError("Arguement \"%s\" is not supported. run tts.supported_lang to get supported language type."%value)

    def supported_lang(self):
        '''
        Return supported languages
        '''
        return self.SUPPORTED_LANGUAUE

    def espeak_params(self, amp=None, speed=None, gap=None, pitch=None):
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

    def espeak(self, words):
        print('espeak: [%s]' % (words))
        if not self._check_executable('espeak'):
            print('espeak is busy. Pass')

        cmd = 'espeak -a%d -s%d -g%d -p%d \"%s\" --stdout | aplay 2>/dev/null & ' % (self._amp, self._speed, self._gap, self._pitch, words)
        self.run_command(cmd)
        # print('command: %s' %cmd)

    def pico2wave(self, words):
        output_file = ".tts_output.wav"
        print('pico2wave: [%s]' % (words))
        if not self._check_executable('pico2wave'):
            print('pico2wave is busy. Pass')
            print('pico2wave is busy. Pass')

        cmd = 'pico2wave -l \"%s\" -w \"%s\" \"%s\" '% (self._lang, output_file, words)
        self.run_command(cmd)
        # print('command: %s' %cmd)
        self.run_command("sudo aplay %s  2>/dev/null &"%output_file)

    def gtts(self, words):
        sound_file = "./output.mp3"
        data = {
            "text": words,
            "language": self.lang(),
        }
        header = {
            "Content-Type": "application/json",
        }

        data =json.dumps(data)
        data = bytes(data, 'utf8')
        req = self.requests.Request(self.url, data=data, headers=header, method='POST')
        r = self.requests.urlopen(req)
        result = r.read()
        result = result.decode("utf-8")
        result = self.ast.literal_eval(result)
        data = result["data"]
        data = self.base64.b64decode(data)
        with open(sound_file, "wb") as f:
            f.write(data)

        # music = Music()
        # music.sound_play(sound_file)
        self.run_command(f"sudo aplayer {sound_file}")

    def polly(self, words):
        sound_file = "./output.mp3"
        send_data = {
            "text": words,
            "language": self._lang,
            "token": self.token
        }
        header = {
            "Content-Type": "application/json",
        }
        for i in range(5):
            r = self.requests.post(url=self.url, headers=header, json=send_data)
            result = r.json()
            # print('result: %s'%result)
            if result != "":
                break
            else:
                print("Empty result")
        else:
            raise IOError("Network Error")

        data = result["data"]
        data = self.base64.b64decode(data)
        with open(sound_file, "wb") as f:
            f.write(data)

        music = Music()
        music.sound_play(sound_file)