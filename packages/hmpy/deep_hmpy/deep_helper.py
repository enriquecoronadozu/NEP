#!/usr/bin/env python

# Luis Enrique Coronado Zuniga
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

"""@See preprocessed 1 dimensional data
"""
import hmpy
import deep_hmpy
from keras.models import Sequential
from keras.layers import Dense
import timeit
from numpy import*
from keras.models import model_from_json

class deep_helper():
    
    def __init__(self):
        print ("New deep helper")

    def train_network(self, X, Y, n_examples, n_inputs, seed  = 7):
        seed = 7
        random.seed(seed)

        # Create model
        model = Sequential()

        # Fully connected -> Dense class
        # firt argument -> number of neurons
        # Init -> Initialization of the weights: nomal or gaussian distribution
        # activation -> activation function method 
        # - better performance is achieved using the rectifier activation function_base
        # - Sigmoid on the output layer to ensure our network output is between 0 and 1

        # First hidden layer: has 12 neurons and expects 8 input variables
        model.add(Dense(12, input_dim=n_inputs, init='uniform', activation='relu'))

        # Secong hidden layer
        model.add(Dense(8, init='uniform', activation='relu'))

        # Output layer 
        model.add(Dense(3, init='uniform', activation='sigmoid'))

        print ("DNN created")

        # Compile the net
        # Select: loss function, the optimizer,  optional metrics to report durin training
        # In Keras:
        # logarithmic loss  -> binary_crossentropy 
        # efficient gradient descent algorithm -> adam
        # report acurrancy metric, metrics=['accuracy']

        tic=timeit.default_timer()

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        print ("Model compiled")

        # nb_epoch = iterations
        # batch_size =  instances that are evaluated before a weight update in the network is performed

        # Fit the net
        #verbose=0 to avoid error in jypiter, ipython

        model.fit(X, Y, nb_epoch=100, batch_size=3, verbose=0)
        toc=timeit.default_timer()
        tm = toc -tic

        print ("Fit complete in" , toc - tic , "seconds")

        tic=timeit.default_timer()
        print "Evaluation ****************************"
        scores = model.evaluate(X, Y)
        print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

        predictions = model.predict(X)
        # round predictions
        for x in predictions:
            print(round(x[0]),round(x[1]),round(x[2]) )
        toc=timeit.default_timer()

        tm = toc -tic
        print "Time ", tm
        print ("Saving the deep model ****************")

        self.dnn_model = model 
        # serialize model to JSON
        model_json = model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights("model.h5")
        print("The model was saved as model.json (dnn structure) and model.h5 (weights)")


    def load_deep_model(self, path_json, path_h5):
        """ Load a deep model save with Keras
            param path_json: path of the json file were the structure of the neural network was saved
            param path_h5: path of the h5 file were the weights  of the neural network was saved
        """
        # load json and create model
        json_file = open(path_json, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)

        # load weights into new model
        loaded_model.load_weights(path_h5)
        print("Loaded model from disk")

        self.dnn_model = loaded_model

    def test_trainig_data(self,X,Y, value,file_number):
        """ Test the model with the training data
            param X: inputs
            param Y: outputs
            param value: numebr of fixed samples (window)
        """
        tic=timeit.default_timer()

        #Here, in one_X we obtain the information of one of the datasets
        one_X = ones((1,(value-1)*3))*X[file_number]
        # evaluate loaded model on test data
        self.dnn_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        score = self.dnn_model.evaluate(X, Y, verbose=0)

        predictions = self.dnn_model.predict(one_X)
        # round predictions
        for x in predictions:
            print(round(x[0]),round(x[1]),round(x[2]) )
        toc=timeit.default_timer()
        tm = toc -tic
        print "Time ", tm
    
    def validate_RNN_models(self, path_of_the_files, n_initial  = 1, n_final = 3):
        #TODO: no finalizdada
        n_data = 1
        sfile = path_to_validate + name_model1 + "/acc" + str(n_data) +   ".txt"
        print sfile

        number_inputs =  value*3
        number_outputs = 3
        deep = deep_hmpy.DeepClassifier ("model.json", value*3,number_outputs,"3IMU_acc",False)
        poss = deep.gesture_prediction(one_X)
        print poss


    