#!/usr/bin/env python

# Luis Enrique Coronado Zuniga
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.


#%%
import os
from numpy import*
from hmpy import GestureModel, pre1D
import timeit

dir_path = os.getcwd()
print dir_path

#Delete, this is the size of the windows in GMM
value = 79

#Define the name of the gesture
name_model1 = "hand_up"
name_model2 = "karate"
name_model3 = "press_button"

from gesture import DeepClassifier

path_to_validate = dir_path + "/data/raw/"


n_data = 5
sfile = path_to_validate + name_model3 + "/acc" + str(n_data) +   ".txt"
print sfile

number_inputs =  value*3
number_outputs = 3

#TODO the wieghts in the file .h5 aun no especificado
deep = DeepClassifier ("model.json", value*3,number_outputs,"3IMU_acc",False)
prob = deep.validate_from_file(sfile,delim = ',')


#%%
"""
import matplotlib.pyplot as plt


name_models = [name_model1,name_model2,name_model3]

for j in range(len(name_models)):
    m,n = prob.shape
    x = arange(0,m,1)
    plt.plot(x, results,'-',label= name_models[j])
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
    ncol=2, mode="expand", borderaxespad=0.)

plt.show()

#%%
"""
print matrix.round(prob)
print prob

"""
# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

 
# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(X, Y, verbose=0)

predictions = loaded_model.predict(X)
# round predictions
for x in predictions:
    print(round(x[0]),round(x[1]),round(x[2]) )
toc=timeit.default_timer()

print tm

#Evalute not trained data

# Define the raw datasets paths (without aligned)
path_to_validate = dir_path + "/data_examples/acceleration_raw/"

name_models = [name_model1,name_model2,name_model3]
print "Validation"

# Test examples no used for training
n_initial = 11
n_final = 15


# Example in ipython
%matplotlib inline 

for n_model in name_models:
    for n_data in range(n_initial,n_final+1):
        sfile = n_model + "/acc" + str(n_data) +   ".txt"
        print sfile
        r.recognition_from_files(path_to_validate, sfile, False, n_data)
        predictions = loaded_model.predict(X)
        for x in predictions:
            print(round(x[0]),round(x[1]),round(x[2]) )
"""

print "finished"
    