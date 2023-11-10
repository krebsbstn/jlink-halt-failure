from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.keyboard import Key as keys
import threading


class IOThread(threading.Thread):
    def __init__(self, _id, name, mouse_callback, start_stop_callback, set_rect_callback):
        """
        Constructor for IOThread class.

        @param _id: Thread ID
        @param name: Thread name
        @param mouse_callback: Callback function for mouse events
        @param start_stop_callback: Callback function for start/stop events
        @param set_rect_callback: Callback function for setting rectangle coordinates
        """
        super().__init__()
        self.daemon = True
        self._id = _id
        self.name = name
        self.mouse_callback = mouse_callback
        self.start_stop_callback = start_stop_callback
        self.set_rect_callback = set_rect_callback
        self.kill = False
        self.current_mouse_pos = (0, 0)
        self.keyboard_listener = KeyboardListener(on_release=self.on_release)
        self.mouse_listener = MouseListener(on_click=self.on_click)

    def on_release(self, key):
        """
        Callback function for key release events.

        @param key: The released key
        @return: None
        """
        if key == keys.esc:
            self.kill = True
            self.keyboard_listener.stop()
            self.mouse_listener.stop()
        elif key == keys.space:
            self.start_stop_callback()

    def on_click(self, x, y, button, pressed):
        """
        Callback function for mouse click events.

        @param x: X-coordinate of the mouse click
        @param y: Y-coordinate of the mouse click
        @param button: The mouse button pressed
        @param pressed: True if the button is pressed, False if released
        @return: None
        """
        if pressed:
            self.current_mouse_pos = (x, y)
        else:
            if self.current_mouse_pos == (x, y):
                self.mouse_callback(x, y)
            else:
                start_coord = min(self.current_mouse_pos, (x, y))
                end_coord = max(self.current_mouse_pos, (x, y))
                self.set_rect_callback(start_coord, end_coord)

    def run(self):
        """
        Run the IOThread.

        @return: None
        """
        self.keyboard_listener.start()
        self.mouse_listener.start()
        self.keyboard_listener.join()
        self.mouse_listener.join()