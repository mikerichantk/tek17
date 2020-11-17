import sys

from PyQt5 import QtWidgets
from PyQt5 import QtCore


# Main class for adding components to the application
# used for formatting as well
class AppMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # set the main container's layout
        super(AppMainWindow, self).__init__()
        WINDOW_WIDTH = 800
        WINDOW_HEIGHT = 640
        STARTING_X_POS = 100
        STARTING_Y_POS = 100
        # sets the starting position and window dimensions
        self.setGeometry(STARTING_X_POS, STARTING_Y_POS, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(QtCore.QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.setWindowTitle("RF Video Monitor")
        # init the window as full screen
        self.showMaximized()

    def closeEvent(self, event):
        # destructor method
        self.on_close()


# runs the application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # runs AppMainWindow class as main container
    main_window = AppMainWindow()
    sys.exit(app.exec_())
