import json
import os
import sys
import resources
from datetime import datetime, timedelta
from threading import Event, Thread
from PyQt5 import QtWidgets, uic

USER_FILE_PATH = os.path.join(
    os.getenv("LOCALAPPDATA"), "VirtualStore\\Program Files\\Timer App\\db.json"
)


class TimerMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(TimerMainWindow, self).__init__()
        uic.loadUi("qt_ui.ui", self)
        
        self.db_json = read_db()
        categories = [x["name"] for x in self.db_json["categories"]]
        self.category_dropdown.clear()
        self.category_dropdown.addItems(categories)
        self.category_dropdown.setItemDelegate(QtWidgets.QStyledItemDelegate())
        self.category_dropdown.currentTextChanged.connect(self.update_timer_label)
        self.start_stop_button.clicked.connect(self.toggle_timer)
        self.timer_event = None
        self.timer_data = {}
        
        self.show()

    def save_json(self):
        """
        Writes the currently saved JSON values to the database file.
        """
        with open(USER_FILE_PATH, "w") as f:
            f.write(json.dumps(self.db_json))

    def update_timer_label(self, value):
        """
        Updates all timer labels according to the specified category.
        
        Args:
            value: str, category
        """
        self.timer_value.setText(value)
        date_str = datetime.now().strftime("%d-%m-%Y")
        try:
            time = self.db_json["calendar"][date_str][value]
            self.timer_label.setText(time)
        except KeyError:
            self.timer_label.setText("00:00:00")
        

    def create_date(self, date) -> None:
        """
        Creates the specified date in the JSON file it it doesn't exist already.
        
        Args:
            date: datetime, date to be added into the JSON file
        """
        date_str = date.strftime("%d-%m-%Y")
        if date_str not in self.db_json["calendar"]:
            self.db_json["calendar"][date_str] = {}
    
    def init_timer_data(self, date, category):
        """
        Initializes the timer data required in order to start the timer.
        
        Args:
            date: datetime
            category: str, the time tracked will be added to this category
        """
        date_str = date.strftime("%d-%m-%Y")
        self.timer_data = {
          "date": date_str,
          "category": category,
        }
        if category in self.db_json["calendar"][date_str]:
            time_values = self.db_json["calendar"][date_str][category].split(":")
            self.timer_data["time"] = timedelta(
                hours=int(time_values[0]),
                minutes=int(time_values[1]),
                seconds=int(time_values[2])
            )
        else:
            self.timer_data["time"] = timedelta(hours=0, minutes=0, seconds=0)
    
    def save_timer_data(self):
        """
        Saves the currently stored timer values into the database JSON.
        """
        date = self.timer_data["date"]
        category = self.timer_data["category"]
        time = format_timedelta(self.timer_data["time"])
        
        self.db_json["calendar"][date][category] = time

    def toggle_timer(self):
        """
        Starts / stops the timer for the selected category.
        """
        dropdown_str = self.category_dropdown.currentText()
        if dropdown_str:
            if self.category_dropdown.isEnabled():
                current_date = datetime.now()
                self.create_date(current_date)
                self.init_timer_data(current_date, dropdown_str)
                
                self.category_dropdown.setEnabled(False)
                self.timer_event = start_thread(1, self.increment_timer)
            else:
                self.save_timer_data()
                self.save_json()
                self.category_dropdown.setEnabled(True)
                self.timer_event()
    
    def increment_timer(self):
        """
        Increments the time for the selected category.
        """
        self.timer_data["time"] += timedelta(seconds=1)
        self.timer_label.setText(format_timedelta(self.timer_data["time"]))

def format_timedelta(timedelta_val):
    """
    Formats a given timedelta object to a "HH:mm:ss" string.
    
    Args:
        timedelta_val: timedelta, object to be formatted
    """
    hours, remainder = divmod(timedelta_val.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

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
    stop_event = Event()
    def loop():
        while not stop_event.wait(interval):
            func(*args)
    Thread(target=loop, daemon=True).start()
    return stop_event.set

def read_db():
    """
    Ensures that the 'database' file exists and reads its contents into the
    script.
    
    JSON schema:
    {
      "calendar": {
        "28-09-2021": {
          "studying": "03:00:00",
          "household_tasks": "01:00:00"
        },
        "29-09-2021": {
          ...
        },
      },
      "categories": [
        {
          "name": "Name of the category",
          "color:" "Color value of this category",
          "time": "Time spent in this category"
        },
        {
          ...
        }
      ]
    }
    """
    if not os.path.exists(USER_FILE_PATH):
        os.makedirs(os.path.dirname(USER_FILE_PATH), exist_ok=True)
        json_str = '{"calendar": {}, "categories": []}'
        db_json = json.loads(json_str)
        with open(USER_FILE_PATH, "w") as f:
            f.write(json_str)
    else:
        with open(USER_FILE_PATH, "r") as f:
            db_json = json.loads(f.read())
    
    return db_json

def main():
    """
    Starts the PyQt application.
    """
    app = QtWidgets.QApplication(sys.argv)
    window = TimerMainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
