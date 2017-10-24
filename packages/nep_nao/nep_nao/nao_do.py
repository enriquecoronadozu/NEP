# -*- encoding: UTF-8 -*-
#!/usr/bin/env python

# ------------------------ NAO action class --------------------------------
# Description: NAO/Pepper functions used to perform some predefined actions
# this class use the NAO SDK
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


#TODO:
# Add more postures, see: http://doc.aldebaran.com/1-14/naoqi/motion/alrobotposture.html
# Also motion_service and posture service can be global with self?

import qi
import sys
from tinydb import TinyDB, Query
import re
import ast
import json
from nep_nao import*
from naoqi import ALProxy
import math
import almath

        

class nao_do():
    """ NAO/Pepper functions used to perform some predefined actions of movement
        :param ip:  Robot IP
        :param port: Robot port for comunication
    """
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.session = qi.Session()
        self.connection()



    def animation_query(self,name_animation):
        db = TinyDB('database/nao_animation_db.json')
        q = Query()
        try:
            s = db.search(q.animation == name_animation)
            names = [x.encode('UTF8') for x in s[0]['names']]
            times =  s[0]['times']
            keys =  s[0]['keys']
    
            return 1, names, times, keys
        
        except:
            print (" ERROR: Animation not found in database")
            return 0,[0],[0],[0]


    def animation(self, animation_name):

        names = list()
        times = list()
        keys = list()
 
        success, names, times, keys = self.animation_query(animation_name)
        try:
            motion_service = self.session.service("ALMotion")
            motion_service.angleInterpolation(names, keys, times, True)
        except BaseException, err:
            print (err)
            print ('Animation not found')


    def StiffnessOn(self,proxy):
        # We use the "Body" name to signify the collection of all joints
        pNames = "Body"
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


    def walk_to(self,x,y,Theta):

        motion_service = self.session.service("ALMotion")
        self.posture_standInit()

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

        X = float(x)
        Y = float(y)
        Theta = Theta*math.pi/180
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


    def get_sound_options(self):
        self.aup = ALProxy("ALAudioPlayer",  self.ip, self.port)
        lista = self.aup.getLoadedSoundSetsList()
        print "Sound type list:" + str(lista)
        for l in lista:
            print "sound files in " + str(l) + ": " + str(self.aup.getSoundSetFileNames(l))
        
                

    def sound(self,type_sound, sound):

        self.aup = ALProxy("ALAudioPlayer",  self.ip, self.port)
        self.aup.post.playSoundSetFile(type_sound,sound)
        self.get_sound_options()
    
    def imitation(self, animation_name, type_sound, sound):
        """Animation + sound"""
        print ("say")
        print ("*** Animation details: *** \n")
        print ("name:" + str(animation_name))
        print ("type_sound:" + str(type_sound))
        print ("sound:" + str(sound))

        self.sound(type_sound, sound)
        self.animation(animation_name)
        
                

    # TODO make Private
    def connection(self):
        """Function used to connect the robot, is used always before that perform an action"""

        try:
            self.session.connect("tcp://" + self.ip  + ":" + str(self.port))
        except RuntimeError:
            print ("Can't connect to Naoqi at ip \"" + self.ip + "\" on port " + str(self.port) +".\n"
                   "Please check your script arguments. Run with -h option for help.")
            sys.exit(1)


    def posture_standInit(self):
        """Function used to turn on the motors of NAO, also to makes NAO go to a stand initial position"""

        # Get the services ALMotion & ALRobotPosture.
        motion_service = self.session.service("ALMotion")
        posture_service = self.session.service("ALRobotPosture")

        # Wake up robot (Turn the motors on)
        motion_service.wakeUp()

        posture_service.goToPosture("StandInit", 0.5)



    def posture_stand(self):
        """Function used to turn on the motors of NAO, also to makes NAO go to a stand initial position"""

        # Get the services ALMotion & ALRobotPosture.
        motion_service = self.session.service("ALMotion")
        posture_service = self.session.service("ALRobotPosture")

        # Wake up robot (Turn the motors on)
        motion_service.wakeUp()

        # Send robot to Stand 
        posture_service.goToPosture("Stand", 0.5)



    def posture_rest(self):
        """Function used to turn off the motors of NAO and to makes NAO to go to a rest position (safe position)"""

        # Get the services ALMotion.
        motion_service = self.session.service("ALMotion")

        # Go to rest position
        motion_service.rest()


    def posture_sit(self):
        """Function used to makes NAO to go to a sit position"""

        # Get the services ALRobotPosture.
        posture_service = self.session.service("ALRobotPosture")

        # Send robot to Stand Init
        posture_service.goToPosture("Sit", 0.5)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
