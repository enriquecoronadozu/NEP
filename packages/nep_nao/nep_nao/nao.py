# -*- encoding: UTF-8 -*-

# ------------------------ NAO action class  --------------------------------
# Description: NAO/Pepper functions used to perform some predefined actions
# this class use the NAO SDK
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga

import random
import qi
import sys
from tinydb import TinyDB, Query
import re
import ast
import json
import os
from nep_nao import*
from naoqi import ALProxy
import math
import almath
import time
import almath
# This library allows to create new thread (to do parallel tasks)
import threading


#TODO:
# Add more postures, see: http://doc.aldebaran.com/1-14/naoqi/motion/alrobotposture.html
# Also motion_service and posture service can be global with self?


class nao():
    """ NAO functions used to make NAO talk
        :param ip:  Robot IP
        :param port: Robot port for comunication
    """

    # ********************************** Robot initialization ***********************************************
    def __init__(self,ip,port):
        """ NAO/Pepper functions used to perform some predefined actions of movement
            :param ip:  Robot IP
            :param port: Robot port for comunication
        """
        self.ip = ip
        self.port = int(port)
        self.session = qi.Session()
        self._connection()
        self.language = "English"
        
        self.name_joints = ["LAnklePitch", "LAnkleRoll", "LHipRoll", "LHipYawPitch", "LKneePitch",\
                                "RAnklePitch", "RAnkleRoll", "RHipRoll", "RHipYawPitch", "RKneePitch", \
                                "LElbowRoll", "LElbowYaw", "LHand","LShoulderPitch", "LShoulderRoll", "LWristYaw", \
                                "RElbowRoll", "RElbowYaw" , "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw",\
                                "HeadPitch", "HeadYaw"
                                ]

        #Pepper
        #self.name_joints= ["HeadPitch","HeadYaw", "HipPitch", "HipRoll", "KneePitch", "LElbowRoll", "LElbowYaw",\
        #                  "LHand","LShoulderPitch", "LShoulderRoll", "LWristYaw", "RElbowRoll", "RElbowYaw" , "RHand", \
        #                   "RShoulderPitch", "RShoulderRoll", "RWristYaw"]

        self.data2save = {}
        for name in self.name_joints:
            self.data2save[name] = []
        
 

    def _connection(self):
        """Function used to connect the robot, is used always before that perform an action"""

        try:
            self.session.connect("tcp://" + self.ip  + ":" + str(self.port))
            print 
            print "---- Connected with NAO robot ----"
        except RuntimeError:
            print ("Can't connect to Naoqi at ip \"" + self.ip + "\" on port " + str(self.port) +".\n"
                   "Please check the IP adress or port of the robot")
            sys.exit(1)

        ip = self.ip
        port = self.port


        self.animatedSpeechProxy = ALProxy("ALAnimatedSpeech", ip, port)
        self.postureProxy =  ALProxy("ALRobotPosture", ip, port)
        self.textToSpeechProxy=  ALProxy("ALTextToSpeech",ip,port)
        self.motionProxy = ALProxy("ALMotion",ip,port)
        self.behaviorManagerProxy = ALProxy("ALBehaviorManager",ip,port)
        self.trackerProxy = ALProxy("ALTracker",ip,port)
        self.memoryProxy = ALProxy("ALMemory",ip,port)
        try:
            self._printSoundSets()
            self.faceDetectionProxy = ALProxy("ALFaceDetection",ip,port)
            self.audioDeviceProxy =  ALProxy("ALAudioDevice",ip,port)
            self.landMarkDetectionProxy =  ALProxy("ALLandMarkDetection",ip,port)
        except:
            pass

        self.bodyLanguageMode = "contextual"
        print "*************************"
        print "Available languages: " + str(self.textToSpeechProxy.getAvailableLanguages())
        print "Current language: " + str(self.textToSpeechProxy.getLanguage())
        print "Volume: " +  str(self.textToSpeechProxy.getVolume())
        print
        print "*************************"
    

        
    # ************************************* Robot settings ***************************************************
    def stop_behaviors(self, parameters = {}, in_parallel = False): #0
        """ Function used to stop all behaviors in a robot (useful for Pepper robot)
        """
        try: 
            #self.behavior_service = self.session.service("ALBehaviorManager") #Delete
            #self.behavior_service.stopAllBehaviors() #Delete
            self.behaviorManagerProxy.stopAllBehaviors()
            print "All behaviors finished"
        except:
            print "Error while finishind all behaviors in the robot"

    # ************************************* Motion ***********************************************************
    
    # ----------------------------------- Mode control ----------------------------------------------------- 
    # wake up -> Turn ON movements
    # rest -> Turn OFF movements

    def wake_up(self,  input ="", parameters = {}, in_parallel = False): #0
        """Function used to turn on the motors of NAO, also to makes NAO go to a stand initial position"""

        # Get the services ALMotion & ALRobotPosture.
        motion_service = self.session.service("ALMotion")
        posture_service = self.session.service("ALRobotPosture")

        # Wake up robot (Turn the motors on)
        self.motionProxy.wakeUp()
        self.postureProxy.goToPosture("StandInit", 0.5)
        print "FINISH WAKE_UP"


    def rest(self,  input =  "", parameters = {}, in_parallel = False): #0
        """Function used to turn off the motors of NAO and to makes NAO to go to a rest position (safe position)"""

        # Get the services ALMotion.
        motion_service = self.session.service("ALMotion")

        # Go to rest position
        motion_service.rest()

    # ------------------------------------ Posture control ----------------------------------------------- 
    def posture(self, posture_name,  parameters = {}, in_parallel = False): #1
        """Function used to makes NAO to go to a sit position"""

        try:
            self.postureProxy.goToPosture(posture_name, 0.5) #Satnd, 
        except:
            print "Posture not valid: " + str(posture_name) 
        

    # ------------------------------------ Low abtraction motion control ----------------------------------------------- 
    # Low abstraction = individual joint control (definition)

    def change_joint_value(self,joint_name,  parameters = {}, in_parallel = False): #2
        try:
            value = parameters["value"]
        except: 
            value = 1.0

        useSensors  = True
        sensorAngle = self.motionProxy.getAngles(joint_name, useSensors)
        self.motionProxy.setStiffnesses(joint_name, 1.0)
        angle = sensorAngle[0] + float(value)*almath.TO_RAD
        fractionMaxSpeed = 0.3
        self.motionProxy.setAngles(joint_name,angle,fractionMaxSpeed)
        time.sleep(0.1)



    def open_hand(self,handName,  parameters = {}, in_parallel = False):
        
        if handName == "both":
            
            if in_parallel:
                self.motionProxy.post.openHand("LHand")
                self.motionProxy.post.openHand("RHand")
            else: 
                self.motionProxy.openHand("LHand")
                self.motionProxy.openHand("RHand")
            
        else:
            
            if in_parallel:
                self.motionProxy.post.openHand(handName)
            else: 
                self.motionProxy.openHand(handName)


    def close_hand(self,handName,  parameters = {}, in_parallel = False):

        if handName == "both":
            
            if in_parallel:
                self.motionProxy.post.closeHand("LHand")
                self.motionProxy.post.closeHand("RHand")
            else: 
                self.motionProxy.closeHand("LHand")
                self.motionProxy.closeHand("RHand")
            
        else:
            
            if in_parallel:
                self.motionProxy.post.closeHand(handName)
            else: 
                self.motionProxy.closeHand(handName)

    
    # -------------------------------------  Waliking control ------------------------------------------------- 

    def move_to_position(self, mode , parameters = {}, in_parallel = False): #3

        print "MOVE"
        print mode
        print parameters

        if mode == "position":
            try:
                x = float(parameters["x"])
                y = float(parameters["y"])
                Theta = float(parameters["angle"])
            
                motion_service = self.session.service("ALMotion")
##                self.posture_standInit()

                #####################
                ## Enable arms control by move algorithm
                #####################
                motion_service.setMoveArmsEnabled(True, True)
                #~ motion_service.setMoveArmsEnabled(False, False)

                #####################
                ## FOOT CONTACT PROTECTION
                #####################
                #~ motion_service.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION",False]])
                motion_service.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

                #####################
                ## get robot position before move
                #####################
                initRobotPosition = almath.Pose2D(motion_service.getRobotPosition(False))
                motion_service.setMoveArmsEnabled(False, False)


                X = float(x)
                Y = float(y)
                Theta = Theta*math.pi/180

                if  in_parallel == True:
                    id = motion_service.post.moveTo(X, Y, Theta)
                    # wait is useful because with _async moveTo is not blocking function
                    motion_service.wait(id,0)

                    
                else:   
                    motion_service.moveTo(X, Y, Theta, _async=True)
                    # wait is useful because with _async moveTo is not blocking function
                    motion_service.waitUntilMoveIsFinished()

                #####################
                ## get robot position after move
                #####################
                endRobotPosition = almath.Pose2D(motion_service.getRobotPosition(False))

                #####################
                ## compute and print the robot motion
                #####################
                robotMove = almath.pose2DInverse(initRobotPosition)*endRobotPosition
                # return an angle between ]-PI, PI]
                robotMove.theta = almath.modulo2PI(robotMove.theta)
                print "Robot Move:", robotMove
            except:
                "error WALKING"
                pass
            
        elif mode == "velocity":
                x = float(parameters["x"])
                y = float(parameters["y"])
                theta = float(parameters["angle"])
                frequency = 0.5
                #frequency = parameters["frequency"]
                self.motionProxy.setWalkTargetVelocity(x,y,theta,frequency)

    # ------------------------------------ Move ROMAN ----------------------------------------------- 
    def move_direction(self, mode , parameters = {}, in_parallel = False): #3

        print "MOVE"
        print mode
        print parameters
        
        x = int(parameters["velocity"])/100.
        theta = int(parameters["velocity"])/100.
        y = 0

        if mode == "foward":
            x = x
            y = 0
            theta = 0 

        elif mode == "backward":
            x = -x
            y = 0
            theta = 0 
            
        elif mode == "left":
            x = 0
            y = 0
            theta = theta
             
        elif mode == "right":
            x = 0
            y = 0
            theta = -theta

        elif mode == "stop":
            x = 0
            y = 0
            theta = 0
            
        frequency = 1
        print x, y, theta
        self.motionProxy.setWalkTargetVelocity(x,y,theta,frequency)
##
##     def turn(self, mode , parameters = {}, in_parallel = False): #3
##
##        print "TURN not jet implemente"

    # ------------------------------------ Animation control ----------------------------------------------- 

    def __flip_animation(self,old_keys,old_names,old_times):
        joint2negative = ["HeadYaw","HipRoll"]
        keys = old_keys
        names = old_names
        times = old_times

        for joint_name in joint2negative:
            if joint_name in names:
                index_number = names.index(joint_name)
                temp_keys = keys[index_number]
                keys[index_number] = map(lambda x: x*(-1), temp_keys)


        joints2flip = [["LElbowRoll","RElbowRoll"], ["LElbowYaw", "RElbowYaw"],["LShoulderPitch","RShoulderPitch"], ["LShoulderRoll", "RShoulderRoll"], ["LWristYaw", "RWristYaw"]]
            
        for joint_tuple in joints2flip:
            if joint_tuple[0] in names and joint_tuple[1] in names:
                index_number1 = names.index(joint_tuple[0])
                index_number2 = names.index(joint_tuple[1])

                print joint_tuple
                print keys[index_number1]
                print keys[index_number2]
                
                temp_keys1 = keys[index_number1]
                temp_keys2 = keys[index_number2]

                if joint_tuple[0] == "LShoulderPitch":
                    pass
                else:
                    temp_keys1 = map(lambda x: x*(-1), temp_keys1)
                    temp_keys2 = map(lambda y: y*(-1), temp_keys2)
                
                temp_times1 = times[index_number1]
                temp_times2 = times[index_number2]

                keys[index_number1] = temp_keys2
                keys[index_number2] = temp_keys1
                times[index_number1] = temp_times2
                times[index_number2] = temp_times1

                print keys[index_number1]
                print keys[index_number2]

            print  


        return keys,names,times

    def __invert_time(self,times):
        # Invert diference between motions
        time_dif = []
        new_times = [times[0]]
        time_len = len(times)
        for t in range (time_len-1):
            time_dif.append(times[t+1]- times[t])

        new_time_dif = time_dif[::-1]
        
        for t in range (time_len-1):
            new_times.append(new_times[t]+new_time_dif[t])
        return new_times

    def _animation_query(self,name_animation, flip = False, reverse = False): #1
        """ Get the animation parameters (joint names, times and joint values) of a specific animation from a database"""
        db = TinyDB('database/nao_animation_db.json')
        q = Query()
        try:
            s = db.search(q.animation == name_animation)
        except:
            print (" ERROR: Animation not found in database")
            return False,[0],[0],[0]

        names = [x.encode('UTF8') for x in s[0]['names']] # Name of the joint
        times =  s[0]['times']                            # Time index
        keys =  s[0]['keys']                              # Joint values

        if flip == True:
            keys,names,times = self.__flip_animation(keys,names,times)

        if reverse == True and len(times) > 1 :
            i = 0
            for k in keys:
                temp = k[::-1]
                keys[i] = temp
                i = i + 1
            i = 0
            for time in times:
                times[i] = self.__invert_time(time)
                i = i + 1                
        return True, names, times, keys

        



    def _change_animation_duration(self, time_list, new_max):
        """ Change the timeline values to other specified by the user
        """
        
        l = len(time_list)
        time_base = time_list[0]
        max_time = float(time_base[-1])
        factor = float(new_max)/max_time
        for lista in time_list:
            for index, item in enumerate(lista):
                lista[index] = lista[index]*factor
        
        return time_list



        
    
    # This function will be executed in parallel with the main program
    def save_motion(self, name_file, parameters = {},in_parallel = False ):
        samples = parameters["samples"]
        time_w = float(parameters["time"])/1000.
        path = os.getcwd()
        file_n = name_file + ".txt"
        self.data2save = {}
        for name in self.name_joints:
            self.data2save[name] = []
            
        for n in range(int(samples)):
            
            angles = self.motionProxy.getAngles(self.name_joints, False)
            print n
            i = 0
            for joint in self.name_joints:
                self.data2save[joint].append(angles[i])
                i = i + 1
            time.sleep(time_w)

        with open(file_n, 'w') as outfile:
            json.dump(self.data2save, outfile)
        print "++++++++++++++++++ MOTION SAVED ++++++++++++++++++++"
        print "In file: " + path + "/"+ file_n
        



    def animation(self, animation_name, parameters = {}, in_parallel = False): #1
        """ Execute a animation saved in the database
        """
            
        names = list()
        times = list()
        keys = list()

        flip = False
        reverse = False

        if "flip" in parameters:
            flip = parameters["flip"]
        if "reverse" in parameters:
            reverse = parameters["reverse"]
 
        success, names, times, keys = self._animation_query(animation_name, flip, reverse)
        self.name_joints = names

        if success:

##            if "save" in parameters:
##                self.data2save = {}
##                self.saving = True
##                for name in names:
##                    self.data2save[name] = []
##                # --------- In main thread ---------------   
##                # Here we define which function will be executed in parallel
##                save_thread = threading.Thread(target = self.get_angles_from_motions)
##                # This avoid that the parallel task follows running after closing the main task
##                save_thread.daemon = True
##                # Here we start the parallel task
##                save_thread.start()            
            

            if "time" in parameters:
                times =  self._change_animation_duration(times,float(parameters["time"]))

            try:
                if in_parallel:
                    id = self.motionProxy.post.angleInterpolation(names, keys, times, True)
                    self.saving = False
                else:
                    self.motionProxy.angleInterpolation(names, keys, times, True)
                    self.saving = False
                    
            except BaseException, err:
                print (err)
        else:
            print ('Animation not found in database')
        print "FINISH ANIMATION"


    # *********************************** Robot sound/say ******************************************

    def _printSoundSets(self): #0
        """ Display soundset infromation
        """
        self.aup = ALProxy("ALAudioPlayer",  self.ip, self.port)
        lista = self.aup.getInstalledSoundSetsList()
        print ("Soundset files installed:" + str(lista))
        for l in lista:
            print ("Sound files in soundsets " + str(l) + ": " + str(self.aup.getSoundSetFileNames(l)))
        

        
    def play_sound(self,sound_name, parameters = {}, in_parallel = False): #2
        """ Play a SoundSet if installed in the robot
        """
        soundSet_name = "sounds"
        try:
            self._printSoundSets()
            self.aup = ALProxy("ALAudioPlayer",  self.ip, self.port)
            if in_parallel:
                self.aup.post.playSoundSetFile(soundSet_name,sound_name)
            else:
                self.aup.playSoundSetFile(soundSet_name,sound_name)
        except:
            print (sound_name + " non found in *"+ soundSet_name + "* SoundSet file in the robot")

    def set_double_voice(self,value): #1
            if(value > 100):
                value = 100
            if(value < 0):
                value = 0

            map_value =  value*4/100
            self.textToSpeechProxy.setParameter("doubleVoiceLevel",  map_value)
            print "voice changed doubleVoice" + str(value)
    
    def set_voice_pitch(self,value): #1
            if(value > 100):
                value = 100
            if(value < 0):
                value = 0

            map_value =  value*4/100
            self.textToSpeechProxy.setParameter("pitchShift", map_value)
            print "voice changed pitch" + str(value)

    def set_volume(self,value): #1
            #self.textToSpeechProxy.setVolume(value)
            try:
                if(value > 100):
                    value = 100
                if(value < 0):
                    value = 0
                self.audioDeviceProxy.setOutputVolume(value) 
                print "voice changed volume " +  str(value)
            except:
                pass

    def set_voice_speed(self,value): #1


            if(value > 400):
                value = 400
            if(value < 50):
                value = 50

            map_value = 50 +  value*350/100

            self.textToSpeechProxy.setParameter("speed", value)
            print "voice changed speed " +  str(value)



    def say(self, some_text, parameters = {}, in_parallel = False): #2
        """ Function used to say a simple text without movement
            :param some_text:  text to be say for the robot
            :param language: select the language to speech, Example: French or Japanese. English is by default
        """

        language = "English"
        some_text = some_text.encode("utf-8")
        try:
            language = parameters["language"]

        except:
            pass

        if(self.language == language):
                pass
        else:
            try:
                self.textToSpeechProxy.setLanguage(language)
                self.language = language
            except:
                print ("Language" + str(language) + "not avaliable")

        if in_parallel:
            self.textToSpeechProxy.post.say(some_text)
        else:
            self.textToSpeechProxy.say(some_text)
            
        print some_text, ", was said by the robot"

    def say_contextual(self, some_text, parameters = {}, in_parallel = False): #2
        """ Function used to say a text + a robot gesture
            :param some_text:  text to be say for the robot
            :param type_gesture:  definition of the type of gesture (in this moment only contextual)
            :param language: select the language to speech, Example: French or Japanese. English is by default
        """
        language = "English"
        some_text = some_text.encode("utf-8")
        try:
            language = parameters["language"]

        except:
            pass

        if(self.language == language):
            pass
        else:
            try:
                self.textToSpeechProxy.setLanguage(language)
                self.language = language
            except:
                print ("Language" + str(language) + "not avaliable")

        self.animatedSpeechProxy.say(some_text,{"bodyLanguageMode":"contextual"})


    # ****************************** Tracking actions ***************************************
    def track_face(self, enable = True, parameters = {}, in_parallel = False):
        self.faceDetectionProxy.enableTracking(tracking_enabled)
        # Just to make sure correct option is set.
        print "Is tracking now enabled on the robot?", faceProxy.isTrackingEnabled()


    # ****************************** Emergent primitives ***************************************
    # Composed of 2 o more primitves, example: imitation = animation + sound playing

    def imitation(self, animation_name, parameters = {}, in_parallel = False): #2
        """Animation + sound"""
        print ("*** Animation details: *** \n")
        print ("name:" + str(animation_name))
        self.play_sound(animation_name, parameters, True)
        print ("Sound request in parallel done")
        self.animation(animation_name, parameters, True)
        print ("Animation request done")


    def executeActionPrimitive(self,name,input_, parameters = {}, in_parallel = False): #1
        try:
            func = getattr(self, "method")
        except AttributeError:
            print "Method/Primitive not found in the API of this robot"
        else:
            func(input_)



if __name__ == "__main__":
    import doctest
    doctest.testmod()
