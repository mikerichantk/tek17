__author__ = "Addison Raak, Michael Antkiewicz, Ka'ulu Ng, Nicholas Baldwin"
__copyright__ = "Copyright 2020, Tektronix Inc. ??????????????????????????????"
__credits__ = ["Addison Raak", "Michael Antkiewicz", "Ka'ulu Ng", "Nicholas Baldwin"]

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

        tab_container.addWidget(tab_controller)

    def on_close(self):
        # Method inherited from QWidget to close the window
        self.on_close()


# Class for the Overlay Tab
class OverlayWidget(QtWidgets.QWidget):

    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()

        # main layout container for the overlay, and the buttons
        # overlay_container = QtWidgets.QVBoxLayout()
        # self.setLayout(overlay_container)

        # layout container for the buttons
        move_button_container = QtWidgets.QGridLayout()
        self.setLayout(move_button_container)

        # create buttons to interact
        self.move_buttons = (QtWidgets.QPushButton("UP"),
                             QtWidgets.QPushButton("DOWN"),
                             QtWidgets.QPushButton("LEFT"),
                             QtWidgets.QPushButton("RIGHT"))

        # add the buttons to the layout
        move_button_container.addWidget(self.move_buttons[0], 0, 1)  # UP
        move_button_container.addWidget(self.move_buttons[1], 1, 2)  # DOWN
        move_button_container.addWidget(self.move_buttons[2], 1, 0)  # LEFT
        move_button_container.addWidget(self.move_buttons[3], 2, 1)  # RIGHT

        # move_button_container.addChildLayout()
        self.move_buttons[0].clicked.connect(self.click_up)
        self.move_buttons[1].clicked.connect(self.click_down)
        self.move_buttons[2].clicked.connect(self.click_left)
        self.move_buttons[3].clicked.connect(self.click_right)

    def click_up(self):
        print("Up button was pressed.")

    def click_down(self):
        print("Down button was pressed.")

    def click_left(self):
        print("Left button was pressed.")

    def click_right(self):
        print("Down button was pressed.")


# Class for the Side-by-Side Tab
class SideBySideWidget(QtWidgets.QWidget):

    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()

        move_button_container = QtWidgets.QGridLayout()

        self.setLayout(move_button_container)

        # create buttons to interact
        self.move_buttons = (QtWidgets.QPushButton("UP"),
                             QtWidgets.QPushButton("DOWN"),
                             QtWidgets.QPushButton("LEFT"),
                             QtWidgets.QPushButton("RIGHT"))

        # add the buttons to the layout
        move_button_container.addWidget(self.move_buttons[0], 0, 1)  # UP
        move_button_container.addWidget(self.move_buttons[1], 1, 2)  # DOWN
        move_button_container.addWidget(self.move_buttons[2], 1, 0)  # LEFT
        move_button_container.addWidget(self.move_buttons[3], 2, 1)  # RIGHT

        # move_button_container.addChildLayout()
        self.move_buttons[0].clicked.connect(self.click_up)
        self.move_buttons[1].clicked.connect(self.click_down)
        self.move_buttons[2].clicked.connect(self.click_left)
        self.move_buttons[3].clicked.connect(self.click_right)

    def click_up(self):
        print("Up button was pressed.")

    def click_down(self):
        print("Down button was pressed.")

    def click_left(self):
        print("Left button was pressed.")

    def click_right(self):
        print("Right button was pressed.")


# Never called but for the future
class MoveButtons(QtWidgets.QWidget):

    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()

        # layout container for the buttons
        move_button_container = QtWidgets.QGridLayout()
        self.setLayout(move_button_container)

        # create buttons to interact
        self.move_buttons = (QtWidgets.QPushButton("UP"),
                             QtWidgets.QPushButton("DOWN"),
                             QtWidgets.QPushButton("LEFT"),
                             QtWidgets.QPushButton("RIGHT"))

        # add the buttons to the layout
        move_button_container.addWidget(self.move_buttons[0], 0, 1)  # UP
        move_button_container.addWidget(self.move_buttons[1], 1, 2)  # DOWN
        move_button_container.addWidget(self.move_buttons[2], 1, 0)  # LEFT
        move_button_container.addWidget(self.move_buttons[3], 2, 1)  # RIGHT


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
        self.setWindowTitle("Remote RF/Video Monitor")

        # sets the main widget to be the tab manager
        self.main_widget = TabManager()
        self.setCentralWidget(self.main_widget)
        self.show()

    def closeEvent(self, event):
        # destructor method
        self.close()


# runs the application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # runs AppMainWindow class as main container
    main_window = AppMainWindow()
    sys.exit(app.exec_())
