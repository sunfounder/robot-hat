from robot_hat.voice_assistant import VoiceAssistant
from robot_hat.llm import OpenAI as LLM
from secret import OPENAI_API_KEY as API_KEY

# ── TTS engines ──────────────────────────────────────────────────────────
# Pick one. The VoiceAssistant accepts any TTS instance via the `tts=` parameter.

# Default: EdgeTTS — free cloud TTS, 100+ voices, no API key
from robot_hat.tts import EdgeTTS
tts = EdgeTTS(voice="en-US-AriaNeural")

# Piper — local neural TTS, offline, fast (but slow on Pi Zero)
# from sunfounder_voice_assistant.tts import Piper
# tts = Piper(model="en_US-ryan-low")

# Espeak — compact offline TTS, robotic, fastest
# from sunfounder_voice_assistant.tts import Espeak
# tts = Espeak()

# OpenAI TTS — cloud TTS via gpt-4o-mini-tts
# from sunfounder_voice_assistant.tts import OpenAI_TTS
# tts = OpenAI_TTS(voice="coral", api_key=API_KEY)

# Pico2Wave — compact offline TTS
# from sunfounder_voice_assistant.tts import Pico2Wave
# tts = Pico2Wave()

# ── LLM ──────────────────────────────────────────────────────────────────
llm = LLM(
    api_key=API_KEY,
    model="gpt-4o-mini",
)

# Robot name
NAME = "Buddy"

# Enable image, need to set up a multimodal language model
WITH_IMAGE = True

# Set models and languages
LLM_MODEL = "gpt-4o-mini"
STT_LANGUAGE = "en-us"

# Enable keyboard input
KEYBOARD_ENABLE = True

# Enable wake word
WAKE_ENABLE = True
WAKE_WORD = [f"hey {NAME.lower()}"]
# Set wake word answer, set empty to disable
ANSWER_ON_WAKE = "Hi there"

# Welcome message
WELCOME = f"Hi, I'm {NAME}. Wake me up with: " + ", ".join(WAKE_WORD)

# Set instructions
INSTRUCTIONS = f"""
You are a helpful assistant, named {NAME}.
"""

va = VoiceAssistant(
    llm,
    name=NAME,
    with_image=WITH_IMAGE,
    tts=tts,
    stt_language=STT_LANGUAGE,
    keyboard_enable=KEYBOARD_ENABLE,
    wake_enable=WAKE_ENABLE,
    wake_word=WAKE_WORD,
    answer_on_wake=ANSWER_ON_WAKE,
    welcome=WELCOME,
    instructions=INSTRUCTIONS,
)

if __name__ == "__main__":
    va.run()
