import requests
import os
import logging

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

        self._model = model or self.DEFAULT_MODEL
        self._voice = voice or self.DEFAULT_VOICE
        self._gain = gain
        self.is_ready = False

        self.set_api_key(api_key)

    def tts(self, words, output_file="/tmp/openai_tts.wav"):
        """
        调用OpenAI的语音合成API生成语音文件
        
        参数:
            words (str): 要转换为语音的文本
            output_file (str): 输出MP3文件路径，默认为"speech.mp3"
        
        返回:
            bool: 成功返回True，失败返回False
        """
        
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self._model,
            "input": words,
            "voice": self._voice,
        }
        
        try:
            # 发送POST请求
            response = requests.post(self.URL, json=data, headers=headers, stream=True)
            
            # 检查请求是否成功
            response.raise_for_status()
            
            # 保存响应内容为MP3文件
            with open(output_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # 过滤掉保持连接的空块
                        f.write(chunk)
            
            if self._gain > 1:
                old_output_file = output_file.replace('.wav', f'_old.wav')
                os.rename(output_file, old_output_file)
                volume_gain(old_output_file, output_file, self._gain)
                os.remove(old_output_file)

            print(f"语音文件已成功保存到: {output_file}")
            return True
        
        except requests.exceptions.RequestException as e:
            print(f"请求发生错误: {e}")
            return False
        except IOError as e:
            print(f"文件操作错误: {e}")
            return False

    def say(self, words, instructions=DEFAULT_INSTRUCTIONS):
        '''
        Say words.

        :param words: words to say.
        :type words: str
        :param instructions: instructions.
        :type instructions: str

        '''

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

    def set_gain(self, gain):
        """
        Set gain.

        :param gain: gain.
        :type gain: int
        """
        self._gain = gain
