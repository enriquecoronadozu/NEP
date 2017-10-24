#!/usr/bin/env python

# Luis Enrique Coronado Zuniga

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

"""@See preprocessed data
"""
from numpy import*
import matplotlib.pyplot as plt
from hmpy import*


class Recognition():
    """Class used to recognize a gesture
        :param gesture models: list of gesture models
        :param method_type: type of model "GMM" or "DNN"
        :param data_type: type of data. "3IMU_acc" -> IMU 3D data
        :param feature_extraction: Bool variable


    """
    def __init__(self,gesture_models, data_type = "3IMU_acc", feature_extraction = False):
    
        self.list_classifiers = []
        self.list_models = gesture_models
        self.data_type = data_type
        self.feature_extraction = feature_extraction
        
        # Create a guassian classifier for each gesture
        for model in self.list_models:
            self.list_classifiers.append(Classifier(model,self.data_type,self.feature_extraction))

        # For online recognition we only must to use one model by thread or proecess. 
        self.main_model = self.list_models[0]
        self.main_classifier = self.list_classifiers[0]
            

    def recognition_from_files(self, name_model, path, sfile, n_file):
        """Class used to recognize a gesture
        :param name_model: Name of the correct model
        :param path: path of the folder with the training sets
        :param sfile: name of the .txt file
        :param n: number of file

        """
        # Get list of models
        list_models = self.list_models
        plt.close('all')
        
        

        # Used to plot the results
        fig = plt.figure("Results", figsize=(8, 6))

        # For each model
        for j in range(len(list_models)):

            # Get all the results in a vector
            poss =  self.list_classifiers[j].validate_from_file(path + sfile, ',')
            m,n = poss.shape
            x = arange(0,m,1)

            # Plot the results
            plt.plot(x, poss,'-',label= list_models[j]['name'])
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        figure_name = path  + name_model + "/" +  name_model + str(n_file) + ".png"
        print ("Saving ... " + figure_name)
        plt.savefig(figure_name, bbox_inches='tight')
            
            
    def online_recognition(self,x,y,z):
        """ Online recognition of a gesture 
        :param x: x data
        :param y: y pdata
        :param z: z data
        :return list_results: result of the recognition process (0-1)
        """
        return self.main_classifier.online_validation(x,y,z)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
