from .llm import LLM

class Deepseek(LLM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
            base_url="https://api.deepseek.com",
            **kwargs)

class Grok(LLM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, 
            base_url="https://api.x.ai/v1",
            **kwargs)

class Doubao(LLM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, 
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            **kwargs)

class OpenAI(LLM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, 
            base_url="https://api.openai.com/v1",
            **kwargs)

class Ollama(LLM):
    def __init__(self, ip: str="localhost", *args, api_key: str="ollama", **kwargs):
        base_url = f"http://{ip}:11434/v1"
        super().__init__(*args, 
            base_url=base_url,
            api_key=api_key,
            **kwargs)

class Gemini(LLM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, 
            base_url="https://generativelanguage.googleapis.com/v1beta/openai",
            **kwargs)
