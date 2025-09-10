from robot_hat.tts import OpenAI_TTS
from secret import OPENAI_API_KEY

# Export your OpenAI_API_KEY before running the script
# export OPENAI_API_KEY="sk-proj-xxxxxx"

tts = OpenAI_TTS(api_key=OPENAI_API_KEY)
# tts.set_model('tts-1')
tts.set_voice('alloy')
tts.set_model('gpt-4o-mini-tts')

msg = "Hello! I'm OpenAI TTS."
print(f"Say: {msg}")
tts.say(msg)

msg = "with instructions, I can say word sadly"
instructions = "say it sadly"
print(f"Say: {msg}, with instructions: '{instructions}'")
tts.say(msg, instructions=instructions)

msg = "or say something dramaticly."
instructions = "say it dramaticly"
print(f"Say: {msg}, with instructions: '{instructions}'")
tts.say(msg, instructions=instructions)
