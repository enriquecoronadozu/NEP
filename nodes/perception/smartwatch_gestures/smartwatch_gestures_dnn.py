#!/usr/bin/env python

# Luis Enrique Coronado Zuniga
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.



#%%   
import os
from hmpy import*
from nep import*
import timeit
from numpy import*
import sys
from keras.models import model_from_json

     
dir_path = os.getcwd()
print dir_path
seed = 1

#Configuration of the models
create_models = False
features = False

#Define the name of the gesture
name_model1 = "saludo"
name_model2 = "karate"
name_model3 = "espada"


# ************************************** Gesture, data and paths definitions *********************************************

#Define the path to save the models
path_to_save = dir_path + "/data/models/"

#Define the path of the gesture folders
path_to_load = dir_path + "/data/segmented/"

#Define id (name) of the files in the datatest, example <acc(1)>.txt, example <acc(2)>.txt , ....
files_id = "acc"

#Crate a new model
create_models = True

gest1 = GestureModel(name_model1,path_to_load,path_to_save)
gest2 = GestureModel(name_model2,path_to_load,path_to_save)
gest3 = GestureModel(name_model3,path_to_load,path_to_save)


#Create a list of models
list_models = [gest1,gest2,gest3]

value = pre1D.equal_inputs(list_models, "min")
print  "minimun value of samples: ",  value*3

# Start publisher and sensory subcriber
pub = publisher("127.0.0.1", 5002, "/human_state", True) #Allow multiple publishers
sub =  subscriber("127.0.0.1", 7070, "/smart_accel") #Allow multiple subscribers
        
path = os.getcwd()
path_data = path + "/data" #This is not used in the moment
# load weights into new model
# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")
# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#TODO: read from dictionaty
decode = decode_message(",")
print ("\n")
print ("********* Arm gesture recognition node ***********")
print ("Ready to read the data and recognize the gestures")
print ("Waiting for the data...")

from deep_hmpy import DeepClassifier
windows_size = value
input_neurons_size =  value*3
output_neurons_size = 3
print "windows size is of =", windows_size
print "Then number of input neurons must be", input_neurons_size 
deep = DeepClassifier ("model.json", input_neurons_size,output_neurons_size,"3IMU_acc",False)

print "waiting fro data"
run = True
poss = 0
while run:
        data = sub.listen_string()
        flag, x,y,z = decode.decode_3axis_info(data)
        poss = deep.online_validation(float(x),float(y),float(z))
        
        try: #TODO, antes de que se llene manda un enetero luego una lista, esto puede causar eerroe y confusiones
                if(poss[0]>.95):
                        print "1"
                if(poss[1]>.95):
                        print "2"
                if(poss[2]>.95):
                        print "3"
                pub.send_string(str(poss[1]), "/possibility")
                #message = {'poss': str(poss[1])}
                #pub.send_info(message, "/possibility")
        except:
                print "windows not filled yet"
        

        







