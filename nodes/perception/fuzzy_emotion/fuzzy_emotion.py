#!/usr/bin/env python

# Luis Enrique Coronado Zuniga
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

from nep import nep_msg
import nep
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from sklearn.neighbors.nearest_centroid import NearestCentroid
import numpy as np
import time
import threading




def HIFIS(kinect_distance, face_happy =  False, face_engagend =  False):
        #--------------------------------------------------#
        #Membership Function - Input and Output Properties
        Distance = ctrl.Antecedent(np.arange(0,450,1),'Distance')
        Pleasure = ctrl.Consequent(np.arange(-10,10,1),'Pleasure')
        Arousal = ctrl.Consequent(np.arange(-10,10,1),'Arousal')
        Dominance = ctrl.Consequent(np.arange(-10,10,1),'Dominance')

        #Membership Function 
        #-----------------------
        #Input
        std_dist = 30
        #first number as mean value, second as gaussian number
        Distance['near']=fuzz.gauss2mf(Distance.universe,0,std_dist,30,std_dist)
        Distance['comfortable']=fuzz.gauss2mf(Distance.universe,70,std_dist,250,std_dist) 
        Distance['far']=fuzz.gauss2mf(Distance.universe,300,std_dist,450,std_dist)

        std = 6
        dist1 = 1
            
        high_mean_1 = 9
        med_mean_1 = -1
        low_mean_1 = -10

        if face_happy == True:
            high_mean_1 = 9
            low_mean_1 = 0
            std = 1
            
        elif face_engagend == False:
            high_mean_1 = 2
            std = 1

            
        high_mean_2 = high_mean_1 + dist1  
        low_mean_2 = low_mean_1 + dist1

        Pleasure['high']=fuzz.gauss2mf(Pleasure.universe,high_mean_1,std,high_mean_2,std)
        Pleasure['low']=fuzz.gauss2mf(Pleasure.universe,low_mean_1,std,low_mean_2,std)

        Arousal['high']=fuzz.gauss2mf(Arousal.universe,high_mean_1,std,high_mean_2,std)
        Arousal['low']=fuzz.gauss2mf(Arousal.universe,low_mean_1,std,low_mean_2,std)

        Dominance['high']=fuzz.gauss2mf(Dominance.universe,high_mean_1,std,high_mean_2,std)
        Dominance['low']=fuzz.gauss2mf(Dominance.universe,low_mean_1,std,low_mean_2,std)

        #Rules 
        rule1=ctrl.Rule(Distance['near'] , 
                        Pleasure['low'])
        rule2=ctrl.Rule(Distance['comfortable'], 
                        Pleasure['high'])
        rule3=ctrl.Rule(Distance['far'] , 
                        Pleasure['low'])

        rule4=ctrl.Rule(Distance['near'] , 
                        Arousal['low'])
        rule5=ctrl.Rule(Distance['comfortable'], 
                        Arousal['high'])
        rule6=ctrl.Rule(Distance['far'] , 
                        Arousal['low'])

        rule7=ctrl.Rule(Distance['near'] , 
                        Dominance['low'])
        rule8=ctrl.Rule(Distance['comfortable'], 
                        Dominance['high'])
        rule9=ctrl.Rule(Distance['far'] , 
                        Dominance['low'])

        emotion_human_human_eval = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9])
        emotion_human = ctrl.ControlSystemSimulation(emotion_human_human_eval)

        emotion_human.input['Distance']= kinect_distance

        #computing input to output
        emotion_human.compute()
        P = emotion_human.output['Pleasure']
        A = emotion_human.output['Arousal']
        D = emotion_human.output['Dominance']

        return P.item(),A.item(),D.item()

def EFIS(T,H,B,motor):
        
        value  = motor/4
            

        #--------------------------------------------------#

        #Membership Function - Input and Output Properties
        Temperature = ctrl.Antecedent(np.arange(0,49,1),'Temperature')
        Humidity = ctrl.Antecedent(np.arange(0,101,1),'Humidity')
        Brightness = ctrl.Antecedent(np.arange(0,101,1),'Brightness')

        Pleasure = ctrl.Consequent(np.arange(-10,11,1),'Pleasure')
        Arousal = ctrl.Consequent(np.arange(-10,11,1),'Arousal')
        Dominance = ctrl.Consequent(np.arange(-10,11,1),'Dominance')

        #Membership Function 
        #-----------------------
        #Input
        Temperature['cold']=fuzz.gauss2mf(Temperature.universe,0-value,8, 0-value,8)
        Temperature['comfort']=fuzz.gauss2mf(Temperature.universe,24-value,8, 25-value,8)
        Temperature['hot']=fuzz.gauss2mf(Temperature.universe,38-value,8, 100-value,8)

        Humidity['dry']=fuzz.gaussmf(Humidity.universe,0,15)
        Humidity['comfort']=fuzz.gaussmf(Humidity.universe,50,15)
        Humidity['wet']=fuzz.gaussmf(Humidity.universe,100,15)

        Brightness['dark']=fuzz.gaussmf(Brightness.universe,0,25)
        Brightness['bright']=fuzz.gaussmf(Brightness.universe,100,25)


        #-----------------------
        #Output

        high_mean_1 = 9
        low_mean_1 = -10
        std = 1.5
        dist1 = 1

        high_mean_2 = high_mean_1 + dist1  
        low_mean_2 = low_mean_1 + dist1

        Pleasure['high']=fuzz.gauss2mf(Pleasure.universe,high_mean_1,std,high_mean_2,std)
        Pleasure['low']=fuzz.gauss2mf(Pleasure.universe,low_mean_1,std,low_mean_2,std)

        Arousal['high']=fuzz.gauss2mf(Arousal.universe,high_mean_1,std,high_mean_2,std)
        Arousal['low']=fuzz.gauss2mf(Arousal.universe,low_mean_1,std,low_mean_2,std)

        Dominance['high']=fuzz.gauss2mf(Dominance.universe,high_mean_1,std,high_mean_2,std)
        Dominance['low']=fuzz.gauss2mf(Dominance.universe,low_mean_1,std,low_mean_2,std)

        #--------------------------------------------------#                

        #Rules 
        rule1=ctrl.Rule(Temperature['cold'] & Humidity['dry'] & Brightness['dark'], 
                        (Pleasure['low'] , Arousal['high'] , Dominance['low']))   # Afraid

        rule2=ctrl.Rule(Temperature['cold'] & Humidity['dry'] & Brightness['bright'], 
                        (Pleasure['low'] , Arousal['low'] , Dominance['low']))    # Sad

        rule3=ctrl.Rule(Temperature['cold'] & Humidity['wet'] & Brightness['dark'], 
                        (Pleasure['low'] , Arousal['low'] , Dominance['high']))   # Disdainful

        rule4=ctrl.Rule(Temperature['cold'] & Humidity['wet'] & Brightness['bright'], 
                        (Pleasure['low'] , Arousal['low'] , Dominance['low']))    # Sad


        rule5=ctrl.Rule(Temperature['comfort'] & Humidity['dry'] & Brightness['dark'], 
                        (Pleasure['high'] , Arousal['high'] , Dominance['low']))   # Suprised

        rule6=ctrl.Rule(Temperature['comfort'] & Humidity['dry'] & Brightness['bright'], 
                        (Pleasure['high'] , Arousal['high'] , Dominance['high']))  # Happy


        rule7=ctrl.Rule(Temperature['comfort'] & Humidity['comfort'] & Brightness['bright'], 
                        (Pleasure['high'] , Arousal['high'] , Dominance['high']))  # Happy

        rule8=ctrl.Rule(Temperature['comfort'] & Humidity['comfort'] & Brightness['dark'], 
                        (Pleasure['high'] , Arousal['low'] , Dominance['high']))    # Relaxed


        rule9=ctrl.Rule(Temperature['comfort'] & Humidity['wet'] & Brightness['dark'], 
                        (Pleasure['high'] , Arousal['low'] , Dominance['low']))    # Protected

        rule10=ctrl.Rule(Temperature['comfort'] & Humidity['wet'] & Brightness['bright'], 
                        (Pleasure['high'] , Arousal['low'] , Dominance['high']))   # Relaxed


        rule11=ctrl.Rule(Temperature['hot'] & Humidity['dry'] & Brightness['dark'], 
                        (Pleasure['high'] , Arousal['high'] , Dominance['high']))  # Happy

        rule12=ctrl.Rule(Temperature['hot'] & Humidity['dry'] & Brightness['bright'], 
                        (Pleasure['low'] , Arousal['high'] , Dominance['high']))  # Angry

        rule13=ctrl.Rule(Temperature['hot'] & Humidity['wet'] & Brightness['dark'], 
                        (Pleasure['low'] , Arousal['low'] , Dominance['high']))   # Disdainful

        rule14=ctrl.Rule(Temperature['hot'] & Humidity['wet'] & Brightness['bright'], 
                        (Pleasure['low'] , Arousal['high'] , Dominance['high']))  # Angry


                        

                        
        emotion_eval = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9,rule10,rule11,rule12,rule13,rule14])
        emotion = ctrl.ControlSystemSimulation(emotion_eval)      
                

        #input 
        emotion.input['Temperature']=T
        emotion.input['Humidity']=H
        emotion.input['Brightness']=B

        #computing input to output
        emotion.compute()
        P = emotion.output['Pleasure']
        A = emotion.output['Arousal']
        D = emotion.output['Dominance']

        return P.item(),A.item(),D.item()
        


def mapping (Pf,Af,Df):

        emotions = {1:"happy", 2:"angry", 3:"afraid", 4: "surprised", 5:"relaxed", 6:"disdainful", 7:"sad", 8:"protected", 9:"neutral"}

        P = 4
        A = 4
        D = 4

        X = np.array([[P, A, D], [-P, A, D], [-P, A, -D], [P, A, -P], [P, -A, D], [-P, -A, D], [-P, -A, -D], [P, -A, -D], [0,0,0]])
        y = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        clf = NearestCentroid()
        clf.fit(X, y)
        NearestCentroid(metric='euclidean', shrink_threshold=None)
        pad_vector = clf.predict([[Pf, Af, Df]])

        current_emotion = emotions[pad_vector[0]]
        return current_emotion

def emotion_():
        while True:

                Phi,Ahi,Dhi = HIFIS(dist,happy,engaged)
                Pe,Ae,De = EFIS(temp,hum,brig,RT)

                P = Phi*alphav + Pe*(1)
                A = Ahi*alphav + Ae*(1)
                D = Dhi*alphav + De*(1)
                
                print "P = " + str(P) +  " , A = " + str(A) + " , D = " + str(D)
                print "Pe = " + str(Pe) +  " , Ae = " + str(Ae) + " , De = " + str(De)
                print "Phi = " + str(Phi*alphav) +  " , Ahi = " + str(Ahi*alphav) + " , Dhi = " + str(Dhi*alphav)
                current_emotion = mapping(P,A,D)
                print current_emotion
                msg = {"emotion": current_emotion}
                pub_emotion.send_info(msg)

                time.sleep(.5)
        
import time

alphav = 0.2 # Personalized variable
node = nep.node("subscriber_node") # Create a new node
conf = node.conf_sub() # Select the configuration of the subscriber

sub_kinect = node.new_sub("/kinect_human", conf) # Set the topic and the configuration of the subscriber
sub_env = node.new_sub("/enviroment", conf) # Set the topic and the configuration of the subscriber
conf = {'msg_type':"dict", 'transport':"ZMQ" , 'network':"P2P", 'port': "9000", 'ip': "127.0.0.1", 'mode': "many2many" }
pub_emotion = node.new_pub("/robot_emotion", conf) # Set the topic and the configuration of the subscriber


Phi = 0
Ahi = 0
Dhi = 0
Pe = 0
Ae = 0
De = 0
samples_dist = 0
samples_happy = 0
samples_engaged = 0
forget_people = 0
temp = 20
hum  = 50
brig = 50
RT = 30
dist = 1000
happy =  False
engaged = False

#New thread that can de used to stop the program
emition_calc = threading.Thread(target = emotion_)
# Used to finish the background thread when the main thread finish
emition_calc.daemon = True
# Start new thread 
emition_calc.start()

start = time.time()

while True:

        s, msg = sub_kinect.listen_info()
        if s:
                start = time.time()
                dist = msg["pedes_pos"][2]*100
                if msg["face_happy"] == "yes":
                        happy =  True
                elif  msg["face_happy"] == "no":
                        happy =  False

                if msg["face_engaged"] == "yes":
                        engaged =  True
                elif msg["face_engaged"] == "no":
                        engaged = False
        
                
        s, msg = sub_env.listen_info()
        if s:
                start = time.time()
                temp = msg["T"]
                hum = msg["H"]
                brig = msg["B"]
                RT = msg["RT"]


        end = time.time()
        elapsed = end - start
        if (elapsed > 5): # Update HFIS if not person in 5 seconds
                happy =  False
                engaged = False
                dist = 1000

        time.sleep(.001)

        
        


