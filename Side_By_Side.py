__author__ = "Addison Raak, Michael Antkiewicz, Ka'ulu Ng, Nicholas Baldwin"
__copyright__ = "Copyright 2017-19, Tektronix Inc."
__credits__ = ["Addison Raak", "Michael Antkiewicz", "Ka'ulu Ng", "Nicholas Baldwin"]

import matplotlib
import cv2
from PyQt5 import Qt, QtGui
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QApplication, QLabel

matplotlib.use('Qt5Agg')

from gui_graph_widget import GraphWidget
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
import matplotlib.pyplot as plt
import serial
from data_stream import *
from graph_widget import *
from threading import Thread
arduinoData = serial.Serial("COM6", 9600)

# code sourced from https://gist.github.com/docPhil99/ca4da12c9d6f29b9cea137b617c7b8b1
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        # camera address: "rtsp://169.254.161.100:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream"
        # use 0 if you want to test with laptop camera
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


class Side_By_Side_Tab(QtWidgets.QWidget):

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

        layout_container.setRowStretch(0, 2)
        layout_container.setColumnStretch(4, 2)
        layout_container.setColumnStretch(0, 2)
        layout_container.setColumnStretch(2, 2)

        # move_button_container.addChildLayout()
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

        self.__zoom_buttons[0].clicked.connect(self.click_zoom_in)
        self.__zoom_buttons[1].clicked.connect(self.click_zoom_out)

        # add graph widget
        self.graph_figure = plt.figure(1, figsize=(5, 10))
        # add axis labels
        ax = self.graph_figure.add_subplot(111)
        ax.set_xlabel("Frequency", fontsize=30)
        ax.set_ylabel("Amplitude", fontsize=30)
        # make the graph
        self.graph_canvas = FigureCanvas(self.graph_figure)
        self.graph_widget = GraphWidget(self.graph_figure, self.graph_canvas)

        # start the stream
        self.stream = create_data_stream()
        self.live_stream_graph = Graph_Widget()

        layout_container.addWidget(self.live_stream_graph, 0, 0, 1, 3)

        thread = Thread(target=self.update_live_widget)
        thread.start()

        # thread target function
        # Opens dpx data stream and grabs frame from RSA while the stream remains open

    def update_live_widget(self):
        try:
            self.stream.open()
        except (RSAError, ValueError) as err:
            self.popup.show_popup("Could not connect to RSA", str(err))
            return

        for data in self.stream.get_dpx_data_while_open():
            self.live_stream_graph.update_graph(data)

    def closeEvent(self, event):
            self.thread.stop()
            event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
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
        self.main_widget = Side_By_Side_Tab()
        self.setCentralWidget(self.main_widget)
        self.setMinimumSize(1500, 1200)
        self.showMaximized()

    def closeEvent(self, event):
        # destructor method
        self.close()


# runs the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = Side_By_Side_Tab()
    a.show()
    sys.exit(app.exec_())
