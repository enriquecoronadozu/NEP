#!/usr/bin/env python

# Luis Enrique Coronado Zuniga
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

"""@See preprocessed data
"""

from numpy import arange, sin, pi
from numpy import*
from numpy.linalg import*
import os
from dtw import dtw



class Aligment:
    """Class used to aligment of 1D sequential data
        Parameters
        ----------
        
        path:str
            path of the folder that contain the gesture
        name:str
            name of the gesture
        file_id:str
            name of the training data files
        num_samples:int
            number of training examples
        axis:int
            dimention for the aligment
    """
    #As numpy

    def __init__(self, path, name_model, file_id, num_samples, axis = 0):
        self.path = path
        self.name_model = name_model
        self.num_samples = num_samples
        self.file_id = file_id
        self.axis = axis
        self.limit_i = 0
        self.limit_r = 0
        
        # File's paths
        self.files = []
        # List to save the training data
        self.lista = []
        # Offset betweem the training data
        self.offsets = []
        
        for k in range(1,num_samples+1):
            #self.files.append(path + '/' + name_model +'/'+ file_id + '('+ str(k) + ').txt')
            self.files.append(path + '/' + name_model +'/'+ file_id + str(k) + '.txt')
        self.n = 0
        for name in self.files:
            self.data = genfromtxt(name, delimiter=',')
            self.lista.append(self.data)
            self.offsets.append(0)
            self.n = self.n + 1



    def dtw_aligment(self):
        """Aligment of data using DTW algorithm
        :return offsets: list of offset between the first sample an the others
        """

        x = self.lista[0][0:,self.axis].reshape(-1, 1)
        for k in range (1,self.n):
            y = self.lista[k][0:,self.axis].reshape(-1, 1)
            dist, cost, acc, path = dtw(x, y, dist=lambda x, y: norm(x - y, ord=1))
            map_x = path[0]
            map_y = path[1]
            counts = bincount(path[0])
            self.offsets[k] = int(mean(map_x - map_y))

        return self.offsets

    def save(self,limit_i, limit_r,offsets,new_path):
        """Save the aligned data

        param limit_i: left limit
        param limit_r: right limit
        param offsets: offsets between the training set
        return new_path: segmented data
        """
        lista = self.lista;
        directory = new_path + "/" + self.name_model
        self.limit_i = limit_i
        self.limit_r =limit_r

        if not os.path.exists(directory):
            os.makedirs(directory)
                              
        new_data = []
        filename = directory + "/mod"
        print "Saving data ... \n"
        num = len(lista)
        for i in range(num):
            samples = int(self.limit_r) - int(self.limit_i)
            offset = int(offsets[i])
            init = self.limit_i - offset
            n,m = lista[i].shape
                
            if self.limit_i < offset:
                print "Error in saving data, sample", i, "increase left limit"
            elif n + offset <  self.limit_r:
                print "Error in saving data, sample", i, "decrease rigth limit"
            else:
                savetxt(filename + "(" + str(i+1) +').txt', lista[i][init:init+samples,:] , delimiter=' ', fmt='%f')
                new_data.append(lista[i][init:init+samples,:])
                print "Saving data", i, "OK"
                
        return new_data


    def plotData(self):
        import matplotlib.pyplot as plt
        """Plot the original data"""
        lista = self.lista;
        num = len(lista)
        fig = plt.figure()

        for i in range(num):
            n,m = lista[i].shape
            x = arange(0,n,1)
            axes = fig.add_subplot(311)
            axes.plot(x, lista[i].transpose()[0])
            axes.grid(True)
            axes = fig.add_subplot(312)
            axes.plot(x, lista[i].transpose()[1])
            axes.grid(True)
            axes = fig.add_subplot(313)
            axes.plot(x, lista[i].transpose()[2])
            axes.grid(True)

    def plotDataAligned(self):
        import matplotlib.pyplot as plt
        
        """Plot the aligned data"""
        num = len(self.lista)
        fig = plt.figure()
        
        for i in range(num):

            x = self.lista[i][0:,0].reshape(-1, 1)
            y = self.lista[i][0:,1].reshape(-1, 1)
            z = self.lista[i][0:,2].reshape(-1, 1)

            n,m = self.lista[i].shape
            
            if (self.offsets[i] > 0):
                t = arange(self.offsets[i],n+self.offsets[i],1)
                axes = fig.add_subplot(311)
                axes.axvline(x=self.limit_i, linewidth=2, color = 'b')
                axes.axvline(x=self.limit_r, linewidth=2, color = 'k')
                axes.plot(t, x)
                axes.grid(True)
                axes = fig.add_subplot(312)
                axes.axvline(x=self.limit_i, linewidth=2, color = 'b')
                axes.axvline(x=self.limit_r, linewidth=2, color = 'k')
                axes.plot(t, y)
                axes.grid(True)
                axes = fig.add_subplot(313)
                axes.axvline(x=self.limit_i, linewidth=2, color = 'b')
                axes.axvline(x=self.limit_r, linewidth=2, color = 'k')
                axes.plot(t, z)
                axes.grid(True)
            else:
                axes = fig.add_subplot(311)
                axes.plot(x[-self.offsets[i]:])
                axes.axvline(x=self.limit_i, linewidth=2, color = 'b')
                axes.axvline(x=self.limit_r, linewidth=2, color = 'k')
                axes.grid(True)
                axes = fig.add_subplot(312)
                axes.plot(y[-self.offsets[i]:])
                axes.axvline(x=self.limit_i, linewidth=2, color = 'b')
                axes.axvline(x=self.limit_r, linewidth=2, color = 'k')
                axes.grid(True)
                axes = fig.add_subplot(313)
                axes.plot(z[-self.offsets[i]:])
                axes.axvline(x=self.limit_i, linewidth=2, color = 'b')
                axes.axvline(x=self.limit_r, linewidth=2, color = 'k')
                axes.grid(True)


 
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()              
                    
