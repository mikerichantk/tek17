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
#arduinoData = serial.Serial("/dev/cu.usbmodem145401", 9600)

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

    # -------------------------------------------------------------------------------
    # Test of Python and Quatanium Python-ONVIF with NETCAT camera PT-PTZ2087
    # ONVIF Client implementation is in Python
    # For IP control of PTZ, the camera should be compliant with ONVIF Profile S
    # The PTZ2087 reports it is ONVIF 2.04 but is actually 2.4 (Netcat said text not changed after upgrade)
    # ------------------------------------------------------------------------------

    if __name__ == '__main__':
        # Do all setup initializations
        import ptzcam

        ptz = ptzcam.ptzcam()

        # *****************************************************************************
        # IP camera motion tests
        # *****************************************************************************
        print
        'Starting tests...'

        # Set preset
        ptz.move_pan(1.0, 1)  # move to a new home position
        ptz.set_preset('home')

        # move right -- (velocity, duration of move)
        ptz.move_pan(1.0, 2)

        # move left
        ptz.move_pan(-1.0, 2)

        # move down
        ptz.move_tilt(-1.0, 2)

        # Move up
        ptz.move_tilt(1.0, 2)

        # zoom in
        ptz.zoom(8.0, 2)

        # zoom out
        ptz.zoom(-8.0, 2)

        # Absolute pan-tilt (pan position, tilt position, velocity)
        # DOES NOT RESULT IN CAMERA MOVEMENT
        ptz.move_abspantilt(-1.0, 1.0, 1.0)
        ptz.move_abspantilt(1.0, -1.0, 1.0)

        # Relative move (pan increment, tilt increment, velocity)
        # DOES NOT RESULT IN CAMERA MOVEMENT
        ptz.move_relative(0.5, 0.5, 8.0)

        # Get presets
        ptz.get_preset()
        # Go back to preset
        ptz.goto_preset('home')


    app = QtWidgets.QApplication(sys.argv)
    # runs AppMainWindow class as main container
    main_window = AppMainWindow()
    sys.exit(app.exec_())
