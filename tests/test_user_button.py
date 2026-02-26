#!/usr/bin/env python3
"""
测试UserButton类的功能
"""

from robot_hat.user_button import UserButton
import time

# 创建UserButton实例
button = UserButton()

# 测试函数
print("测试UserButton类功能")
print("请按下、释放或长按按钮...")
print("按Ctrl+C退出测试")

# 设置回调函数
def on_press():
    print("[事件] 按钮被按下")

def on_release():
    print("[事件] 按钮被释放")

def on_click():
    print("[事件] 按钮被点击")

def on_press_released(state):
    print(f"[事件] 按钮状态变化: {'按下' if state else '释放'}")

def on_long_press():
    print("[事件] 按钮被长按")

def on_long_press_released():
    print("[事件] 长按按钮被释放")

# 注册回调函数
button.set_on_press(on_press)
button.set_on_release(on_release)
button.set_on_click(on_click)
button.set_on_press_released(on_press_released)
button.set_on_long_press(on_long_press, duration=2.0)
button.set_on_long_press_released(on_long_press_released, duration=2.0)

# 持续测试
try:
    while True:
        # 每秒钟打印一次按钮状态
        state = button.is_pressed()
        print(f"[状态] 按钮当前状态: {'按下' if state else '释放'}")
        time.sleep(0.2)
except KeyboardInterrupt:
    print("\n测试结束，退出...")
    button.stop()
