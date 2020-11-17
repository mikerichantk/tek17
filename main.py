import sys

from PyQt5 import QtWidgets
from PyQt5 import QtCore


class AppMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AppMainWindow, self).__init__()
        WINDOW_WIDTH = 800
        WINDOW_HEIGHT = 640
        STARTING_X_POS = 100
        STARTING_Y_POS = 100

        self.setGeometry(STARTING_X_POS, STARTING_Y_POS, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(QtCore.QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.setWindowTitle("RF Video Monitor")
        self.showMaximized()

    def closeEvent(self, event):
        self.on_close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = AppMainWindow()
    sys.exit(app.exec_())
