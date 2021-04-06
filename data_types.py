# This class stores the data necessary to graph DPX bitmaps
# that were read from the spectrum analyzer.
class GraphData:
    # The types and descriptions of each of these inputs can be found
    # above its respective instance variable.
    def __init__(self, bitmap, bitmap_width, bitmap_height,
                 center_frequency, span, ref_level, min_level):
        # <numpy.ndarray>: The 2-D array containing the DPX bitmap.
        self.bitmap = bitmap
        # <int>: The number of columns in the bitmap.
        self.bitmap_width = bitmap_width
        # <int>: The number of rows in the bitmap.
        self.bitmap_height = bitmap_height
        # <int>: The center frequency in Hz that the RSA was set to when reading the DPX data.
        self.center_frequency = center_frequency
        # <int>: The span in Hz that the RSA was set to when reading the DPX data.
        self.span = span
        # <int>: The upper bound on power level (the y-axis) that was graphed in dBm.
        # Tektronix calls this yTop in the RSA API documentation.
        self.ref_level = ref_level
        # <int>: The lower bound on power level (the y-axis) that was graphed in dBm.
        # Tektronix calls this yBottom in the RSA API documentation.
        self.min_level = min_level


    # String representation of the DPXGraphData. Used for debugging.
    def __str__(self):
        s = []
        s.append("Bitmap Width: {0}".format(self.bitmap_width))
        s.append("Bithap Height: {0}".format(self.bitmap_height))
        s.append("Center Frequency: {0}".format(self.center_frequency))
        s.append("Span: {0}".format(self.span))
        s.append("Reference Level: {0}".format(self.ref_level))
        s.append("Min Level: {0}".format(self.min_level))
        return " | ".join(s)

#create a DPXGraphData object given a bitmap and the configuration
#used when this bitmap was created
def create_data(bitmap, rsa_config):
    width = bitmap.shape[1]
    height = bitmap.shape[0]

    return GraphData(bitmap, width, height,
                        rsa_config.cf.value, rsa_config.span.value,
                        rsa_config.refLevel.value, rsa_config.refLevel.value - 100)

# This class is an extension of DPXGraphData. It stores
# data that is related to the encapsulated DPXGraphData that is not
# directly necessary for graphing or machine learning analysis.
class CaptureData(GraphData):


    # See the definition of DPXGraphData for information on what
    # these input values should be.
    def __init__(self, bitmap, bitmap_width, bitmap_height,
                 center_frequency, span, ref_level, min_level,
                 capture_timestamp):
        super().__init__(bitmap, bitmap_width, bitmap_height,
            center_frequency, span, ref_level, min_level)
        # A datetime object indicating when this DPX bitmap was captured from the RSA.
        # See https://docs.python.org/3/library/datetime.html for more info
        # on datetime objects.
        self.timestamp = capture_timestamp


    def __str__(self):
        super_str = super().__str__()
        time = " | Timestamp: {0}".format(self.timestamp.strftime("%d/%m/%Y , %H:%M:%S.%f"))
        return super_str + time


# This class stores all of the data necessary to graph
# a DPX data frame, and also stores the label reflecting
# the frame's contents.
class LabeledDPXGraphData(GraphData):


    def __init__(self, bitmap, bitmap_width, bitmap_height,
                 center_frequency, span, ref_level, min_level, signal_type):
        super().__init__(bitmap, bitmap_width, bitmap_height,
            center_frequency, span, ref_level, min_level)
        self.signal_type = signal_type
