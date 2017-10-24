#!/usr/bin/env python

# Luis Enrique Coronado Zuniga
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

"""@See preprocessed 1 dimensional data
"""
from hmpy import*
from scipy import linalg


#TODO: documentation

import os
class arm_gesture():
    """
    Main class used to train, load and validate arm gesture models using GMM and RNN
    :param main_path: name of the main path where the datasets of observations and the models are saved. 
    
    Inside the main_path folder must be folder shown bellow:
    
    - raw
    - segmentation
    - validation
    - models
        
    The **raw** folder must contain the raw datasets from sensors. The **segmentation** folder have the datasets segmented or preprocessed.
    In the **validation** folder the validation images where saved. The models will be saved in the **models** folder.
    
    """
    
    def __init__(self, main_path, data_type = "3IMU_acc"):
        print "New path: "+ main_path
        self.data_type = data_type
        self.main_path = main_path
        self.path_to_train = self.main_path + "/segmented/"
        self.path_to_save =  self.main_path + "/models/"
        self.path_to_validation =  self.main_path + "/validation/"
        self.path_raw_data =  self.main_path + "/raw/"
        self.gestures = self.getGestureNames()
    
    
    def getGestureNames(self):
        """ Get all the names of the folders (gestures) inside the main_path/segmentation folder
        """
        try:
            gestures_names = os.listdir(self.path_to_train)
            print ("Name of the gestures : " + str(gestures_names))
            return gestures_names
        except:
            print ("Error: " + self.main_path +  "/segmented folder do not exist")
    
    def trainSingleGesture(self,gesture_name, th_cluster = 0.68, features = False):
        """ Function used to train a single gesture. It is needed to specify the algorithm to use, the type of data and if it will be a feature extraction process
            :param data_type: can be "3IMU_acc" (3 axis acceleration) ...
            :param features: bool value, if True feature extraction is performed.
        """
        if gesture_name in self.gestures:
            self.models_description = [{ 'name': gesture_name, 'threashlod': 100}]
            self.list_models = []
            print len([name for name in os.listdir(self.path_to_train) if os.path.isfile(name)])
            
            gesture_model = GestureModel(gesture_name,self.path_to_train,self.path_to_save)
            gesture_model.buildGMM_model(self.data_type, features, th_cluster)
                
        else:
            print "There are not datasets for train the gesture **"  +  gesture_name  +  "**. Check if the correct name of gesture was selected"

    def trainAllGestures(self, th_cluster = [0.69], features = False):
        """ Function used to train all the gesture in the segmented. It is needed to specify the algorithm to use, the type of data and if it will be a feature extraction process
            :param data_type: can be "3IMU_acc" (3 axis acceleration) ...
            :param features: bool value, if True feature extraction is performed.
        """
        
        i  = 0
        for gesture in self.gestures:
            self.trainSingleGesture(gesture, th_cluster[i],  features)
            i = i + 1


        
    def loadAllGestures(self, features = False, th = [100]):
        models = []

        i = 0
        for gesture in self.gestures:
            models.append(self.loadSingleGesture(gesture, self.data_type, features, th[i]))
            i = i + 1
        return models
            
    
    def loadSingleGesture(self, gesture_name, data_type = "3IMU_acc" , features = False, th = 100):
        self.features = features
        self.path_models = self.path_to_save + gesture_name
        self.threashold = th
        print
        print (" *** Loading model ***")
        print ("threashold = 100")
            
        if data_type == "3IMU_acc":
            print ("Type = 3IMU_acc model")
            if features:
                print ("Using features of Gravity and Body")
                self.gr_points = loadtxt(self.path_models+"/MuGravity.txt")
                self.gr_sigma = loadtxt(self.path_models+"/SigmaGravity.txt")
                self.model_gravity = {"mean":self.gr_points, "sigma":self.gr_sigma, "weights":0.5}

                self.b_points = loadtxt(self.path_models+"/MuBody.txt")
                self.b_sigma = loadtxt(self.path_models+"/SigmaBody.txt")

                self.setModel("gravity",self.gr_points, self.gr_sigma,self.threashold)
                self.setModel("body",self.b_points, self.b_sigma,self.threashold)
                self.model_body = {"mean":self.b_points, "sigma":self.b_sigma, "weights":0.5}
                    
                self.model = {"name":gesture_name, "gravity":self.model_gravity, "body":self.model_gravity, "threashold":self.threashold }
            else:
                print "No features of Gravity and Body"
                self.acc_points = loadtxt(self.path_models+"/MuIMUacc.txt")
                self.acc_sigma = loadtxt(self.path_models+"/SigmaIMUacc.txt")
                self.model_acc = {"mean":self.acc_points, "sigma":self.acc_sigma}
                self.model = {"name":gesture_name, "3_axis":self.model_acc, "threashold":self.threashold}
            
            if self.data_type == "3IMU_acc":
                print ("plotting GMM models")
                if features :
                    self.plotGMMmodel_3IMU(feature = True)
                else:
                    self.plotGMMmodel_3IMU(feature =  False)
                    
            return self.model
                        
    def plotGMMmodel_3IMU(self, feature = "False"):
        """Plot the results of GMR + GMM used to create the model (Gravity and Body)
        """
        print self.path_models
        if feature: 
                
            import matplotlib.pyplot as plt
            gr_points =  self.gr_points
            gr_sig = self.gr_sigma
            b_points = self.b_points
            b_sig =  self.b_sigma

            gr_points = gr_points.transpose()
            b_points = b_points.transpose()

            gr_sigma = []
            b_sigma = []

            n,m = gr_points.shape

            maximum = zeros((m))
            minimum = zeros((m))

            x = arange(0,m,1)

            for i in range(m):
                gr_sigma.append(gr_sig[i*3:i*3+3])
                b_sigma.append(b_sig[i*3:i*3+3])


            for i in range(m):
                sigma = 3.*linalg.sqrtm(gr_sigma[i])
                maximum[i] =  gr_points[0,i]+ sigma[0,0];
                minimum[i] =  gr_points[0,i]- sigma[0,0];

            fig2 = plt.figure()
            import matplotlib.pyplot as plt
            plt.fill_between(x, maximum, minimum,lw=2, alpha=0.5 )
            plt.plot(x, gr_points[0])
            plt.savefig(self.path_models+ "/_gravity_x_axis.png")
            plt.close('all')

            for i in range(m):
                sigma = 3.*linalg.sqrtm(gr_sigma[i])
                maximum[i] =  gr_points[1,i]+ sigma[1,1];
                minimum[i] =  gr_points[1,i]- sigma[1,1];

            fig3 = plt.figure()
            plt.fill_between(x, maximum, minimum,lw=2, alpha=0.5 )
            plt.plot(x, gr_points[1])
            plt.savefig(self.path_models+ "/_gravity_y_axis.png")
            plt.close('all')

            for i in range(m):
                sigma = 3.*linalg.sqrtm(gr_sigma[i])
                maximum[i] =  gr_points[2,i]+ sigma[2,2];
                minimum[i] =  gr_points[2,i]- sigma[2,2];

            fig3 = plt.figure()
            import matplotlib.pyplot as plt
            plt.fill_between(x, maximum, minimum,lw=2, alpha=0.5 )
            plt.plot(x, gr_points[2])
            plt.savefig(self.path_models+ "/_gravity_z_axis.png")
            plt.close('all')

            for i in range(m):
                sigma = 3.*linalg.sqrtm(b_sigma[i])
                maximum[i] =  b_points[0,i]+ sigma[0,0];
                minimum[i] =  b_points[0,i]- sigma[0,0];

            fig4 = plt.figure()
            import matplotlib.pyplot as plt
            plt.fill_between(x, maximum, minimum,lw=2, alpha=0.5 )
            plt.plot(x, b_points[0])
            plt.savefig(self.path_models+ "/_body_x_axis.png")
            plt.close('all')

            for i in range(m):
                sigma = 3.*linalg.sqrtm(b_sigma[i])
                maximum[i] =  b_points[1,i]+ sigma[1,1];
                minimum[i] =  b_points[1,i]- sigma[1,1];

            fig5 = plt.figure()
            import matplotlib.pyplot as plt
            plt.fill_between(x, maximum, minimum,lw=2, alpha=0.5 )
            plt.plot(x, b_points[1])
            plt.savefig(self.path_models+ "/_body_axis.png")
            plt.close('all')

            for i in range(m):
                sigma = 3.*linalg.sqrtm(b_sigma[i])
                maximum[i] =  b_points[2,i]+ sigma[2,2];
                minimum[i] =  b_points[2,i]- sigma[2,2];

            fig6 = plt.figure()
            import matplotlib.pyplot as plt
            plt.fill_between(x, maximum, minimum,lw=2, alpha=0.5 )
            plt.plot(x, b_points[2])
            plt.savefig(self.path_models+ "/_body_z_axis.png")
            plt.close('all')
            
        else:
                
            import matplotlib.pyplot as plt
            gr_points =  self.acc_points
            gr_sig = self.acc_sigma


            gr_points = gr_points.transpose()

            gr_sigma = []

            n,m = gr_points.shape

            maximum = zeros((m))
            minimum = zeros((m))

            x = arange(0,m,1)

            for i in range(m):
                gr_sigma.append(gr_sig[i*3:i*3+3])

            for i in range(m):
                sigma = 3.*linalg.sqrtm(gr_sigma[i])
                maximum[i] =  gr_points[0,i]+ sigma[0,0];
                minimum[i] =  gr_points[0,i]- sigma[0,0];

            fig2 = plt.figure()
            import matplotlib.pyplot as plt
            plt.fill_between(x, maximum, minimum,lw=2, alpha=0.5 )
            plt.plot(x, gr_points[0])
            plt.savefig(self.path_models+ "/_acc_x_axis.png")
            plt.close('all')

            for i in range(m):
                sigma = 3.*linalg.sqrtm(gr_sigma[i])
                maximum[i] =  gr_points[1,i]+ sigma[1,1];
                minimum[i] =  gr_points[1,i]- sigma[1,1];

            fig3 = plt.figure()
            plt.fill_between(x, maximum, minimum,lw=2, alpha=0.5 )
            plt.plot(x, gr_points[1])
            plt.savefig(self.path_models+ "/_acc_y_axis.png")
            plt.close('all')

            for i in range(m):
                sigma = 3.*linalg.sqrtm(gr_sigma[i])
                maximum[i] =  gr_points[2,i]+ sigma[2,2];
                minimum[i] =  gr_points[2,i]- sigma[2,2];

            fig3 = plt.figure()
            import matplotlib.pyplot as plt
            plt.fill_between(x, maximum, minimum,lw=2, alpha=0.5 )
            plt.plot(x, gr_points[2])
            plt.savefig(self.path_models+ "/_acc_z_axis.png")
            plt.close('all')

    #TODO: save in validation folder and auto get all the samples insetad of select a number
    def validateGestureModels(self, list_models, n_files):
        print "********* Validation **********"
        
        self.list_models = list_models
        r =  Recognition(self.list_models, self.data_type , self.features )
        dir_path = os.getcwd()

        # Define the raw datasets paths (without aligned)
        path_to_validate = self.path_raw_data

        for model in self.list_models:
            name_model =  model['name']

            for n_data in range(1,n_files):
                
                dataset = name_model + "/acc" + str(n_data) +   ".txt"
                print ("Datset used to validation: " +  dataset)
                r.recognition_from_files(name_model, path_to_validate, dataset, n_data)
            
  
