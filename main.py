__author__ = "Addison Raak, Michael Antkiewicz, Ka'ulu Ng, Nicholas Baldwin"
__copyright__ = "Copyright 2017-19, Tektronix Inc."
__credits__ = ["Addison Raak", "Michael Antkiewicz", "Ka'ulu Ng", "Nicholas Baldwin"]

import sys
import os
import random
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')

from gui_graph_widget import DrawGraph

from numpy import arange, sin, pi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import serial

# change this port number based on the machine you are using
# will need to get changed if the USB port changes
arduinoData = serial.Serial("COM6")


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
        self.move_buttons = [QtWidgets.QPushButton("UP"),
                             QtWidgets.QPushButton("DOWN"),
                             QtWidgets.QPushButton("LEFT"),
                             QtWidgets.QPushButton("RIGHT")]

        self.zoom_buttons = [QtWidgets.QPushButton("Zoom In"),
                             QtWidgets.QPushButton("Zoom Out")]

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
        # add axis labels
        ax = self.graph_figure.add_subplot(111)
        ax.set_xlabel("Frequency", fontsize=30)
        ax.set_ylabel("Amplitude", fontsize=30)
        # make the graph
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
        self.__move_buttons = [QtWidgets.QPushButton("UP"),
                             QtWidgets.QPushButton("DOWN"),
                             QtWidgets.QPushButton("LEFT"),
                             QtWidgets.QPushButton("RIGHT")]

        self.__zoom_buttons = [QtWidgets.QPushButton("Zoom In"),
                             QtWidgets.QPushButton("Zoom Out")]

        # add the buttons to the layout
        layout_container.addWidget(self.__move_buttons[0], 1, 6, 1, 1)  # UP
        layout_container.addWidget(self.__move_buttons[1], 3, 6, 1, 1)  # DOWN
        layout_container.addWidget(self.__move_buttons[2], 2, 5, 1, 1)  # LEFT
        layout_container.addWidget(self.__move_buttons[3], 2, 7, 1, 1)  # RIGHT

        layout_container.addWidget(self.__zoom_buttons[0], 2, 0, 1, 2)  # Zoom In
        layout_container.addWidget(self.__zoom_buttons[1], 2, 2, 1, 2)  # Zoom Out

        # formatting the rows and columns, so the drawing of the
        layout_container.setRowStretch(0, 2)

        layout_container.setColumnStretch(4, 2)
        layout_container.setColumnStretch(0, 2)
        layout_container.setColumnStretch(2, 2)

        # move_button_container.addChildLayout()

        # Connects the move buttons to the click_xx methods (calls click_xx when pressed)
        self.__move_buttons[0].clicked.connect(self.click_up)
        self.__move_buttons[1].clicked.connect(self.click_down)
        self.__move_buttons[2].clicked.connect(self.click_left)
        self.__move_buttons[3].clicked.connect(self.click_right)

        ''''
            For some reason, python didn't like iterating over a list of QPushButtons in a for loop?
            If you can figure out how to do this let me know.
            These next four lines makes it so you can press and hold the button down and repeatedly send move
            commands to the arduino (to then move the motors).
        '''
        self.__move_buttons[0].setAutoRepeat(True)
        self.__move_buttons[1].setAutoRepeat(True)
        self.__move_buttons[2].setAutoRepeat(True)
        self.__move_buttons[3].setAutoRepeat(True)

        # Connects the zoom buttons to the zoom_xx methods (calls zoom_xx when pressed)
        self.__zoom_buttons[0].clicked.connect(self.click_zoom_in)
        self.__zoom_buttons[1].clicked.connect(self.click_zoom_out)

    # prints what button was pressed, then sends a move signal to the arduino
    def click_up(self):
        print("Up button was pressed.")
        # uses PySerial to send serial signals to the Arduino, which was previously flashed with the code:
        # "/arduino_mast_control/arduino_mast_control.ino"
        arduinoData.write(b'w')

    def click_down(self):
        print("Down button was pressed.")
        arduinoData.write(b's')

    def click_left(self):
        print("Left button was pressed.")
        arduinoData.write(b'a')

    def click_right(self):
        print("Right button was pressed.")
        arduinoData.write(b'd')

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
