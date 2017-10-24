#!/usr/bin/env python

# Luis Enrique Coronado Zuniga
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

# Descrption: ---------------------------------
# This node can be use to perform online recgnition of arm gesture using werable devices.
# Two types of results are published: probabilities and triggers
# The probabilities results are continuously published in the topic "/possibility" in each time step
# The triggers are published in the topic "/ human_state" after a gesture is detected a certain number of times
# ---------------------------------------------


from hmpy import*
import os
import nep
import timeit
from numpy import*
import sys

def main(name):
        
        node = nep.node("smartwatch_gesture")

        sub_config = node.config_sub()
        sub = node.new_sub("/smart_accel", sub_config)

        pub_config = node.config_pub()
        pub = node.new_pub("/human_state", pub_config)
        
                
        path = os.getcwd()
        path_data = path + "/data"
        arm = arm_gesture(path_data)

        th = 100
        if name == "batting":
                th = 50
        if name == "katana":
                th = 50

        print name
        model = arm.loadSingleGesture(name, th = th)

        th = .7  # The gesture is detected if the possibilities are > than .7
        times = 0 # Times that a gesture is detected
        itrigger = 5 # Times that a gesture must be detected before send a trigger

        r =  Recognition([model], "3IMU_acc")

        #TODO: read from dictionaty
        decode = decode_message(",")
        print ("\n")
        print ("********* Arm gesture recognition node ***********")
                
        print ("Ready to read the data and recognize the gestures")
        print ("Waiting for the data...")

        run = True
        while run:
                s, data = sub.listen_string()
                flag, x,y,z = decode.decode_3axis_info(data)
                poss =  r.online_recognition(float(x),float(y),float(z))
                #Send data for plot
                pub.send_string(str(poss), "/possibility")
                if(poss >th):
                        times = times + 1
                        if(times>itrigger):
                                times = 0
                                #Publish the gesture detected (trigger)
                                message = {'human_action':  name}
                                pub.send_info(message)
                                print message
    
if __name__ == "__main__":
        
        # Set the gesture to recognize
        try:
                gesture_name = sys.argv[1]
        
        # If not set a default gesture
        except:
                gesture_name = 'karate'
        
        #Start the program
        main(gesture_name)
       
