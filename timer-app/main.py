import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class TimerMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(TimerMainWindow, self).__init__()
        uic.loadUi("qt_ui.ui", self)
        self.category_dropdown.setItemDelegate(QtWidgets.QStyledItemDelegate())
        self.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = TimerMainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
