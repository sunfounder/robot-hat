from robot_hat.llm import Doubao
from secret import DOUBAO_API_KEY

INSTRUCTIONS = "You are a helpful assistant."
WELCOME = "Hello, I am a helpful assistant. How can I help you?"

llm = Doubao(
    api_key=DOUBAO_API_KEY,
    model="doubao-seed-1-6-250615",
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
