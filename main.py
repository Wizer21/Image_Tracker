import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from Trackergui import *

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = Trackergui()
    widget.ini_gui()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())