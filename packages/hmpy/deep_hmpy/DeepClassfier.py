#!/usr/bin/env python

# Luis Enrique Coronado Zuniga
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

"""@See preprocessed data
"""

from numpy import*
from numpy.linalg import*
from scipy import interpolate
from scipy.signal import filtfilt, lfilter
from scipy.signal import medfilt
from scipy.signal import filter_design as ifd
from scipy.stats import multivariate_normal
import scipy.spatial
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from numpy import*
import time


class DeepClassifier:
    """Class used to classify a gesture using a Deep Learning model
        :param path_model: path the of .json file of the Deep Learning model
        :param number_inputs: number of inputs of the neural network
        :param number_outputs: number of outputs of the neural network
        :param dtype: type of data. "3IMU_acc" for IMU 3D data
        :param feature_extraction: bool variable, if true then obtain body and gravity components.
    
    """

    def __init__(self, path_model, number_inputs, number_outputs, dtype = "3IMU_acc", feature_extraction = True):


        self.number_inputs = number_inputs
        self.number_outputs = number_outputs
        self.dtype = dtype
        self.feature_extraction = feature_extraction

        if("3IMU_acc"):
            self.window_size = int(number_inputs/3) -1
            self.window = zeros((self.window_size,3))

        # load json model
        json_file = open(path_model, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.deep_model = model_from_json(loaded_model_json)
        self.deep_model.load_weights("model.h5")
        self.dataIndex = 0


    def online_validation(self,x,y,z):
        """This function is used for online classification from a sample of sensory data
            :param x: x value
            :param y: y value
            :param z: z value
        """
        one_sample = array([x,y,z])
        import time
        t0 = time.clock()
        self.window,self.dataIndex = self.createWindow(one_sample, self.window, self.window_size,self.dataIndex)

        # Start the recognition when the are enough data in the window
        if (self.dataIndex >= self.window_size):
            if self.dtype == "3IMU_acc":
                if self.feature_extraction == True:
                    # TODO
                    print "no jet"
                else:
                    acc = self.analyzeActualWindow(self.window,self.window_size);
                    windows_in_vector = self.window2KerasIMU(self.window)
                    #print windows_in_vector.size
                    poss = self.gesture_prediction(windows_in_vector)
            return poss 
        else:
            return 0

    def validate_from_file(self,sfile,delim = ' '):
        """
        This function returns a probability vector given a .txt file with data information
        :param sfile: path and name of the file to be validated
        :param delim: delimiter of the data in the txt file
        :return class_recognized: vector of binary values
        """
        numWritten = 0
        data = genfromtxt(sfile, delimiter=delim)
        numSamples,m = data.shape

        possibilities = zeros((numSamples,self.number_outputs))
        
        for i in range (numSamples):
            one_sample = data[i]

            t0 = time.clock()

            # Create a windows from the samples
            self.window,numWritten = self.createWindow(one_sample, self.window, self.window_size, numWritten)

            # Start the recognition when the are enough data in the window
            if (numWritten >= self.window_size):
                if self.dtype == "3IMU_acc":
                    if self.feature_extraction == True:
                        # TODO
                        print "no jet"
                        # Compute the acceleration components of the current window of samples
                        #gravity,body = self.analyzeActualWindow_f(self.window,self.window_size,delay = 64);
                        #possibilities_vector[i,0] = self.compareModel_f(self.model,gravity, body,self.window_size);
                    else:
                        acc = self.analyzeActualWindow(self.window,self.window_size);
                        windows_in_vector = self.window2KerasIMU(self.window)
                        print ("SIZE windows: " + str(windows_in_vector.size))
                        poss = self.gesture_prediction(windows_in_vector)

                        j = 0 
                        for p in poss:
                            possibilities[i,j] = p
                            j = j + 1
                    

                tm = time.clock() - t0
                #print "comparar =", tm

        return possibilities

    def window2KerasIMU(self, data):
          """Convert a 3-axis IMU information information to a vector of inputs for Keras
          """
          n_data = self.window_size
          x = ones((1,n_data))*data[:,0].transpose()
          y = ones((1,n_data))*data[:,1].transpose()
          z = ones((1,n_data))*data[:,2].transpose()

          vector = concatenate((x,y), axis=1)
          vector = concatenate((vector, z), axis=1)
          return vector

    def gesture_prediction(self,windows_in_vector):
        """Predict a gesture from a Deap Learning Model"""
        predictions = self.deep_model.predict(windows_in_vector)
        return predictions[0]


    def createWindow(self,one_sample, window, window_size, numWritten):
        """
        This function creates a windows used to compare with the models

        :param one_sample: vector of sensory data in time t
        :param windows: old windows
        :param windows_size: size that can have the windows
        :param numWritten: count used to itearte betweem samples
        """
        #Fill window if numWritten < window_size
        if numWritten < window_size:
            for j in range(3):
                window[numWritten,j] = one_sample[j];
            numWritten = numWritten + 1
        #shift window and update
        else:
            for i in range(window_size-1):
                for j in range(3):
                        window[i,j] = window[i+1,j];
            for j in range(3):
                window[window_size - 1,j] = one_sample[j];
            numWritten = numWritten + 1
        return window,numWritten


        #The same that in Classfier class
    def analyzeActualWindow(self,window,numSamples,delay = 0):
        """ AnalyzeActualWindow separates the gravity and body acceleration features
            contained in the window of real-time acceleration data, by first reducing
            the noise on the raw data with a median filter and then discriminating
            between the features with a low-pass IIR filter.

            :param window: windows to be processed and analalized
            :param numSamples: is equal to the windows size
            :param delay: delay of samples
            """

        self.delay = delay
        #REDUCE THE NOISE ON THE SIGNALS BY MEDIAN FILTERING
        n = 3  #order of the median filter
        x_axis = medfilt(window[:,0],n)
        y_axis = medfilt(window[:,1],n)
        z_axis = medfilt(window[:,2],n)


        acc = zeros((numSamples-delay,3));

        i=delay
        while(i < numSamples):
            acc[i-delay,0] = x_axis[i];
            acc[i-delay,1] = y_axis[i];
            acc[i-delay,2] = z_axis[i];
            i = i + 1
            
        return acc


if __name__ == "__main__":
    import doctest
    doctest.testmod()
