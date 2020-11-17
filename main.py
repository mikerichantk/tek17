__author__ = "Addison Raak, Michael Antkiewicz, Ka'ulu Ng, Nicholas Baldwin"
__copyright__ = "Copyright 2020, Tektronix Inc. ??????????????????????????????"
__credits__ = ["Addison Raak", "Michael Antkiewicz", "Ka'ulu", "Nicholas Baldwin"]

import sys

from PyQt5 import QtWidgets
from PyQt5 import QtCore


# Class for the main widget of the program, which will have the tab manager
class TabManager(QtWidgets.QWidget):

    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()

        tab_container = QtWidgets.QVBoxLayout()
        self.setLayout(tab_container)

        # create the tab widget itself
        tab_controller = QtWidgets.QTabWidget()

        # make the two tabs needed (overlay and sidebyside)
        tab_controller.addTab(OverlayWidget(), "Overlay")
        tab_controller.addTab(SideBySideWidget(), "Side by Side")

    def on_close(self):
        self.live_tab.on_close()


class OverlayWidget(QtWidgets.QWidget):

    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()

        move_button_container = QtWidgets.QGridLayout()

        # create buttons to interact
        self.move_buttons = (QtWidgets.QPushButton("UP"),
                             QtWidgets.QPushButton("DOWN"))

        # add the buttons to the layout
        move_button_container.addWidget(self.move_buttons[0], 0, 1)
        move_button_container.addWidget(self.move_buttons[1], 1, 1)


class SideBySideWidget(QtWidgets.QWidget):

    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()

        move_button_container = QtWidgets.QGridLayout()

        # create buttons to interact
        self.move_buttons = (QtWidgets.QPushButton("UP"),
                             QtWidgets.QPushButton("DOWN"))

        # add the buttons to the layout
        move_button_container.addWidget(self.move_buttons[0], 0, 1)
        move_button_container.addWidget(self.move_buttons[1], 1, 1)


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

        # sets the main widget to be the tab manager
        self.main_widget = TabManager()
        self.setCentralWidget(self.main_widget)

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
