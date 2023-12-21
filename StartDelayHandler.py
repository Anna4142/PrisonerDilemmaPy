import time
import threading

class StartDelayHandler:
    def __init__(self, delay_duration, callback):
        """
        Initializes the delay handler.

        :param delay_duration: The duration of the delay in seconds.
        :param callback: The function to be called after the delay.
        """
        self.delay_duration = delay_duration
        self.callback = callback

    def start_delay(self):
        """
        Starts the delay in a separate thread.
        """
        delay_thread = threading.Thread(target=self._execute_delay)
        delay_thread.start()

    def _execute_delay(self):
        """
        Waits for the specified duration and then calls the callback function.
        """
        time.sleep(self.delay_duration)
        self.callback()
