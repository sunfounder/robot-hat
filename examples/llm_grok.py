from robot_hat.llm import Grok
from secret import GROK_API_KEY

INSTRUCTIONS = "You are a helpful assistant."
WELCOME = "Hello, I am a helpful assistant. How can I help you?"

llm = Grok(
    api_key=GROK_API_KEY,
    model="grok-4-latest",
)

# Set how many messages to keep
llm.set_max_messages(20)
# Set instructions
llm.set_instructions(INSTRUCTIONS)
# Set welcome message
llm.set_welcome(WELCOME)

print(WELCOME)

while True:
    input_text = input(">>> ")

    # Response without stream
    # response = llm.prompt(input_text)
    # print(f"response: {response}")

    # Response with stream
    response = llm.prompt(input_text, stream=True)
    for next_word in response:
        if next_word:
            print(next_word, end="", flush=True)
    print("")
