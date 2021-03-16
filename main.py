__author__ = "Addison Raak, Michael Antkiewicz, Ka'ulu Ng, Nicholas Baldwin"
__copyright__ = "Copyright 2020, Tektronix Inc."
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

from graph_widget import DrawGraph

from numpy import arange, sin, pi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
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


#code sourced from https://gist.github.com/docPhil99/ca4da12c9d6f29b9cea137b617c7b8b1
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture("rtsp://169.254.161.100:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream")
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


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

        # add graph widget
        self.graph_figure = plt.figure(1, figsize=(5, 10))
        self.graph_canvas = FigureCanvas(self.graph_figure)
        self.graph_widget = DrawGraph(self.graph_figure, self.graph_canvas)
        layout_container.addWidget(self.graph_widget.graph_canvas, 0, 0, 1, 3)

        #add temporary box where video feed will go
        videoBox = QVBoxLayout()
        videoFrame = QFrame(self)
        videoFrame.setFrameShape(QFrame.StyledPanel)
        videoFrame.setLineWidth(0.6)
        videoFrame.setGeometry(1000, 100, 800, 600)
        videoBox.addWidget(videoFrame)
        self.setLayout(videoBox)

        self.display_width = 640
        self.display_height = 480
        self.image_label = QLabel(self)
        self.image_label.resize(self.display_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')

        ###sourced from https://gist.github.com/docPhil99/ca4da12c9d6f29b9cea137b617c7b8b1###
        # create a vertical box layout and add the two labels
        videoBox.addWidget(self.image_label)
        videoBox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(videoBox)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        #self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

        def closeEvent(self, event):
            self.thread.stop()
            event.accept()

        @pyqtSlot(np.ndarray)
        def update_image(self, cv_img):
            """Updates the image_label with a new opencv image"""
            qt_img = self.convert_cv_qt(cv_img)
            self.image_label.setPixmap(qt_img)

        def convert_cv_qt(self, cv_img):
            """Convert from an opencv image to QPixmap"""
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
            return QPixmap.fromImage(p)

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
    a = SideBySideWidget()
    a.show()
    sys.exit(app.exec_())


    #app = QApplication(sys.argv)
    #a = SideBySideWidget()
    #a.show()
    #sys.exit(app.exec_())