__author__ = "Addison Raak, Michael Antkiewicz, Ka'ulu Ng, Nicholas Baldwin"
__copyright__ = "Copyright 2017-19, Tektronix Inc."
__credits__ = ["Addison Raak", "Michael Antkiewicz", "Ka'ulu Ng", "Nicholas Baldwin"]

import sys
import os
import random
import matplotlib
matplotlib.use('Qt5Agg')

from graph_widget import DrawGraph

from numpy import arange, sin, pi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


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
        layout_container = QtWidgets.QGridLayout()
        self.setLayout(layout_container)

        # create buttons to interact
        self.move_buttons = (QtWidgets.QPushButton("UP"),
                             QtWidgets.QPushButton("DOWN"),
                             QtWidgets.QPushButton("LEFT"),
                             QtWidgets.QPushButton("RIGHT"))

        self.zoom_buttons = (QtWidgets.QPushButton("Zoom In"),
                             QtWidgets.QPushButton("Zoom Out"))

        # add the buttons to the layout
        layout_container.addWidget(self.move_buttons[0], 1, 6, 1, 1)  # UP
        layout_container.addWidget(self.move_buttons[1], 3, 6, 1, 1)  # DOWN
        layout_container.addWidget(self.move_buttons[2], 2, 5, 1, 1)  # LEFT
        layout_container.addWidget(self.move_buttons[3], 2, 7, 1, 1)  # RIGHT

        layout_container.addWidget(self.zoom_buttons[0], 2, 0, 1, 2)  # Zoom In
        layout_container.addWidget(self.zoom_buttons[1], 2, 2, 1, 2)  # Zoom Out

        layout_container.setRowStretch(0, 2)

        layout_container.setColumnStretch(4, 2)
        layout_container.setColumnStretch(0, 2)
        layout_container.setColumnStretch(2, 2)

        # move_button_container.addChildLayout()
        self.move_buttons[0].clicked.connect(self.click_up)
        self.move_buttons[1].clicked.connect(self.click_down)
        self.move_buttons[2].clicked.connect(self.click_left)
        self.move_buttons[3].clicked.connect(self.click_right)

        self.zoom_buttons[0].clicked.connect(self.click_zoom_in)
        self.zoom_buttons[1].clicked.connect(self.click_zoom_out)

        # add graph widget
        self.graph_figure = plt.figure(1, figsize=(5, 10))
        self.graph_canvas = FigureCanvas(self.graph_figure)
        self.graph_widget = DrawGraph(self.graph_figure, self.graph_canvas)

        layout_container.addWidget(self.graph_widget.graph_canvas, 0, 0, 1, 3)

    def click_up(self):
        print("Up button was pressed.")

    def click_down(self):
        print("Down button was pressed.")

    def click_left(self):
        print("Left button was pressed.")

    def click_right(self):
        print("Right button was pressed.")

    def click_zoom_in(self):
        print("Zoom in button pressed.")

    def click_zoom_out(self):
        print("Zoom out button pressed.")

    def keyPressEvent(self, e):
        print(e.key())


# Class for the Side-by-Side Tab
class SideBySideWidget(QtWidgets.QWidget):

    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()

        # layout container for the buttons
        layout_container = QtWidgets.QGridLayout()
        self.setLayout(layout_container)

        # create buttons to interact
        self.move_buttons = (QtWidgets.QPushButton("UP"),
                             QtWidgets.QPushButton("DOWN"),
                             QtWidgets.QPushButton("LEFT"),
                             QtWidgets.QPushButton("RIGHT"))

        self.zoom_buttons = (QtWidgets.QPushButton("Zoom In"),
                             QtWidgets.QPushButton("Zoom Out"))

        # add the buttons to the layout
        layout_container.addWidget(self.move_buttons[0], 1, 6, 1, 1)  # UP
        layout_container.addWidget(self.move_buttons[1], 3, 6, 1, 1)  # DOWN
        layout_container.addWidget(self.move_buttons[2], 2, 5, 1, 1)  # LEFT
        layout_container.addWidget(self.move_buttons[3], 2, 7, 1, 1)  # RIGHT

        layout_container.addWidget(self.zoom_buttons[0], 2, 0, 1, 2)  # Zoom In
        layout_container.addWidget(self.zoom_buttons[1], 2, 2, 1, 2)  # Zoom Out

        layout_container.setRowStretch(0, 2)

        layout_container.setColumnStretch(4, 2)
        layout_container.setColumnStretch(0, 2)
        layout_container.setColumnStretch(2, 2)

        # move_button_container.addChildLayout()
        self.move_buttons[0].clicked.connect(self.click_up)
        self.move_buttons[1].clicked.connect(self.click_down)
        self.move_buttons[2].clicked.connect(self.click_left)
        self.move_buttons[3].clicked.connect(self.click_right)

        self.zoom_buttons[0].clicked.connect(self.click_zoom_in)
        self.zoom_buttons[1].clicked.connect(self.click_zoom_out)

    def click_up(self):
        print("Up button was pressed.")

    def click_down(self):
        print("Down button was pressed.")

    def click_left(self):
        print("Left button was pressed.")

    def click_right(self):
        print("Right button was pressed.")

    def click_zoom_in(self):
        print("Zoom in button pressed.")

    def click_zoom_out(self):
        print("Zoom out button pressed.")


# Main class for adding components to the application
# used for formatting as well
class AppMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        # set the main container's layout
        super(AppMainWindow, self).__init__()
        self.setWindowTitle("Remote RF/Video Monitor")

        # sets the main widget to be the tab manager
        self.main_widget = TabManager()
        self.setCentralWidget(self.main_widget)
        self.setMinimumSize(1500, 1200)
        self.showMaximized()

    def closeEvent(self, event):
        # destructor method
        self.close()


# runs the application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # runs AppMainWindow class as main container
    main_window = AppMainWindow()
    sys.exit(app.exec_())
