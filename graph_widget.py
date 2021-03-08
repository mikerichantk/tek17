__author__ = "Addison Raak, Michael Antkiewicz, Ka'ulu Ng, Nicholas Baldwin"
__copyright__ = "Copyright 2017-19, Tektronix Inc."
__credits__ = ["Addison Raak", "Michael Antkiewicz", "Ka'ulu Ng", "Nicholas Baldwin"]

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


# This class represents the widget graphing dpx bitmap
# used in top_container_graphs on the live tab for the live and classification graphs
class Graph_Widget(FigureCanvas):
    def __init__(self):
        figure = Figure()
        FigureCanvas.__init__(self, figure)

        ax = self.figure.add_subplot(111)
        ax.set_xlabel("Frequency")
        ax.set_ylabel("Amplitude")
        self.figure.subplots_adjust(bottom=0.2)

    # Updates graph from new_graph_data object that is passed in
    # Parameters:
    #   new_graph_data - DPXData
    def update_graph(self, new_graph_data):
        ax = self.figure.get_axes()[0]

        ax.clear()
        ax.set_xlabel("Frequency")
        ax.set_ylabel("Amplitude")

        num_xticks = 5
        num_yticks = 5

        # set x axis values based on center frequency and span of new_graph_data
        x_start = new_graph_data.center_frequency - new_graph_data.span / 2
        x_end = new_graph_data.center_frequency + new_graph_data.span / 2

        # set y axis values based on reflevel of new_graph_data
        y_start = new_graph_data.ref_level
        y_end = new_graph_data.min_level

        x_ticks = np.linspace(0, new_graph_data.bitmap_width - 1, num_xticks)
        y_ticks = np.linspace(0, new_graph_data.bitmap_height - 1, num_yticks)

        x_ticklabels = list(map(lambda tick: str(tick / 1e6), np.linspace(x_start, x_end, num_xticks)))
        y_ticklabels = np.linspace(y_start, y_end, num_yticks)

        ax.set_xticks(x_ticks)
        ax.set_yticks(y_ticks)

        ax.set_xticklabels(x_ticklabels)
        ax.set_yticklabels(y_ticklabels)

        # display bitmap from new_graph_data on graph
        ax.imshow(new_graph_data.DPX_bitmap, cmap='gist_stern', aspect='auto')

        self.draw()