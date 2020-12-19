import sys
from Trackergui import *

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = Trackergui()

    with open("theme.qss") as my_file:
        theme = my_file.read()
        widget.setStyleSheet(theme)

    widget.ini_gui()
    widget.resize(1000, 1000)
    widget.show()

    sys.exit(app.exec_())