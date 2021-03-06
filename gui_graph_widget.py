from PyQt5 import QtWidgets
import numpy as np
import matplotlib.pyplot as plt


__author__ = "Cole French, Chris Lytle, Alexander Nowlin, Pouya Rad"
__copyright__ = "Copyright 2019, Tektronix Inc."
__credits__ = ["Cole French", "Chris Lytle", "Alexander Nowlin", "Pouya Rad"]


class GraphWidget(QtWidgets.QWidget):


    def __init__(self, figure, canvas, dpx_graph_data=None):
        super(QtWidgets.QWidget, self).__init__()
        self.__graph_figure = figure
        self.__dpx_graph_data = dpx_graph_data
        self.graph_canvas = canvas

        # graph details
        self.__font_size = 12
        self.__xlabel = "Frequency (GHz)"
        self.__ylabel = "Amplitude (dBm)"
        self.__title = "DPX Spectrum"

        self.draw_DPX_graph()


    def update_graph(self, new_graph_data):
        self.__dpx_graph_data = new_graph_data
        self.draw_DPX_graph()


    # Draws the graph in the log based on the given bitmap data.
    # This is where the attributes are set for data, title, x and y labels,
    # and font size.
    def draw_DPX_graph(self):
        if self.__dpx_graph_data is None:
            return

        # Variables to calculate plot frequency
        cf = self.__dpx_graph_data.center_frequency
        span = self.__dpx_graph_data.span
        refLevel = self.__dpx_graph_data.ref_level
        numTicks = 11
        plotFreq = np.linspace(cf - span / 2.0, cf + span / 2.0, numTicks) / 1e9

        # Set title and axis labels.
        ax = self.__graph_figure.add_subplot(111)
        ax.set_xlabel(self.__xlabel, fontsize=self.__font_size)
        ax.set_ylabel(self.__ylabel, fontsize=self.__font_size)
        ax.set_title(self.__title)

        # Add graph content to the plot.
        ax.imshow(self.__dpx_graph_data.DPX_bitmap, cmap='gist_stern')
        ax.set_aspect(2)
        xTicks = map('{:.3}'.format, plotFreq)
        plt.xticks(np.linspace(0, self.__dpx_graph_data.bitmap_width,
                               numTicks), xTicks)
        yTicks = map('{}'.format, np.linspace(refLevel, refLevel - 100,
                                              numTicks))
        plt.yticks(np.linspace(0, self.__dpx_graph_data.bitmap_height,
                               numTicks), yTicks)
        plt.tight_layout()
        self.graph_canvas.draw()


    # Clears the graph of all data points but keeps
    # the title and axis names
    def clear_graph(self):
        self.__graph_figure.clear()
        self.__dpx_graph_data = None
        self.draw_DPX_graph()
