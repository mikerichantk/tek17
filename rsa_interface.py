__author__ = "Addison Raak, Michael Antkiewicz, Ka'ulu Ng, Nicholas Baldwin"
__copyright__ = "Copyright 2017-19, Tektronix Inc."
__credits__ = ["Addison Raak", "Michael Antkiewicz", "Ka'ulu Ng", "Nicholas Baldwin"]

import os
import numpy as np
import DLL_loader
from rsa_config import RSAConfig
from RSA_API import *


class RSAInterface:

    # Creates an RSA object to access its functionality
    rsa = None

    # Default config values for the RSA, can be changed in rsa_config.py
    rsaConfig = RSAConfig()

    def __init__(self):
        # Only is called is the RSA is not already defined
        if RSAInterface.rsa is None:
            # change the directory so the dll file will work
            current_dir = os.getcwd()
            RSAInterface.rsa = RSAInterface.init_RSA_interface(self)
            os.chdir(current_dir)

    # Loads the RSA_API.dll file if it exists
    def init_RSA_interface(self):
        if DLL_loader.change_cwd(DLL_loader.RSA_DLL_PATH_x64):
            rsa = cdll.LoadLibrary(DLL_loader.DLL_FULL_PATH_x64)
            if rsa is not None:
                return rsa
        elif DLL_loader.change_cwd(DLL_loader.RSA_DLL_PATH_x84):
            rsa = WinDLL(DLL_loader.DLL_FULL_PATH_x84)
            if rsa is not None:
                return rsa
        return None

    # Connects to the RSA
    # ################## RSA PDF GUIDE PAGE 6 ################## #
    def connect_rsa(self):
        # throws Not Connected error if the RSA is not initialized
        if RSAInterface.rsa is None:
            raise RSAError(ReturnStatus.errorNotConnected.name)

        # numFound used later to hold number of available RSA's that connected
        # page 6 of pdf
        numFound = c_int(0)
        intArray = c_int(DEVSRCH_MAX_NUM_DEVICES)
        deviceIDs = intArray()
        deviceSerial = create_string_buffer(DEVSRCH_SERIAL_MAX_STRLEN)
        deviceType = create_string_buffer(DEVSRCH_TYPE_MAX_STRLEN)

        # Checks to see how many RSA's are connected. Currently only supports 1.
        if numFound.value < 1:
            print("No RSA found.")
            raise RSAError(ReturnStatus.errorNotConnected.name)
        elif numFound.value == 1:
            print("One Device Found.")
            print("Device Type: {}".format(deviceType.value))
            print("Device Serial Number: {}".format(deviceSerial.value))
            RSAInterface.rsa.DEVICE_Connect(deviceIDs[0])
        else:
            print("More than one device found. Expected one.")

        RSAInterface.rsa.CONFIG_Preset()


    # set the spectrum values to default to avoid communication errors
    # page 16 of RSA_API_Guide pdf
    def config_spectrum(self, rsaCfg):
        RSAInterface.rsa.SPECTRUM_SetEnable(c_bool(True))
        RSAInterface.rsa.CONFIG_SetCenterFreq(rsaCfg.cf)
        RSAInterface.rsa.CONFIG_SetReferenceLevel(rsaCfg.refLevel)
        RSAInterface.SPECTRUM_SetDefault()
        specSet = Spectrum_Settings()
        RSAInterface.__rsa.SPECTRUM_GetSettings(byref(specSet))
        specSet.window = SpectrumWindows.SpectrumWindow_Kaiser
        specSet.verticalUnit = SpectrumVerticalUnits.SpectrumVerticalUnit_dBm
        specSet.span = rsaCfg.span
        specSet.rbw = rsaCfg.rbw
        RSAInterface.rsa.SPECTRUM_SetSettings(specSet)
        RSAInterface.rsa.SPECTRUM_GetSettings(byref(specSet))
        return specSet

    # Check for errors from the RSA
    def error_checker(self, status):
        if ReturnStatus(status) != ReturnStatus.noError:
            raise RSAError(ReturnStatus(status.names))

    # Helper method to disconnect the RSA
    def disconenct_rsa(self):
        RSAInterface.rsa.DEVICE_Disconnect()
