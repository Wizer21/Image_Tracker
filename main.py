import sys
from Main_gui import *

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_gui = Main_gui()

    with open(".\\files\\theme.qss") as my_file:
        theme = my_file.read()
        main_gui.setStyleSheet(theme)

    main_gui.resize(1000, 1000)
    main_gui.show()

    sys.exit(app.exec_())