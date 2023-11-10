import threading
import mouse as ms
from time import sleep

class ClickerThread(threading.Thread):
    def __init__(self, _id, name, x, y):
        """
        Constructor for ClickerThread class.

        @param _id: Thread ID
        @param name: Thread name
        @param x: X-coordinate for mouse click
        @param y: Y-coordinate for mouse click
        """
        super().__init__()
        self.daemon = True
        self._id = _id
        self.name = name
        self.killme = False
        self.x = x
        self.y = y

    def run(self):
        """
        Run the clicker thread.

        @return: None
        """
        while True:
            print("CLICK!!")
            # Move the mouse to the specified coordinates
            ms.move(self.x, self.y)
            # Perform a left-click
            ms.click("left")
            # Pause for 1 second
            sleep(1)
            if self.killme:
                break