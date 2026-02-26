import time
import threading
import warnings
from typing import Callable
from .pin import Pin

class UserButton:
    """ User button class using Pin for GPIO input events
    """

    def __init__(self) -> None:
        self.pressed = False
        self.pressed_for = 0
        self.pressed_at = time.time()
        self._pin = Pin("USER", Pin.IN, Pin.PULL_UP)

        self.__on_click__ = None
        self.__on_press__ = None
        self.__on_release__ = None
        self.__on_press_released__ = None
        self.__on_long_press__ = None
        self.__on_long_press_released__ = None
        self._long_press_duration = 2.0
        self._long_press_timer = None
        self._long_press_triggered = False
        self._running = True

        self._setup_event_listener()

    def set_on_click(self, callback: Callable[[], None]) -> None:
        """ Set callback function when the user button is clicked

        Args:
            callback (Callable[[], None]): callback function
        """
        self.__on_click__ = callback

    def set_on_press(self, callback: Callable[[], None]) -> None:
        """ Set callback function when the user button is pressed

        Args:
            callback (Callable[[], None]): callback function
        """
        self.__on_press__ = callback

    def set_on_release(self, callback: Callable[[], None]) -> None:
        """ Set callback function when the user button is released

        Args:
            callback (Callable[[], None]): callback function
        """
        self.__on_release__ = callback

    def set_on_press_released(self, callback: Callable[[], None]) -> None:
        """ Set callback function when the user button is pressed and released

        Args:
            callback (Callable[[], None]): callback function
        """
        self.__on_press_released__ = callback

    def set_on_long_press(self, callback: Callable[[], None], duration: float=2.0) -> None:
        """ Set callback function when the user button is pressed for a long time

        Args:
            callback (Callable[[], None]): callback function
            duration (float, optional): long press duration(2.0~5.0)
        """
        self.__on_long_press__ = callback
        self._long_press_duration = max(2.0, min(5.0, duration))

    def set_on_long_press_released(self, callback: Callable[[], None], duration: float=2.0) -> None:
        """ Set callback function when the user button is pressed for a long time and released

        Args:
            callback (Callable[[], None]): callback function
            duration (float, optional): long press duration(2.0~5.0)
        """
        self.__on_long_press_released__ = callback
        self._long_press_duration = max(2.0, min(5.0, duration))

    def get_state(self) -> bool:
        """ Get the state of the user button

        Returns:
            bool: True if pressed, False if released
        """
        return self.pressed

    def is_pressed(self) -> bool:
        """
        Check if the user button is pressed

        Returns:
            bool: True if pressed, False if released
        """
        return self.get_state()

    def get_pressed_for(self) -> float:
        """
        Get the time the user button has been pressed for

        Returns:
            float: time in seconds
        """ 
        if self.is_pressed():
            return time.time() - self.pressed_at
        return self.pressed_for

    def _setup_event_listener(self) -> None:
        def _long_press_handler():
            if self.pressed and not self._long_press_triggered:
                self._long_press_triggered = True
                if self.__on_long_press__ is not None:
                    self.__on_long_press__()

        def _poll_thread():
            last_state = self._pin.value()
            while self._running:
                try:
                    current_state = self._pin.value()
                    
                    if current_state != last_state:
                        if not current_state:
                            if not self.pressed:
                                self.pressed = True
                                self.pressed_at = time.time()
                                self._long_press_triggered = False
                                if self.__on_press__ is not None:
                                    self.__on_press__()
                                if self.__on_press_released__ is not None:
                                    self.__on_press_released__(True)
                                if self.__on_long_press__ is not None or self.__on_long_press_released__ is not None:
                                    self._long_press_timer = threading.Timer(self._long_press_duration, _long_press_handler)
                                    self._long_press_timer.daemon = True
                                    self._long_press_timer.start()
                        else:
                            if self.pressed:
                                if self._long_press_timer:
                                    self._long_press_timer.cancel()
                                    self._long_press_timer = None
                                
                                self.pressed = False
                                self.pressed_for = time.time() - self.pressed_at
                                if self.__on_release__ is not None:
                                    self.__on_release__()
                                if self.__on_press_released__ is not None:
                                    self.__on_press_released__(False)
                                if self._long_press_triggered and self.__on_long_press_released__ is not None:
                                    self.__on_long_press_released__()
                                elif not self._long_press_triggered and self.__on_click__ is not None:
                                    self.__on_click__()
                        
                        last_state = current_state
                except Exception:
                    pass
                
                time.sleep(0.05)

        self._poll_thread = threading.Thread(target=_poll_thread, daemon=True)
        self._poll_thread.start()

    def start(self) -> None:
        """ 此方法已弃用，不再需要调用 
        
        由于使用了轮询方式，按钮事件会自动被监听和处理，无需手动启动轮询循环。
        """
        warnings.warn(
            "UserButton.start() 方法已弃用。由于使用了轮询方式，按钮事件会自动被监听和处理。",
            DeprecationWarning,
            stacklevel=2
        )

    def stop(self) -> None:
        """ 关闭按钮设备连接 """
        self._running = False
        
        # 取消长按定时器
        if hasattr(self, '_long_press_timer') and self._long_press_timer:
            try:
                self._long_press_timer.cancel()
            except Exception:
                pass
            self._long_press_timer = None
        
        # 关闭Pin实例
        if hasattr(self, '_pin') and self._pin:
            try:
                self._pin.close()
            except Exception:
                pass
            self._pin = None
