from robot_hat.llm import OpenAI
from secret import OPENAI_API_KEY
from picamera2 import Picamera2
import time

'''
You need to setup ollama first, see llm_local.py

You need at leaset 8GB RAM to run llava:7b large multimodal model
'''

INSTRUCTIONS = "You are a helpful assistant."
WELCOME = "Hello, I am a helpful assistant. How can I help you?"

llm = OpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4o"
)

# Set how many messages to keep
llm.set_max_messages(20)
# Set instructions
llm.set_instructions(INSTRUCTIONS)
# Set welcome message
llm.set_welcome(WELCOME)

# Init camera
camera = Picamera2()
config = camera.create_still_configuration(
    main={"size": (640, 480)},
)
camera.configure(config)
camera.start()
time.sleep(2)

print(WELCOME)

while True:
    input_text = input(">>> ")

    # Capture image
    img_path = './llm-img.jpg'
    camera.capture_file(img_path)

    # Response without stream
    # response = llm.prompt(input_text, image_path=img_path)
    # print(f"response: {response}")

    # Response with stream
    response = llm.prompt(input_text, stream=True, image_path=img_path)
    for next_word in response:
        if next_word:
            print(next_word, end="", flush=True)
    print("")
