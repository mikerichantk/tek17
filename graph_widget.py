__author__ = "Addison Raak, Michael Antkiewicz, Ka'ulu Ng, Nicholas Baldwin"
__copyright__ = "Copyright 2020, Tektronix Inc."
__credits__ = ["Addison Raak", "Michael Antkiewicz", "Ka'ulu Ng", "Nicholas Baldwin"]

from PyQt5 import QtWidgets
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Class for a FigureCanvas
class DrawGraph(QtWidgets.QWidget):

    def __init__(self, figure, canvas, dpx_graph_data=None):
        super(QtWidgets.QWidget, self).__init__()
        self.graph_figure = figure
        self.graph_data = dpx_graph_data
        self.graph_canvas = canvas

        self.font_size = 12
        self.xLabel = "Frequency (GHz)"
        self.yLabel = "Amplitude (dBm)"
        self.title = "DPX Spectrum"

        self.axes = figure.add_subplot(111)

        self.graph_canvas.draw()

    # Helper method to draw the data on a plot
    # def drawRFgraph(self):
