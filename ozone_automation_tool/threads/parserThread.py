from PIL import ImageGrab
import pytesseract
import threading

class ParserThread(threading.Thread):
    def __init__(self, _id, name, wakeword, coords, callback):
        """
        Constructor for ParserThread class.

        @param _id: Thread ID
        @param name: Thread name
        @param wakeword: The word to wake up the parser
        @param coords: Coordinates of the region to capture for parsing
        @param callback: Callback function to invoke when the wakeword is detected
        """
        super().__init__()
        self.daemon = True
        self._id = _id
        self.name = name
        self.killme = False
        self.callback = callback
        self.wakeword = wakeword
        self.coordinates = coords

    def run(self):
        """
        Run the parser thread.

        @return: None
        """
        while True:
            # Capture a screenshot of the specified region
            screenshot = ImageGrab.grab(bbox=self.coordinates)
            # Extract text from the screenshot using Tesseract OCR
            extracted_text = pytesseract.image_to_string(screenshot)
            print(extracted_text)
            # Check if the wakeword is present in the extracted text
            if self.wakeword in extracted_text:
                # Invoke the callback function
                self.callback()
            # Check if the thread should be terminated
            if self.killme:
                break