#!/usr/bin/env python3
"""
Test UserButton class functionality
"""

from robot_hat.user_button import UserButton
import time

# Create UserButton instance
button = UserButton()

# Test functions
print("Testing UserButton class functionality")
print("Please press, release, or long press the button...")
print("Press Ctrl+C to exit the test")

# Set callback functions
def on_press():
    print("[Event] Button pressed")

def on_release():
    print("[Event] Button released")

def on_click():
    print("[Event] Button clicked")

def on_press_released(state):
    print(f"[Event] Button state changed: {'Pressed' if state else 'Released'}")

def on_long_press():
    print("[Event] Button long pressed")

def on_long_press_released():
    print("[Event] Long press button released")

# Register callback functions
button.set_on_press(on_press)
button.set_on_release(on_release)
button.set_on_click(on_click)
button.set_on_press_released(on_press_released)
button.set_on_long_press(on_long_press, duration=2.0)
button.set_on_long_press_released(on_long_press_released, duration=2.0)

# Start listening for button events
button.start()

# Continuous testing
try:
    while True:
        # Print button status every 0.2 seconds
        state = button.is_pressed()
        print(f"[Status] Button current state: {'Pressed' if state else 'Released'}")
        time.sleep(0.2)
except KeyboardInterrupt:
    print("\nTest ended, exiting...")
    button.stop()
