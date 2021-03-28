__author__ = "Addison Raak, Michael Antkiewicz, Ka'ulu Ng, Nicholas Baldwin"
__copyright__ = "Copyright 2017-19, Tektronix Inc."
__credits__ = ["Addison Raak", "Michael Antkiewicz", "Ka'ulu Ng", "Nicholas Baldwin"]

import os
import numpy as np
import DLL_loader
from rsa_config import RSAConfig
from RSA_API import *
from ctypes import *


class RSAInterface:
    # Creates an RSA object to access its functionality
    __rsa = None

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
        if RSAInterface.__rsa is None:
            return None
        else:
            return instance

    def __init__(self):
        # Only is called is the RSA is not already defined
        if RSAInterface.__rsa is None:
            # change the directory so the dll file will work
            current_dir = os.getcwd()
            RSAInterface.__rsa = RSAInterface.__try_init_RSA_Interface()
            os.chdir(current_dir)

    # Loads the RSA_API.dll file if it exists
    # @staticmethod
    # def __try_init_RSA_interface():
    #     if DLL_loader.change_cwd(DLL_loader.RSA_DLL_PATH_x64):
    #         rsa = cdll.LoadLibrary(DLL_loader.RSA_DLL_FILENAME)
    #         if rsa is not None:
    #             return rsa
    #     elif DLL_loader.change_cwd(DLL_loader.RSA_DLL_PATH_x84):
    #         rsa = cdll.LoadLibrary(DLL_loader.RSA_DLL_FILENAME)
    #         if rsa is not None:
    #             return rsa
    #     return None

    @staticmethod
    def __try_init_RSA_Interface():
        if DLL_loader.change_cwd(DLL_loader.FULL_DLL_PATH_x64):
            rsa = RSAInterface.__try_load_dll()
            if rsa is not None:
                return rsa
        # If x64 version failed, try loading the x86 version.
        if DLL_loader.change_cwd(DLL_loader.FULL_DLL_PATH_x84):
            rsa = RSAInterface.__try_load_dll()
            if rsa is not None:
                return rsa
        return None

    @staticmethod
    def __try_load_dll():
        try:
            print(os.getcwd())
            print(DLL_loader.RSA_DLL_FILENAME)
            print(DLL_loader.FULL_DLL_PATH_x64)
            rsa = cdll.LoadLibrary("C:/Users/Mikey/Desktop/School/Capstone/tek17/RSA_API/lib/x64/RSA_API.dll")
            return rsa
        except OSError as e:
            print(e)
            return None

    # Check for errors
    def err_check(self, rs):
        if ReturnStatus(rs) != ReturnStatus.noError:
            raise RSAError(ReturnStatus(rs).name)

    # Connects to the RSA
    # ################## RSA PDF GUIDE PAGE 6 ################## #
    @staticmethod
    def search_connect(self):
        # throws Not Connected error if the RSA is not initialized
        if RSAInterface.__rsa is None:
            raise RSAError(ReturnStatus.errorNotConnected.name)

        # numFound used later to hold number of available RSA's that connected
        # page 6 of pdf
        numFound = c_int(0)
        # intArray = c_int * DEVSRCH_MAX_NUM_DEVICES
        intArray = c_int * 10
        deviceIDs = intArray()
        deviceSerial = create_string_buffer(DEVSRCH_SERIAL_MAX_STRLEN)
        deviceType = create_string_buffer(DEVSRCH_TYPE_MAX_STRLEN)
        apiVersion = create_string_buffer(DEVINFO_MAX_STRLEN)

        RSAInterface.__rsa.DEVICE_GetAPIVersion(apiVersion)
        print('API Version {}'.format(apiVersion.value.decode()))

        # self.err_check(RSAInterface.__rsa.DEVICE_Search(byref(numFound), deviceIDs,
        #                                                 deviceSerial, deviceType))

        RSAInterface.__rsa.DEVICE_Search(byref(numFound), deviceIDs, deviceSerial, deviceType)
        # Checks to see how many RSA's are connected. Currently only supports 1.
        if numFound.value < 1:
            print("No RSA found.")
            raise RSAError(ReturnStatus.errorNotConnected.name)
        elif numFound.value == 1:
            print("One Device Found.")
            print("Device Type: {}".format(deviceType.value))
            print("Device Serial Number: {}".format(deviceSerial.value))
            RSAInterface.__rsa.DEVICE_Connect(deviceIDs[0])
        else:
            print("More than one device found. Expected one.")

        RSAInterface.__rsa.CONFIG_Preset()
        ''' THIS IS FROM THE RSA EXAMPLE CODE ON GITHUB '''
        ''' RSA_example.py def search_connect():
                print('API Version {}'.format(DEVICE_GetAPIVersion_py()))
                try:
                    numDevicesFound, deviceIDs, deviceSerial, deviceType = DEVICE_Search_py()
                except RSAError:
                    print(RSAError)
                print('Number of devices: {}'.format(numDevicesFound))
                if numDevicesFound > 0:
                    print('Device serial numbers: {}'.format(deviceSerial[0].decode()))
                    print('Device type: {}'.format(deviceType[0].decode()))
                    DEVICE_Connect_py(deviceIDs[0])
                else:
                    print('No devices found, exiting script.')
                    exit()
                CONFIG_Preset_py()
        '''

    # set the spectrum values to default to avoid communication errors
    # page 16 of RSA_API_Guide pdf
    def config_spectrum(self, rsaCfg):
        enable = c_bool(True)
        RSAInterface.__rsa.SPECTRUM_SetEnable(enable)
        RSAInterface.__rsa.CONFIG_SetCenterFreq(rsaCfg.cf)
        RSAInterface.__rsa.CONFIG_SetReferenceLevel(rsaCfg.refLevel)
        RSAInterface.__rsa.SPECTRUM_SetDefault()
        specSet = Spectrum_Settings()
        RSAInterface.__rsa.SPECTRUM_GetSettings(byref(specSet))
        specSet.window = SpectrumWindows.SpectrumWindow_Kaiser
        specSet.verticalUnit = SpectrumVerticalUnits.SpectrumVerticalUnit_dBm
        specSet.span = rsaCfg.span
        specSet.rbw = rsaCfg.rbw
        RSAInterface.__rsa.SPECTRUM_SetSettings(specSet)
        RSAInterface.__rsa.SPECTRUM_GetSettings(byref(specSet))
        return specSet

    def acquire_spectrum(self, specSet):
        ready = c_bool(False)
        traceArray = c_float * specSet.traceLength
        traceData = traceArray()
        outTracePoints = c_int(0)
        traceSelector = SpectrumTraces.SpectrumTrace1

        RSAInterface.__rsa.DEVICE_Run()
        RSAInterface.__rsa.SPECTRUM_AcquireTrace()
        while not ready.value:
            RSAInterface.__rsa.SPECTRUM_WaitForDataReady(c_int(100), byref(ready))
        RSAInterface.__rsa.SPECTRUM_GetTrace(traceSelector, specSet.traceLength, byref(traceData),
                                             byref(outTracePoints))
        RSAInterface.__rsa.DEVICE_Stop()
        return np.array(traceData)

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
        RSAInterface.__rsa.CONFIG_SetCenterFreq(rsaCfg.cf)
        RSAInterface.__rsa.CONFIG_SetReferenceLevel(rsaCfg.refLevel)

        RSAInterface.__rsa.DPX_SetEnable(c_bool(True))
        RSAInterface.__rsa.DPX_SetParameters(rsaCfg.span, rsaCfg.rbw, rsaCfg.bitmapWidth, rsaCfg.tracePtsPerPixel,
                                             rsaCfg.yUnit, rsaCfg.yTop, rsaCfg.yBottom, rsaCfg.infinitePersistence,
                                             rsaCfg.persistenceTimeSec,
                                             rsaCfg.showOnlyTrigFrame)  # rsaCfg.persistenceTimeSec, rsaCfg.showOnlyTrigFrame)

        RSAInterface.__rsa.DPX_SetSogramParameters(c_double(1e-3), c_double(1e-3),
                                                   rsaCfg.refLevel,
                                                   c_double(rsaCfg.refLevel.value - rsaCfg.refLevelOffset.value))
        RSAInterface.__rsa.DPX_Configure(c_bool(True), c_bool(True))

        RSAInterface.__rsa.DPX_SetSpectrumTraceType(c_int32(0), c_int(2))
        RSAInterface.__rsa.DPX_SetSpectrumTraceType(c_int32(1), c_int(4))
        RSAInterface.__rsa.DPX_SetSpectrumTraceType(c_int32(2), c_int(0))

        RSAInterface.__rsa.DPX_GetSettings(byref(dpxSet))
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
            RSAInterface.__rsa.TRIG_SetTriggerMode(TriggerMode.freeRun)
        else:
            # set rsa to triggered mode (1), as opposed to free mode (0)
            RSAInterface.__rsa.TRIG_SetTriggerMode(TriggerMode.triggered)

            # set rsa to power trigger (1), as opposed to external source trigger (0)
            RSAInterface.__rsa.TRIG_SetTriggerSource(TriggerSource.TriggerSourceIFPowerLevel)

            # set power level and position percent
            RSAInterface.__rsa.TRIG_SetIFPowerTriggerLevel(c_double(trigger.power_level))
            RSAInterface.__rsa.TRIG_SetTriggerPositionPercent(c_int(int(trigger.position_percent)))

            # either transition high to low or low to high
            RSAInterface.__rsa.TRIG_SetTriggerTransition(TriggerTransition.TriggerTransitionEither)

        # track the number of attempts, raise RuntimeError exception if
        # the attempts exceeds the max
        attempts = 0
        while not frameAvailable.value:
            RSAInterface.__rsa.DPX_IsFrameBufferAvailable(byref(frameAvailable))
            while not ready.value:
                attempts += 1
                if trigger is None and attempts > max_attempts:
                    raise RSAError(
                        "Maximum attempts exceeded: failed to acquire frame {} times".format(
                            max_attempts
                        ))

                RSAInterface.__rsa.DPX_WaitForDataReady(c_int(100), byref(ready))

        RSAInterface.__rsa.DPX_GetFrameBuffer(byref(fb))
        RSAInterface.__rsa.DPX_FinishFrameBuffer()
        RSAInterface.__rsa.DEVICE_Stop()
        return fb

    def extract_dpx_spectrum(selfself, fb):
        # When converting a ctypes pointer to a numpy array, we need to
        # explicitly specify its length to dereference it correctly
        dpxBitmap = np.array(fb.spectrumBitmap[:fb.spectrumBitmapSize])
        dpxBitmap = dpxBitmap.reshape((fb.spectrumBitmapHeight,
                                       fb.spectrumBitmapWidth))

        # Grab trace data and convert from W to dBm
        # http://www.rapidtables.com/convert/power/Watt_to_dBm.htm
        # Note: fb.spectrumTraces is a pointer to a pointer, so we need to
        # go through an additional dereferencing step
        traces = []
        for i in range(3):
            traces.append(10 * np.log10(1000 * np.array(
                fb.spectrumTraces[i][:fb.spectrumTraceLength])) + 30)
        # specTrace2 = 10 * np.log10(1000*np.array(
        #     fb.spectrumTraces[1][:fb.spectrumTraceLength])) + 30
        # specTrace3 = 10 * np.log10(1000*np.array(
        #     fb.spectrumTraces[2][:fb.spectrumTraceLength])) + 30

        # return dpxBitmap, specTrace1, specTrace2, specTrace3
        return dpxBitmap, traces

    def extract_dpxogram(self, fb):
        # When converting a ctypes pointer to a numpy array, we need to
        # explicitly specify its length to dereference it correctly
        dpxogram = np.array(fb.sogramBitmap[:fb.sogramBitmapSize])
        dpxogram = dpxogram.reshape((fb.sogramBitmapHeight,
                                     fb.sogramBitmapWidth))
        dpxogram = dpxogram[:fb.sogramBitmapNumValidLines, :]

        return dpxogram

    # Helper method to disconnect the RSA
    def disconenct_rsa(self):
        RSAInterface.__rsa.DEVICE_Disconnect()