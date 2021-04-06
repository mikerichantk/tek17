__author__ = "Addison Raak, Michael Antkiewicz, Ka'ulu Ng, Nicholas Baldwin"
__copyright__ = "Copyright 2017-19, Tektronix Inc."
__credits__ = ["Addison Raak", "Michael Antkiewicz", "Ka'ulu Ng", "Nicholas Baldwin"]

import sys
import os
import numpy as np
import matplotlib
import cv2
from PyQt5 import Qt, QtGui
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QApplication, QLabel

matplotlib.use('Qt5Agg')

from gui_graph_widget import GraphWidget

from numpy import arange, sin, pi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from Side_By_Side import Side_By_Side_Tab
from Overlay import Overlay_Tab
import serial

# change this port number based on the machine you are using
# will need to get changed if the USB port changes
arduinoData = serial.Serial("/dev/cu.usbmodem145401", 9600)

# Class for the main widget of the program, which will have the tab manager
class TabManager(QtWidgets.QWidget):

    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()

        tab_container = QtWidgets.QVBoxLayout()
        self.setLayout(tab_container)

        # create the tab widget itself
        tab_controller = QtWidgets.QTabWidget()

        self.side_tab = Side_By_Side_Tab()
        self.overlay_tab = Overlay_Tab()

        # make the two tabs needed (overlay and sidebyside)
        tab_controller.addTab(self.overlay_tab, "Overlay")
        tab_controller.addTab(self.side_tab, "Side by Side")

        tab_container.addWidget(tab_controller)

    def on_close(self):
        # Method inherited from QWidget to close the window
        self.on_close()


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
