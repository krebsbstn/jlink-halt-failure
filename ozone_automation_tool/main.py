from threads.ioThread import IOThread
from threads.tkinterThread import TkinterThread
from time import sleep

def main():
    """
    The main function to start and manage the threads.

    @return: None
    """

    # Start Tkinter thread for GUI
    tkinter_thread = TkinterThread(2, "tkinter_thread")
    tkinter_thread.start()

    # Start IO thread for mouse and keyboard input
    io_thread = IOThread(
        1,
        "thread_1",
        tkinter_thread.update_mouse_label,
        tkinter_thread.start_stop,
        tkinter_thread.set_rect)

    io_thread.start()

    # Keep the main thread alive while waiting for user input
    while True:
        sleep(1)
        # Check if any thread needs to be terminated
        if io_thread.kill or tkinter_thread.kill:
            break

if __name__ == "__main__":
    main()
