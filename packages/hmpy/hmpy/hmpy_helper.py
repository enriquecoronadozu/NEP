#!/usr/bin/env python

# Luis Enrique Coronado Zuniga
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

"""@See preprocessed 1 dimensional data
"""
import hmpy
from numpy import*

class hmpy_helper():
    
    def __init__(self, models_description, path_train = "/data_examples/acceleration_aligned", path_save = "/data_examples/Gaussian_Models/", data_type = "3IMU_acc", features = False):
         self.path_to_train, self.path_to_save =  self.get_paths(path_train, path_save)   
         self.models_description = models_description
         self.data_type = data_type
         self.features = features
         self.list_models = []
    
    def get_paths(self, path_train, path_save):
        """
        This function can be used to get the complete path of the files used to train and save the gesture models
        :param path_train: relative path were are the files to train the models
        :param path_save: relative path were we want to save the GMM models
        """
        # Get the current path
        import os
        dir_path = os.getcwd()
        # print "Current path in ", dir_path

        # Define the path to save the GMM models
        path_to_save = dir_path + path_save 

        # Define the path of the gesture folders with the training examples
        path_to_train = dir_path + path_train
        
        return path_to_train, path_to_save

    def generate_models(self, train = True):
        """
        This function can be used to help to generate gesture models with GMM
        :param models_dictionary: dictionary of models
        :param path_to_train: full path were are the files to train the models
        :param path_to_save: full path were we want to save the GMM models
        :param features: if is set as True, then a set of features will be extracted
        :param plot: if True, then plot the results
        """
        # Generate a model for each type of gesture
        for model in self.models_description:
            gesture_model = hmpy.GestureModel(model['name'],self.path_to_train,self.path_to_save,model['training_examples'])
            if(train):
                gesture_model.buildModel("GMM", self.data_type, self.features)
            self.list_models.append(gesture_model)

    def generate_DNN_datasets(self):
        """
        This function can be used to help to generate gesture models with DNN
        :param models_dictionary: dictionary of models
        :param path_to_train: full path were are the files to train the models
        :param path_to_save: full path were we want to save the RNN models
        :param features: if is set as True, then a set of features will be extracted
        :param plot: if True, then plot the results
        """
        # Generate a model for each type of gesture
        for model in self.models_description:
            gesture_model = hmpy.GestureModel(model['name'],self.path_to_train,self.path_to_save,model['training_examples'])
            self.list_models.append(gesture_model)

        #Create a list of models
        value = hmpy.pre1D.equal_inputs(self.list_models, "min")
        print "min value = ", value*3

        for model in self.list_models:
            model.buildModel("DNN", self.data_type, self.features, value=value)
        
        # Create datasets 
        dnn_dataset = concatenate((self.list_models[0].dnn_dataset,self.list_models[1].dnn_dataset), axis=0)
        i = 2
        n = size(self.list_models)

        while(i < n):
            dnn_dataset = concatenate((dnn_dataset,self.list_models[i].dnn_dataset), axis=0)
            i = i + 1
        #Inputs
        X = dnn_dataset

        #Outputs
        n_classes = size(self.list_models)
        #Y = hmpy.pre1D.set_outputs(n_classes,self.models_description[0]['training_examples'])
        Y = hmpy.pre1D.set_outputs(n_classes,10)
        print Y

        n_examples, n_inputs = shape(X)
        print shape(X)
        print shape(Y)

        return self.list_models, X, Y, n_examples, n_inputs, value


    def load_models(self,plot = False):
        """
        This function can be used to help to load models to a posteori recognition phase
        :param plot: if True, then the GMM model are plotted
        """

        i = 0
        for model in self.list_models:
            print ("loading model: " + self.models_description[i][ 'name'])
            model.loadModel(self.data_type, self.models_description[i][ 'threashlod'], self.features)
            i = i +  1
            if plot and self.data_type == "3IMU_acc":
                print ("plotting GMM models")
                if self.features :
                    model.plotResults_IMU_acc_f()
                else:
                    model.plotResults_IMU_acc()   

    def validate_GMM_models(self, path_of_the_files, n_initial  = 1, n_final = 3):

        print "Validation **********+"
        r =  hmpy.Recognition(self.list_models, "GMR", self.data_type , self.features )
        import os
        dir_path = os.getcwd()
        print "Current path in ", dir_path

        # Define the raw datasets paths (without aligned)
        path_to_validate = dir_path + path_of_the_files

        for model in self.models_description:
            n_model =  model['name']
            for n_data in range(n_initial,n_final+1):
                sfile = n_model + "/acc" + str(n_data) +   ".txt"
                print sfile
                r.recognition_from_files(path_to_validate, sfile, False, n_data)