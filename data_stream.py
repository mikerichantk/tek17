import random
import sys

import numpy as np

from RSA_API import RSAError
from rsa_config import RSAConfig
from data_types import create_data

from threading import Lock

from rsa_interface import RSAInterface


# This class is built on top of the RSA interface
# and can be used to quickly pull data off of an RSA in DPXGraphData format
# this class is in charge of connecting and disconnecting from an RSA
class GraphDataStream:
    # rsa to stream data out of
    rsa = None

    # rsa lock
    rsa_lock = Lock()

    # current configuration of the rsa
    rsa_config = RSAConfig()

    # current trigger for the rsa
    trigger = None

    # hold previously returns DPXGraphData objects
    buffer_size = 10
    dpx_data_buffer = []

    # Changes the configuration of the RSA
    #
    # Parameters:
    #   rsa_config <RSAConfig>: The configuration to update this stream's RSA with
    def set_rsa_config(self, rsa_config):
        if rsa_config == None:
            raise ValueError("rsa_config cannot be None")

        self.rsa_config = rsa_config

        if self.rsa != None:
            self.rsa_lock.acquire()
            self.rsa.config_DPX(self.rsa_config)
            self.rsa_lock.release()

    # Sets a trigger
    # !!! Currently does not work !!!
    def set_trigger(self, trigger):
        self.trigger = trigger
        new_config = self.rsa_config

        # show only trig frame iff we are setting a trigger
        new_config.showOnlyTrigFrame = trigger is not None

        self.set_rsa_config(new_config)

    # Collects dpx data
    # Returns:
    #   A DPXGraphData object from the RSA
    def get_data(self):
        if not self.is_open():
            raise ValueError("Cannot get DPX data from a closed stream")

        try:
            self.rsa_lock.acquire()
            if self.rsa is None:
                self.rsa_lock.release()
                raise ValueError("Cannot get DPX data from a closed stream")

            fb = self.__rsa.acquire_dpx_frame(self.trigger)
            self.rsa_lock.release()
        except RSAError as err:
            self.rsa_lock.release()
            self.close()
            raise RSAError("Could not acquire frame, closing stream")

        bitmap, dpx_traces = self.rsa.extract_dpx_spectrum(fb)

        data = create_data(bitmap, self.rsa_config)

        self.__add_to_buffer(data)

        return data

    # Creates an iterator which continually pulls data from an RSA
    # and yields the data. The iterator terminates when this stream closes
    def get_dpx_data_while_open(self):
        while self.is_open():
            try:
                yield self.get_data()
            except (RSAError, ValueError) as err:
                print(err)
                if not self.is_open():
                    return

    # Adds a DPX data to the buffer
    # Parameters:
    #   dpx_data <DPXGraphData>: the data to buffer
    def __add_to_buffer(self, data):
        # push the new data into the buffer
        self.data_buffer.insert(0, data)

        # get rid of any data exceeding the buffer size
        self.data_buffer = self.data_buffer[:self.buffer_size]

    # Parameters:
    #   count <int>: optionally specifies the number of data to return
    #               if provided, as list of data is returned, if not
    #               a single data is returned
    # Returns:
    #   the DPXGraphData that was most recently returned by get_dpx_data
    def get_previous_dpx_data(self, count=None):
        if count == None:
            return self.data_buffer[0]

        return self.data_buffer[0:count]

    # Opens this stream
    def open(self):
        if self.rsa is not None:
            raise ValueError('Stream is already open -- cannot open')

        self.__enter__()

    # Closes this stream
    def close(self):
        if self.rsa is None:
            raise ValueError('Stream is not open -- cannot close')

        self.__exit__(None, None, None)

    # Returns:
    #   a boolean, whether the stream is open
    def is_open(self):
        return self.rsa is not None

    # The enter function to open the stream
    def __enter__(self):
        print("Enter stream")
        self.rsa = RSAInterface.get_instance()

        try:
            self.__rsa.search_connect()
        except (RSAError, ValueError) as e:
            print(e)
            self.__rsa = None
            print(e)
            raise e

        self.__rsa.config_DPX(self.rsa_config)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exit stream")

        self.rsa_lock.acquire()
        self.rsa.disconnect_rsa()
        self.rsa_lock.release()

        self.rsa = None

        # raise the exception to the next level
        return False


# Create a stream
# Parameters:
#   rsa_config <RSAConfig>: optionally specify the configuration to initially use this stream
# Returns:
#   a new DPX data stream
def create_data_stream(rsa_config=RSAConfig()):
    stream = GraphDataStream()
    stream.set_rsa_config(rsa_config)

    return stream


#######################################################
############## Mock Version ##########################
#######################################################

class MockGraphDataStream:
    # rsa to stream data out of
    __is_open = False

    # current configuration of the rsa
    rsa_config = RSAConfig()

    buffer_size = 10
    data_buffer = []

    def set_rsa_config(self, rsa_config):
        if rsa_config == None:
            raise ValueError("rsa_config cannot be None")

        self.rsa_config = rsa_config

    # get a mock data with random output
    def get_data(self):
        bitmap = np.ndarray(shape=(201, 801))

        for i in range(bitmap.shape[0]):
            if random.random() < .2:
                for j in range(bitmap.shape[1]):
                    bitmap[i][j] = 4

        data = create_data(bitmap, self.rsa_config)

        self.add_to_buffer(data)

        return data

    def get_data_while_open(self):
        while self.is_open():
            yield self.get_data()

    def add_to_buffer(self, dpx_data):
        # push the new data into the buffer
        self.data_buffer.insert(0, dpx_data)

        # get rid of any data exceeding the buffer size
        self.data_buffer = self.data_buffer[:self.buffer_size]

    # return the data that was most recently returned by get_data
    # if a count is supplied, a list of count datas (up to the buffer size) are returned
    # if no count is supplied, a single dpx data is returned
    def get_previous_data(self, count=None):
        if count == None:
            return self.data_buffer[0]

        return self.data_buffer[0:count]

    def open(self):
        if self.is_open():
            raise ValueError('Mock Stream is already open -- cannot open')

        self.__enter__()

    def close(self):
        if not self.is_open():
            raise ValueError('Mock Stream is not open -- cannot close')

        self.__exit__(None, None, None)

    def is_open(self):
        return self.__is_open

    # The enter function to open the stream
    def __enter__(self):
        print("Enter mock stream")
        self.__is_open = True

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exit mock stream")
        self.__is_open = False

        # raise the exception to the next level
        return False


def create_mock_data_stream(rsa_config=RSAConfig()):
    stream = MockGraphDataStream()
    stream.set_rsa_config(rsa_config)

    return stream
