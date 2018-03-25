from PyQt5 import QtWidgets
from app import RobotApp

import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = RobotApp()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
