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

    # NOTE: Use this function instead of __init__ when creating an instance of
    #   the RSA object.
    # Description: This method exists to ensure that the instance
    # of the class that is used has properly loaded the rsa functionality.
    #
    # Returns:
    #   This method returns an instance of the RSAInterface class,
    #   or returns None if the dll could not be loaded.
    #   It is recommended that any users of this class check for
    #   a None result when getting instances of this class.
    # Author: DPX Capstone Team
    @staticmethod
    def get_instance():
        instance = RSAInterface()
        if RSAInterface.rsa is None:
            return None
        else:
            return instance

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
        intArray = c_int * DEVSRCH_MAX_NUM_DEVICES
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

    # refLevel and refLevelOffset are used to determine the upper and lower bounds
    # for the y-axis of the frame.
    # The upper bound is given by refLevel in dBm.
    # The lower bound is the refLevel - refLevelOffset; refLevelOffset should be in dBm.
    def config_DPX(self, rsaCfg):
        # DPX_SetParameters(double fspan, double rbw, int32_t bitmapWidth,int32_t tracePtsPerPixel,
        # VerticalUnitTypes yUnit,double yTop, double yBottom,bool inﬁnitePersistence,
        # double persistenceTimeSec,bool showOnlyTrigFrame)
        yTop = rsaCfg.yTop
        yBottom = rsaCfg.yBottom
        yUnit = rsaCfg.yUnit

        dpxSet = DPX_SettingStruct()
        RSAInterface.rsa.CONFIG_SetCenterFreq(rsaCfg.cf)
        RSAInterface.rsa.CONFIG_SetReferenceLevel(rsaCfg.refLevel)

        RSAInterface.rsa.DPX_SetEnable(c_bool(True))
        RSAInterface.rsa.DPX_SetParameters(rsaCfg.span, rsaCfg.rbw, rsaCfg.bitmapWidth, rsaCfg.tracePtsPerPixel,
                                           rsaCfg.yUnit, rsaCfg.yTop, rsaCfg.yBottom, rsaCfg.infinitePersistence,
                                           rsaCfg.persistenceTimeSec,
                                           rsaCfg.showOnlyTrigFrame)  # rsaCfg.persistenceTimeSec, rsaCfg.showOnlyTrigFrame)

        RSAInterface.rsa.DPX_SetSogramParameters(c_double(1e-3), c_double(1e-3),
                                                 rsaCfg.refLevel,
                                                 c_double(rsaCfg.refLevel.value - rsaCfg.refLevelOffset.value))
        RSAInterface.rsa.DPX_Configure(c_bool(True), c_bool(True))

        RSAInterface.rsa.DPX_SetSpectrumTraceType(c_int32(0), c_int(2))
        RSAInterface.rsa.DPX_SetSpectrumTraceType(c_int32(1), c_int(4))
        RSAInterface.rsa.DPX_SetSpectrumTraceType(c_int32(2), c_int(0))

        RSAInterface.rsa.DPX_GetSettings(byref(dpxSet))
        # print(dpxSet.persistenceTimeSec)
        dpxFreq = np.linspace((rsaCfg.cf.value - rsaCfg.span.value / 2), (rsaCfg.cf.value + rsaCfg.span.value / 2),
                              dpxSet.bitmapWidth)
        dpxAmp = np.linspace(yBottom, yTop, dpxSet.bitmapHeight)
        return dpxFreq, dpxAmp

    # return a frame buffer from a connected RSA
    def acquire_dpx_frame(self, trigger=None, max_attempts=10):
        frameAvailable = c_bool(False)
        ready = c_bool(False)
        fb = DPX_FrameBuffer()

        RSAInterface.__rsa.DEVICE_Run()

        if trigger is None:
            # set rsa to free mode (0), as opposed to triggered mode (0)
            RSAInterface.rsa.TRIG_SetTriggerMode(TriggerMode.freeRun)
        else:
            # set rsa to triggered mode (1), as opposed to free mode (0)
            RSAInterface.rsa.TRIG_SetTriggerMode(TriggerMode.triggered)

            # set rsa to power trigger (1), as opposed to external source trigger (0)
            RSAInterface.rsa.TRIG_SetTriggerSource(TriggerSource.TriggerSourceIFPowerLevel)

            # set power level and position percent
            RSAInterface.rsa.TRIG_SetIFPowerTriggerLevel(c_double(trigger.power_level))
            RSAInterface.rsa.TRIG_SetTriggerPositionPercent(c_int(int(trigger.position_percent)))

            # either transition high to low or low to high
            RSAInterface.rsa.TRIG_SetTriggerTransition(TriggerTransition.TriggerTransitionEither)

        # track the number of attempts, raise RuntimeError exception if
        # the attempts exceeds the max
        attempts = 0
        while not frameAvailable.value:
            RSAInterface.rsa.DPX_IsFrameBufferAvailable(byref(frameAvailable))
            while not ready.value:
                attempts += 1
                if trigger is None and attempts > max_attempts:
                    raise RSAError(
                        "Maximum attempts exceeded: failed to acquire frame {} times".format(
                            max_attempts
                        ))

                RSAInterface.rsa.DPX_WaitForDataReady(c_int(100), byref(ready))

        RSAInterface.rsa.DPX_GetFrameBuffer(byref(fb))
        RSAInterface.rsa.DPX_FinishFrameBuffer()
        RSAInterface.rsa.DEVICE_Stop()
        return fb

    # Check for errors from the RSA
    def error_checker(self, status):
        if ReturnStatus(status) != ReturnStatus.noError:
            raise RSAError(ReturnStatus(status.names))

    # Helper method to disconnect the RSA
    def disconenct_rsa(self):
        RSAInterface.rsa.DEVICE_Disconnect()
