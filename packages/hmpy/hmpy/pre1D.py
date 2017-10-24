#!/usr/bin/env python

# Luis Enrique Coronado Zuniga
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

"""@See preprocessed 1 dimensional data
"""
from numpy import*


def getmaxlength(list_models):
    """Obtain the maximum number of samples from a list of models
        param list_models: list of gesture models
    """
    max_d = 0
    for model in list_models:
        max_d = maximum(max_d,model.gesture_model.n_data)
        
    return max_d

def getminlength(list_models):
    """Obtain the minimum number of samples from a list of models
         param list_models: list of gesture models
    """
    min_d = Inf
    for model in list_models:
        min_d = minimum(min_d,model.gesture_model.n_data)
        

        return int(min_d)
def equal_inputs(list_models, c_type = "max"):
    """Used to give to all the data training sets the same length in their samples
        param list_models: list of gesture models
        param c_type: can be "max" or "min" to take the maximun or minimum value of the samples 
        
    """

    if(c_type == "max"):
        value = getmaxlength(list_models)
        return value
        
    if(c_type == "min"):
        value = getminlength(list_models)
        return value
    
def set_outputs (n_classes, n_examples):
    #TODO: esta funcion considera que todos los gestos tiene en mismo numero de ejemplo, cambiar a una variable
    """ Generate outputs in a binary format
        param n_classe: Number of classes or gesture models
        param n_examples: Number of example by classes
    """
    classes = identity(n_classes)
    outputs = zeros((n_examples*n_classes,n_classes))
    
    for i in range (n_classes):
        for j in range (n_examples):
            outputs[i*n_examples+j] = classes[i]
    return outputs
    
