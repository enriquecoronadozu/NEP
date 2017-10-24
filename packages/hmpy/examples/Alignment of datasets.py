
# coding: utf-8

# # Aligment of datasets
# 
# ### Autor: Luis Enrique Coronado Zuñiga
# 
# ## Descrption:
# 
# In this example we align and cut some set of fils with the data to be used to train gesture models

# In[12]:

get_ipython().magic(u'matplotlib inline')

import os
from hmpy import Aligment
from matplotlib import pyplot as plt

def align_helper(path_to_load,name_model,files_id,training_examples,axis):
    print "Main path of the gestures defined in:",  path_to_load
    # Create a new class A for the aligment of the data
    aligment = Aligment(path_to_load, name_model,files_id,training_examples,axis)
    # Aligment using dtw
    offsets = aligment.dtw_aligment()

    #See the offsets betweem data
    print offsets
    
    return aligment, offsets


# In[13]:

# Get current path
c_path = os.getcwd()

path_to_load = c_path +  "/data_examples/acceleration_raw"
path_to_save = c_path +  "/data_examples/acceleration_aligned"

# We consider that the datasets of each gesture are separated 
# in folders with the name of the gesture

# We define the name of the gesture
name_model = "hand_up"

# We consider that each training example are in txt files with the format of
# `file_id + number_of_example + .txt`
# For this example the txt files of each gesture have a file_id of:
files_id = "acc"

# We need to define the max number of examples
training_examples = 15

# Define the dimention (x = 0,y = 1, or z =2) in which the aligment will be based. 
# If there are not good results try with other axis.
axis = 0

aligment, offsets = align_helper(path_to_load,name_model,files_id,training_examples,axis)


# In[14]:

# Show aligned data, figure 2
aligment.plotDataAligned()
plt.show()


# In[15]:

# Save the aligned data, create a new folder in `newpath` with the name of the gesture

# Each training example must have the same number of samples for a specific gesture
# The we need to define the limits of the samples to be cutted
cut_left = 50
cut_right = 130
# TO DO:  How to do this automatically, without manual inspection?

# This intruction save a cut the data.
# Also shows if the data is saved correctly, otherwise also shows what to do
new_data = aligment.save(cut_left,cut_right,offsets,path_to_save)



# In[16]:

# Show original data, figure 1
aligment.plotData()
plt.show()

# Show aligned data, figure 2
aligment.plotDataAligned()
plt.show()


# In[ ]:



