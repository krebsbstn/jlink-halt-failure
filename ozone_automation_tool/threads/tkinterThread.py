from threads.clickerThread import ClickerThread
from threads.parserThread import ParserThread
import threading
from tkinter import Tk, Toplevel, Entry, Button, Label, Canvas, BOTH
import re

class TkinterThread(threading.Thread):
    def __init__(self, _id, name):
        """
        Constructor for TkinterThread class.

        @param _id: Thread ID
        @param name: Thread name
        """
        super().__init__()
        self.daemon = True
        self._id = _id
        self.name = name
        self.kill = False
        self.clicker = ClickerThread(3, "thread_3", 0, 0)
        self.parser = None

    def open_window(self):
        """
        Open the Tkinter window with labels, buttons, and canvas.

        @return: None
        """
        self.window = Tk()
        self.window.attributes("-topmost", True)
        self.window.geometry("300x160")
        self.mouse_label = Label(self.window, text="Target coordinates: (0, 0)")
        self.mouse_label.grid(row=0, column=0, columnspan=2, pady=5)
        self.parser_label = Label(self.window, text="Parser coordinates: (0, 0, 0, 0)")
        self.parser_label.grid(row=1, column=0, columnspan=2, pady=5)
        self.user_input_entry = Entry(self.window, width=30)
        self.user_input_entry.insert(0, "Wakeword?")
        self.user_input_entry.grid(row=2, column=0, columnspan=2, pady=5)
        self.startstop_button = Button(self.window, text="Start (SPACE)", command=self.start_stop, background="lightgreen")
        self.startstop_button.grid(row=3, column=0, padx=10, pady=5)
        self.cancle_button = Button(self.window, text="Exit (ESC)", command=self.cancle)
        self.cancle_button.grid(row=3, column=1, padx=10, pady=5)
        self.window.protocol("WM_DELETE_WINDOW", self.cancle)

        self.top = Toplevel(self.window)
        self.top.attributes('-transparentcolor', 'grey15')
        self.top.attributes('-topmost', True)
        self.top.attributes('-fullscreen', True)
        self.canvas = Canvas(self.top, bg='grey15', highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=True)

    def set_rect(self, up_left, down_right):
        """
        Set a rectangle on the canvas with specified coordinates.

        @param up_left: Upper-left coordinates of the rectangle
        @param down_right: Bottom-right coordinates of the rectangle
        @return: None
        """
        widget_under_topleft = self.window.winfo_containing(up_left[0], up_left[1])
        if widget_under_topleft == self.window or widget_under_topleft in self.window.winfo_children():
            return
        widget_under_bottomright = self.window.winfo_containing(down_right[0], down_right[1])
        if widget_under_bottomright == self.window or widget_under_bottomright in self.window.winfo_children():
            return
        if self.clicker.is_alive():
            return
        print(f"set rectangle at {up_left} to {down_right}")
        self.parser_label.config(
            text=f"Parser coordinates: ({up_left[0]}, {up_left[1]}, {down_right[0]}, {down_right[1]})")
        self.canvas.delete("rectangle")
        self.canvas.create_rectangle(
            up_left[0], up_left[1], down_right[0], down_right[1],
            outline='red', width=2, tags="rectangle")

    def cancle(self):
        """
        Set the kill flag to True when the window is closed.

        @return: None
        """
        self.kill = True

    def start_stop(self):
        """
        Start or stop threads based on button click.

        @return: None
        """
        if self.window.focus_get() == self.user_input_entry:
            return
        current_text = self.startstop_button.cget("text")
        new_text = "Stop (SPACE)" if current_text == "Start (SPACE)" else "Start (SPACE)"
        new_color = "lightcoral" if current_text == "Start (SPACE)" else "lightgreen"
        self.startstop_button.configure(text=new_text, background=new_color)
        if new_text.startswith("Stop"):
            label_text = self.mouse_label.cget("text")
            parser_label_text = self.parser_label.cget("text")
            wakeword = None
            try:
                x, y = map(int, re.findall(r'\d+', label_text))
                a, b, c, d = map(int, re.findall(r'\d+', parser_label_text))
                wakeword = self.user_input_entry.get()
            except ValueError:
                x, y = 0, 0
                a, b, c, d = 0, 0, 0, 0

            if not wakeword:
                wakeword = "Wakeword?"
                self.user_input_entry.delete(0, "end")
                self.user_input_entry.insert(0, wakeword)

            self.clicker = ClickerThread(3, "thread_3", x, y)
            self.parser = ParserThread(4, "thread_4", wakeword, (a, b, c, d), self.cancle)
            self.clicker.start()
            self.parser.start()
        else:
            if self.clicker is None:
                return
            self.clicker.killme = True
            self.parser.killme = True

    def update_mouse_label(self, x, y):
        """
        Update mouse label and draw a red circle on the canvas.

        @param x: X-coordinate of the mouse
        @param y: Y-coordinate of the mouse
        @return: None
        """
        widget_under_cursor = self.window.winfo_containing(x, y)
        if widget_under_cursor == self.window or widget_under_cursor in self.window.winfo_children():
            return
        if self.clicker.is_alive():
            return
        print(f"set clicker at ({x}, {y})")
        self.mouse_label.config(text=f"Target coordinates: ({x}, {y})")
        self.canvas.delete("mouse")
        radius = 8
        line = 13
        self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            outline='red', width=2, tags="mouse")
        self.canvas.create_line(
            x - line, y, x + line, y,
            fill='red', width=2, tags="mouse")
        self.canvas.create_line(
            x, y - line, x, y + line,
            fill='red', width=2, tags="mouse")

    def run(self):
        """
        Run the Tkinter main loop and destroy the window if the kill flag is True.

        @return: None
        """
        self.open_window()
        self.window.mainloop()
        if self.kill:
            self.window.destroy()
