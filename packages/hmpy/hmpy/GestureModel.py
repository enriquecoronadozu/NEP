#!/usr/bin/env python

# Luis Enrique Coronado Zuniga

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.


# Requiered libraries

from numpy import* #Note: to avoid errors we need to call first numpy and then scipy import linalg
from scipy import linalg
import matplotlib.pyplot as plt
import os

from hmpy import*


#TODO: createGMM_model_f and createGMM_model better way?


class GestureModel():
    """ This class is used to save the parameters of a model
        :param name_model: name of the model
        :param path_to_load: In which folder the data is loaded?
        :param path_to_save: In which folder the model will be saved?
        :param num_samples: number of samples by model

          
        The .txt files used to create the models must be named as: *mod(i).txt*
          
        Where :math:`i=\{1,..,num\_samples\}`.
    """
    def __init__(self,name_model,path_to_load,path_to_save):
        # Init the the type of the parameters
        print
        print "*************  Model = ", name_model, "***********"
        print
        # Get name of the gesture model
        self.name_model = name_model
          
        # This gesture can have diferent components, a dictionary is used to save the information of each component
        self.component = {}
        self.Weights = {}
        self.files = []

        # Diferent path where is loaded and saved
        self.path_data =  path_to_load  + self.name_model
        self.path_models =  path_to_save  + self.name_model
        print path_to_load + name_model


        import glob
        txts = glob.glob(self.path_data + "/*.txt")
        num_samples = len(txts)

        print ("Number of samples: " + str(num_samples))

        # Open the files
        for k in range(1,num_samples+1):
            self.files.append(self.path_data + '/mod'+ str(k) + '.txt')
               
        #print self.files 

        self.gesture_model = newModel()
        #Read the  files	
        self.gesture_model.ReadFiles(self.files)


        if not os.path.exists(self.path_models):
            os.makedirs(self.path_models)


    def buildDNN_model(self, dtype = "3IMU_acc", feature_extraction = True, value = "100"):
        """Build a new Gesture model from a list of .txt files
               :param dtype: type of data. "3IMU_acc" -> IMU 3D data
               :param feature_extraction: Bool variable
               :param value: number of samples for each training set
        """
        print "Building a Gesture model"           
        if dtype == "3IMU_acc":
            print "Type Model = DNN , Type data= 3IMU_acc"
            if feature_extraction:
                self.gesture_model.extract3D_acceleration_features()
                self.createDNN_model_f(value)
            else:
                self.gesture_model.IMU2matrix()
                self.createDNN_model(value)


               
    def buildGMM_model(self, dtype = "3IMU_acc", feature_extraction = True, th_cluster = 0.68):
        """Build a new Gesture model from a list of .txt files
            :param mtype: type of model "GMM" or "DNN"
            :param dtype: type of data. "3IMU_acc" -> IMU 3D data
            :param feature_extraction: Bool variable
            :param th: threashold (only GMM)
            :param value: number of samples for each training set (for DNN)
        """
          
        print "Building a Gesture model"
        # Create a GMM model
        self.gesture_model.th_cluster = th_cluster
        if dtype == "3IMU_acc":
            print "Type Model = GMM , Type data= 3IMU_acc"
            if feature_extraction:
                self.gesture_model.extract3D_acceleration_features()
                self.createGMM_model_f()
            else:
                self.gesture_model.IMU2matrix()
                self.createGMM_model()



     # ------------------------------------------------- DNN ---------------------------------------------------------------


    def list2KerasIMU(self, value):
        """Convert a list of datafiles from IMU 3d informtion to a matrix for be used in Keras
        """
        n_data = self.gesture_model.n_data
          
        x = ones((1,n_data))*self.gesture_model.datafiles[0][0].transpose()
        y = ones((1,n_data))*self.gesture_model.datafiles[0][1].transpose()
        z = ones((1,n_data))*self.gesture_model.datafiles[0][2].transpose()

        if(value <= n_data):
            x = x[:,0:value-1]
            y = y[:,0:value-1]
            z = z[:,0:value-1]

        else:              
            additional = value - n_data -1
            x = concatenate((x,zeros((1,additional))), axis=1)
            y = concatenate((y,zeros((1,additional))), axis=1)
            z = concatenate((z,zeros((1,additional))), axis=1)

        data = concatenate((x,y), axis=1)
        data = concatenate((data, z), axis=1)
        cdata = data

        i = 1


        while (i < self.gesture_model.nfiles):
            x = ones((1,n_data))*self.gesture_model.datafiles[i][0].transpose()
            y = ones((1,n_data))*self.gesture_model.datafiles[i][1].transpose()
            z = ones((1,n_data))*self.gesture_model.datafiles[i][2].transpose()
            if(value <= n_data):
                x = x[:,0:value-1]
                y = y[:,0:value-1]
                z = z[:,0:value-1]
            else:
                x = concatenate((x,zeros((1,additional))), axis=1)
                y = concatenate((y,zeros((1,additional))), axis=1)
                z = concatenate((z,zeros((1,additional))), axis=1)

            data = concatenate((x,y), axis=1)
            data = concatenate((data, z), axis=1)
            cdata = concatenate((cdata, data), axis=0)
            i = i + 1
   
        return cdata

    def createDNN_model(self, value):
        self.dnn_dataset = self.list2KerasIMU(value)
        print "dataset obtained"


    def concatenate_in_vector(data):
        print data

    # ------------------------------------------------- GMM ---------------------------------------------------------------
    def createGMM_model(self,):
        gmm_model = self.gesture_model

        # 1) Use Knn to obtain the number of cluster
        # TO IMPROVE
        gmm_model.ObtainNumberOfCluster(dtype = "3IMU_acc", feature_extraction = False, save = True, path = self.path_models)
          
        acc = gmm_model.acc
        K_acc = gmm_model.K_acc

        # 2) define the number of points to be used in GMR
        #    (current settings allow for CONSTANT SPACING only)
        numPoints = amax(acc[0,:]);
        scaling_factor = 10/10;
        numGMRPoints = math.ceil(numPoints*scaling_factor);

        # 3) perform Gaussian Mixture Modelling and Regression to retrieve the
        #   expected curve and associated covariance matrices for each feature

        acc_points, acc_sigma = gmm_model.GetExpected(acc,K_acc,numGMRPoints)


        #Save the model
        try:
            savetxt(self.path_models+ '/MuIMUacc.txt', acc_points,fmt='%.12f')
            savetxt(self.path_models+ '/SigmaIMUacc.txt', acc_sigma,fmt='%.12f')
        except:
            print "Error, folder not found"
               
    def createGMM_model_f(self):

        gmm_model = self.gesture_model


        # 1) Use Knn to obtain the number of cluster
        # TO IMPROVE
        gmm_model.ObtainNumberOfCluster(dtype = "3IMU_acc", feature_extraction = True, save = True, path = self.path_models)
          
        gravity = gmm_model.gravity
        K_gravity = gmm_model.K_gravity
        body = gmm_model.body
        K_body = gmm_model.K_body

        # 2) define the number of points to be used in GMR
        #    (current settings allow for CONSTANT SPACING only)
        numPoints = amax(gravity[0,:]);
        scaling_factor = 10/10;
        numGMRPoints = math.ceil(numPoints*scaling_factor);

        # 3) perform Gaussian Mixture Modelling and Regression to retrieve the
        #   expected curve and associated covariance matrices for each feature

        gr_points, gr_sigma = gmm_model.GetExpected(gravity,K_gravity,numGMRPoints)
        b_points, b_sigma = gmm_model.GetExpected(body,K_body,numGMRPoints)


        #Save the model
        try:
            savetxt(self.path_models+ '/MuGravity.txt', gr_points,fmt='%.12f')
            savetxt(self.path_models+ '/SigmaGravity.txt', gr_sigma,fmt='%.12f')
            savetxt(self.path_models+ '/MuBody.txt', b_points,fmt='%.12f')
            savetxt(self.path_models+ '/SigmaBody.txt', b_sigma,fmt='%.12f')
        except:
            print "Error, folder not found"
     

if __name__ == "__main__":
    import doctest
    doctest.testmod()


