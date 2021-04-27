__author__ = "Addison Raak, Michael Antkiewicz, Ka'ulu Ng, Nicholas Baldwin"
__copyright__ = "Copyright 2017-19, Tektronix Inc."
__credits__ = ["Addison Raak", "Michael Antkiewicz", "Ka'ulu Ng", "Nicholas Baldwin"]

from threading import Thread
from PyQt5 import QtWidgets, QtCore
from data_stream import *
import popup as pw


# This class handles the error popups
class ErrorPopup(QtCore.QObject):
    popup_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.popup_signal.connect(self.__do_popup)
        self.error_message = None
        self.details = None

    # method to be called when a popup should be shown
    # takes the message and details
    def show_popup(self, error_message, details):
        self.error_message = error_message
        self.details = details
        self.popup_signal.emit()

    # QT slot to be triggered when the show_popup method is called
    def __do_popup(self):
        pw.show_error_message(error_message=self.error_message, details=self.details)


# This class represents the widget "Live" tab of the software.
class LiveFeed(QtWidgets.QWidget):

    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        self.output_directory = None

        #create mock dpx data stream, generates random data
        self.stream = create_data_stream()

        # create the main window
        main_container = QtWidgets.QGridLayout()
        self.setLayout(main_container)

        #create widget that contains both graphs at top of tab
        self.graphs_widget = Top_Container_Widget()
        main_container.addWidget(self.graphs_widget, 0, 0, 50, 100)

        #create and add buttons to layout
        self.buttons_widget = Live_Buttons_Widget(self.liveButtonClick, self.grabButtonClicked, self.stopButtonClicked)
        main_container.addWidget(self.buttons_widget,50, 0, 10, 100)

        #add settings widget to main container
        main_container.addWidget(self.settings_Widget, 60, 0, 20, 100)

        self.grabCount = 0

        self.popup= ErrorPopup()

        self.updateRSASettings()

    # This method is called when the window is closed
    # closes stream if it is open and ends the fast grab thread
    def on_close(self):
        if self.stream.is_open():
            self.stream.close()

        self.settings_Widget.fast_grab_box.setChecked(False)

    # Listener for "start live" button
    # creates thread that calls update_live_widget
    def liveButtonClick(self):
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
            self.graphs_widget.live_stream_graph.update_graph(data)

    # Listener function for "Grab" button
    # this function is also called during fast grab each time a frame is grabbed
    # takes previous data frame and saves it to dsi file

    # listener for "Stop Live" button
    def stopButtonClicked(self):
        #close stream if it is open
        if self.stream.is_open():
            self.stream.close()