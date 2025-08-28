from openai import OpenAI
import logging
import os

class OpenAI_STT():
    LANGUAGES = {
        "Afrikaans": "af",
        "Arabic": "ar",
        "Armenian": "hy",
        "Azerbaijani": "az",
        "Belarusian": "be",
        "Bosnian": "bs",
        "Bulgarian": "bg",
        "Catalan": "ca",
        "Chinese": "zh",
        "Croatian": "hr",
        "Czech": "cs",
        "Danish": "da",
        "Dutch": "nl",
        "English": "en",
        "Estonian": "et",
        "Finnish": "fi",
        "French": "fr",
        "Galician": "gl",
        "German": "de",
        "Greek": "el",
        "Hebrew": "he",
        "Hindi": "hi",
        "Hungarian": "hu",
        "Icelandic": "is",
        "Indonesian": "id",
        "Italian": "it",
        "Japanese": "ja",
        "Kannada": "kn",
        "Kazakh": "kk",
        "Korean": "ko",
        "Latvian": "lv",
        "Lithuanian": "lt",
        "Macedonian": "mk",
        "Malay": "ms",
        "Marathi": "mr",
        "Maori": "mi",
        "Nepali": "ne",
        "Norwegian": "no",
        "Persian": "fa",
        "Polish": "pl",
        "Portuguese": "pt",
        "Romanian": "ro",
        "Russian": "ru",
        "Serbian": "sr",
        "Slovak": "sk",
        "Slovenian": "sl",
        "Spanish": "es",
        "Swahili": "sw",
        "Swedish": "sv",
        "Tagalog": "tl",
        "Tamil": "ta",
        "Thai": "th",
        "Turkish": "tr",
        "Ukrainian": "uk",
        "Urdu": "ur",
        "Vietnamese": "vi",
        "Welsh": "cy",
    }

    DEFAULT_MODEL = "whisper-1"

    def __init__(self, api_key=None, model=DEFAULT_MODEL, language=None, log=None):
        self.log = log or logging.getLogger(__name__)
        self._model = model
        self._language = language
        self.is_ready = False
        if api_key:
            self.set_api_key(api_key)
        else:
            if os.environ.get("OPENAI_API_KEY"):
                self.client = OpenAI()
                self.is_ready = True

    def stt(self, filename, stream=False):
        with open(filename, "rb") as file:
            options = {
                "model": self._model,
                "file": file,
                "response_format": "text",
            }
            if self._language:
                options["language"] = self._language
            if stream:
                options["stream"] = stream

            transcription = self.client.audio.transcriptions.create(
                **options
            )
            if stream:
                for chunk in transcription:
                    if hasattr(chunk, "delta"):
                        yield chunk.delta
            else:
                return transcription


    def set_api_key(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.is_ready = True

    def set_model(self, model):
        self._model = model

    def set_language(self, language):
        self._language = language
