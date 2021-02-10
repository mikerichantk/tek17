__author__ = "Addison Raak, Michael Antkiewicz, Ka'ulu Ng, Nicholas Baldwin"
__copyright__ = "Copyright 2021, Tektronix Inc."
__credits__ = ["Addison Raak", "Michael Antkiewicz", "Ka'ulu Ng", "Nicholas Baldwin"]

from RSA_API import *


# RSAConfig is a record class
# it holds all necessary configurations to configure an RSA
# these types are stored as ctypes in order to easily interface with the RSA API
class RSAConfig:
    def __init__(self, cf=5e9, refLevel=0, refLevelOffset=100, span=40e6, rbw=None, persistence=1.0):
        if rbw is None:
            rbw = span/100

        self.span = c_double(span)
        self.rbw = c_double(rbw)  # resolution bandwidth
        self.bitmapWidth = c_int(801)
        self.tracePtsPerPixel = c_int(1)
        self.yUnit = VerticalUnitType.VerticalUnit_dBm
        self.yTop = c_double(refLevel)
        self.yBottom = c_double(refLevel - refLevelOffset)
        self.infinitePersistence = c_bool(False)
        self.persistenceTimeSec = c_double(persistence)
        self.showOnlyTrigFrame = c_bool(False)

        self.cf = c_double(cf)  # center frequency
        self.refLevel = c_double(refLevel)
        self.refLevelOffset = c_double(refLevelOffset)

