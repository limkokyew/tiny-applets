import sys
import resources
from datetime import datetime, timedelta
from threading import Event, Thread
from win10toast import ToastNotifier
from PyQt5 import QtWidgets, QtGui, uic

DEFAULT_TIMEDELTA = timedelta(seconds=0)


class PomodoroMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(PomodoroMainWindow, self).__init__()
        uic.loadUi("qt_ui.ui", self)
        
        self.consecutive_timers = 0
        self.timer = None
        self.timer_data = None
        self.timer_events = None
        self.cancel_button.clicked.connect(self.cancel_timer)
        self.reset_button.clicked.connect(self.reset_timer)
        self.start_button.clicked.connect(self.toggle_timer)
        self.toaster = ToastNotifier()
        
        self.show()
    
    def toggle_timer(self):
        """
        Starts a new timer or pauses / resumes the current timer in use.
        """
        if not self.timer:
            # No timer is currently in use, create a new one
            self.set_consecutive_timers(self.consecutive_timers + 1)
            self.timer_data = timedelta(minutes=1, seconds=0)
            self.time.setText(format_timedelta(self.timer_data))
            self.timer, self.timer_events = start_thread(1, self.decrement_timer)
            self.start_button.setIcon(QtGui.QIcon(":/icons/icon-stop.png"))
        else:
            if self.timer_events[0].is_set():
                # Pause event is set, pause timer
                self.timer_events[0].clear()
                self.start_button.setIcon(QtGui.QIcon(":/icons/icon-stop.png"))
            else:
                # Pause event is not set, resume timer
                self.timer_events[0].set()
                self.start_button.setIcon(QtGui.QIcon(":/icons/icon-play.png"))
    
    def clear_timer(self):
        """
        Cancels the currently running timer, removing it from use.
        """
        self.timer_events[1].set()
        self.timer = None
        self.time.setText("00:00")
        self.start_button.setIcon(QtGui.QIcon(":/icons/icon-play.png"))
    
    def cancel_timer(self):
        """
        Cancels the currently running timer, removing it from use. Updates
        all labels accordingly.
        """
        if self.timer:
            self.clear_timer()
            self.set_consecutive_timers(self.consecutive_timers - 1)

    def reset_timer(self):
        """
        Cancels the currently running timer and sets the amount of consecutive
        timers that have expired to 0 (effectively a full reset). Updates
        all labels accordingly.
        """
        if self.timer:
            self.cancel_timer()
            self.set_consecutive_timers(0)
    
    def decrement_timer(self):
        """
        Decrements the time for the selected category.
        """
        self.timer_data -= timedelta(seconds=1)
        self.time.setText(format_timedelta(self.timer_data))
        
        if self.timer_data <= DEFAULT_TIMEDELTA:
            # Timer has expired
            self.clear_timer()
            if self.consecutive_timers < 4:
                toast_description = "Please take a short break of around 5 " \
                                    "minutes before resuming."
            else:
                toast_description = "Please take a long break of around 20 " \
                                    "minutes before resuming."
                self.set_consecutive_timers(0)
            self.toaster.show_toast(
                "Pomodoro timer expired",
                toast_description,
                duration=15
            )
    
    def set_consecutive_timers(self, value):
        """
        Sets the amount of consecutive timers to the given value and changes
        the timer label accordingly.
        """
        self.consecutive_timers = value
        self.time_label.setText(f"Remaining time ({4 - self.consecutive_timers})")

def format_timedelta(timedelta_val):
    """
    Formats a given timedelta object to a "mm:ss" string.
    
    Args:
        timedelta_val: timedelta, object to be formatted
    """
    hours, remainder = divmod(timedelta_val.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02d}:{:02d}".format(minutes, seconds)

def start_thread(interval, func, *args):
    """
    Starts a new thread running 'func' every 'interval' seconds. Call the return
    value in order to stop the thread.
    
    Args:
        interval: int, wait between function calls
        func: Function to be called every 'interval' seconds
        *args: Arguments that should be passed to 'func'
    
    Returns:
        Event, can be used to stop the thread
    """
    pause_event = Event()
    stop_event = Event()
    pause_event.set()
    
    def loop():
        while not stop_event.wait(interval):
            pause_event.wait()
            func(*args)
    
    thread = Thread(target=loop, daemon=True)
    thread.start()
    return thread, (pause_event, stop_event)


def main():
    """
    Starts the PyQt application.
    """
    app = QtWidgets.QApplication(sys.argv)
    window = PomodoroMainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
