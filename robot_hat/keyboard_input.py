import threading
import sys
import select

class KeyboardInput:
    def __init__(self):
        self.thread = None
        self.running = False
        self.result = None

    def start(self):
        if self.running:
            return
        self.thread = threading.Thread(name="Keyboard Input Thread", target=self.main)
        self.thread.start()

    def main(self):
        self.running = True
        self.result = None
        print(">>> ", end="", flush=True)

        while self.running:
            if select.select([sys.stdin], [], [], 0.1)[0]:  # 0.1秒超时
                self.result = sys.stdin.readline().strip()
                break  # 有输入时退出循环

        self.running = False

    def is_result_ready(self):
        return self.result is not None

    def stop(self):
        if not self.running:
            return
        self.running = False
        self.result = None
        self.thread.join()

if __name__ == "__main__":
    try:
        keyboard_input = KeyboardInput()
        while True:
            keyboard_input.start()
            while True:
                if keyboard_input.is_result_ready():
                    print(f"Received: {keyboard_input.result}")
                    keyboard_input.stop()
                    break
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        keyboard_input.stop()
