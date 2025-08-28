from openai import OpenAI
import os
import base64

class LLM():
    DEFAULT_MAX_MESSAGES = 20

    def __init__(self, api_key=None, model=None, base_url=None, max_messages=DEFAULT_MAX_MESSAGES):
        self._max_messages = max_messages
        self._model = model
        self._base_url = base_url
        self._api_key = api_key
        self.is_ready = False
        self.init()
        self.messages = []

    def init(self):
        if os.environ.get("LLM_API_KEY"):
            self._api_key = os.environ.get("LLM_API_KEY")

        if self._api_key and self._base_url:
            self.client = OpenAI(api_key=self._api_key, base_url=self._base_url)
            self.is_ready = True
        elif self._api_key:
            self.client = OpenAI(api_key=self._api_key)
            self.is_ready = True
        elif self._base_url:
            self.client = OpenAI(base_url=self._base_url)
            self.is_ready = True
        else:
            self.is_ready = False
        


    def set_api_key(self, api_key):
        self._api_key = api_key
        self.init()

    def set_base_url(self, base_url):
        self._base_url = base_url
        self.init()

    def set_model(self, model):
        self._model = model

    def set_max_messages(self, max_messages):
        self._max_messages = max_messages

    def add_message(self, role, content, image_path=None):
        if image_path is not None:
            image_file = self.client.files.create(
                file=open(image_path, "rb"),
                purpose="vision"
            )
            # convert image file to base64
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            # convert base64 to string
            encoded_string = encoded_string.decode("utf-8")
            # add prefix
            encoded_string = "data:image/jpeg;base64," + encoded_string
            # add to content
            content = [
                {"type": "text", "text": content},
                {"type": "image_url", "image_url": {"url": encoded_string}},
            ]

        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self._max_messages:
            self.messages.pop(0)

    def set_instructions(self, instructions):
        self.add_message("system", instructions)

    def set_welcome(self, welcome):
        self.add_message("assistant", welcome)

    def prompt(self, msg, image_path=None, stream=False):

        if not self._model:
            raise ValueError("Model not set")

        if isinstance(msg, str):
            self.add_message("user", msg, image_path)
        elif isinstance(msg, list):
            self.messages = msg
        else:
            raise ValueError("Prompt must be a string or a list of messages")

        response = self.client.chat.completions.create(
            model=self._model,
            messages=self.messages,
            stream=stream,
        )

        if stream:
            return self._stream_response(response)
        else:
            return self._non_stream_response(response)

    def _stream_response(self, response):
        full_content = []
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                full_content.append(chunk.choices[0].delta.content)
                yield chunk.choices[0].delta.content
        full_content = ''.join(full_content)
        self.add_message("assistant", full_content)

    def _non_stream_response(self, response):
        response_text = response.choices[0].message.content
        self.add_message("assistant", response_text)
        return response_text

    def print_stream(self, stream):
        for next_word in stream:
            if next_word:
                print(next_word, end="", flush=True)
        print("")
