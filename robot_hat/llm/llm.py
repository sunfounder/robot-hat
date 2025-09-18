
import requests
import base64
import json

class Authorization:
    BEARER = "Bearer"
    API_KEY = "Api-Key"

class LLM():
    DEFAULTMAX_MESSAGES = 20

    def __init__(self, 
        api_key=None,
        model=None,
        url=None,
        base_url=None,
        max_messages=DEFAULTMAX_MESSAGES,
        authorization=Authorization.BEARER
    ):
        self.max_messages = max_messages
        self.model = model
        self.url = url
        self.base_url = base_url
        self.api_key = api_key
        self.authorization = authorization

        self.params = {}
        self.messages = []

        if self.url is None and self.base_url is not None:
            self.url = self.base_url + "/chat/completions"

    def set_api_key(self, api_key):
        self.api_key = api_key

    def set_base_url(self, base_url):
        self.base_url = base_url
        self.url = self.base_url + "/chat/completions"

    def set_model(self, model):
        self.model = model

    def set_max_messages(self, max_messages):
        self.max_messages = max_messages

    def set(self, name, value):
        self.params[name] = value

    def add_message(self, role, content, image_path=None):
        if image_path is not None:
            # get base64 url from image
            base64_url = self.get_base_64_url_from_image(image_path)
            # add to content
            content = [
                {"type": "text", "text": content},
                {"type": "image_url", "image_url": {"url": base64_url}},
            ]

        self.messages.append({"role": role, "content": content})

    def _add_message(self, role, content, image_path=None):
        self.add_message(role, content, image_path)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def get_base64_from_image(self, image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")

    def get_base_64_url_from_image(self, image_path):
        image_type = image_path.split(".")[-1]
        base64 = self.get_base64_from_image(image_path)
        return f"data:image/{image_type};base64,{base64}"

    def set_instructions(self, instructions):
        self._add_message("system", instructions)

    def set_welcome(self, welcome):
        self._add_message("assistant", welcome)

    def chat(self, stream=False):
        # Create headers
        headers = {}
        headers["Content-Type"] = "application/json"
        if self.authorization == Authorization.BEARER:
            headers["Authorization"] = f"Bearer {self.api_key}"

        # Create data
        data = {}
        data["messages"] = self.messages
        data["model"] = self.model
        data["stream"] = stream

        for name, value in self.params.items():
            data[name] = value
        
        # print(f"Chat with URL: {self.url}")
        # print(f"Chat with headers: {headers}")
        # print(f"Chat with data: {data}")
        response = requests.post(self.url, headers=headers, data=json.dumps(data), stream=stream)
        return response

    def prompt(self, msg, image_path=None, stream=False):
        if not self.model:
            raise ValueError("Model not set")

        if not self.api_key:
            raise ValueError("API key not set")

        if not self.url:
            raise ValueError("URL not set")
        
        if isinstance(msg, str):
            self._add_message("user", msg, image_path)
        elif isinstance(msg, list):
            self.messages = msg
        else:
            raise ValueError("Prompt must be a string or a list of messages")

        response = self.chat(stream)

        if stream:
            return self._stream_response(response)
        else:
            return self._non_stream_response(response)

    def decode_stream_response(self, line):
        if not line.startswith('data: '):
            return None

        chunk_str = line[6:]  # Remove 'data: ' prefix
        if chunk_str == "[DONE]":
            return None
        try:
            chunk = json.loads(chunk_str)
        except json.JSONDecodeError:
            return None
        if "choices" in chunk and len(chunk["choices"]) > 0 and \
                "delta" in chunk["choices"][0] and \
                "content" in chunk["choices"][0]["delta"]:
            content = chunk["choices"][0]["delta"]["content"]
            return content

    def _stream_response(self, response):
        full_content = []
        content = ""

        for line in response.iter_lines():
            # print(f"Stream line: {line}")

            if not line:
                continue

            decoded_line = line.decode('utf-8')
            content += decoded_line
            next_word = self.decode_stream_response(decoded_line)
            if next_word:
                full_content.append(next_word)
                yield next_word
        if len(full_content) > 0:
            full_content = ''.join(full_content)
            self._add_message("assistant", full_content)
        else:
            try:
                data = json.loads(content)
                if "error" in data:
                    raise Exception(data["error"]["message"])
            except json.JSONDecodeError:
                pass

    def _non_stream_response(self, response):
        data = response.json()
        response_text = data["choices"][0]["message"]["content"]
        return response_text

    def print_stream(self, stream):
        for next_word in stream:
            if next_word:
                print(next_word, end="", flush=True)
        print("")
