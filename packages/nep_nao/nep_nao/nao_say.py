# -*- encoding: UTF-8 -*-

# ------------------------ NAO say class --------------------------------
# Description: NAO functions used to make NAO talk
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


import qi
import sys
import random
from naoqi import ALProxy

class nao_say():
    """ NAO functions used to make NAO talk
        :param ip:  Robot IP
        :param port: Robot port for comunication
    """
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.session = qi.Session()
        #Start NAO speech classes and connect the robot
        print "NAO say starting ..."
        self.connection()
        self.language = "English"

        self.setVoice(100,1,1,2)
        

    # Make private
    def connection(self):
        """Function used start NAO speech classes and connect the robot"""

        try:
            self.tts = ALProxy("ALTextToSpeech", self.ip, self.port)
            self.animatedSpeechProxy = ALProxy("ALAnimatedSpeech", self.ip, self.port)
            self.configuration = {"bodyLanguageMode":"contextual"}
            print "**** NAO say started **** "
            print
            print "Available languages: " + str(self.tts.getAvailableLanguages())
            print "Current language: " + str(self.tts.getLanguage())
            print "Volume: " +  str(self.tts.getVolume())
            print
            print "*************************"


            
        except RuntimeError:
            print ("Can't connect to Naoqi at ip \"" + self.ip + "\" on port " + str(self.port) +".\n"
                   "Please check your script arguments")
            sys.exit(1)

    def setDoubleVoice(self,value):
            if(value > 4):
                value = 4
            if(value < 0):
                value = 0
            self.tts.setParameter("doubleVoiceLevel", value)
            print "voice changed doubleVoice" + str(value)
    
    def setPitchShift(self,value):
            if(value > 4):
                value = 4
            if(value < 1):
                value = 1
            self.tts.setParameter("pitchShift", value)
            print "voice changed pitch" + str(value)

    def setVolume(self,value):
            if(value > 2):
                value = 2
            if(value < 0.01):
                value = 0.01
            self.tts.setVolume(value)
            print "voice changed volume " +  str(value)

    def setSpeed(self,value):
            if(value > 400):
                value = 400
            if(value < 50):
                value = 50
            self.tts.setParameter("speed", value)
            print "voice changed speed " +  str(value)

    def setVoice(self,speed,volume,pitch,dvoice):
        self.speed = speed
        self.pitch = pitch
        self.volum = volume
        self.dvoice = dvoice
        self.change_request = True

    def changeVoice(self):
        self.setDoubleVoice(self.dvoice)
        self.setSpeed(self.speed)
        self.setPitchShift(self.pitch)
        self.setVolume(self.volum)


    def without_moving(self, some_text, language = "English"):
        """ Function used to say a simple text without movement
            :param some_text:  text to be say for the robot
            :param language: select the language to speech, Example: French or Japanese. English is by default
        """

        if(self.language == language):
                pass
        else:
            self.tts.setLanguage(language)
            self.language = language
            self.changeVoice()

        if(self.change_request == True):
            self.change_request = False
            self.changeVoice()
        
        self.tts.say(some_text)

    def with_gesture(self, some_text, type_gesture = "contextual" ,language = "English"):
        """ Function used to say a text + a robot gesture
            :param some_text:  text to be say for the robot
            :param type_gesture:  definition of the type of gesture (in this moment only contextual)
            :param language: select the language to speech, Example: French or Japanese. English is by default
        """

        if(self.language == language):
            pass
        else:
            self.tts.setLanguage(language)
            self.language = language
            self.changeVoice()

        if(self.change_request == True):
            self.change_request = False
            self.changeVoice()


        if(type_gesture == "contextual" ):
            self.animatedSpeechProxy.say(some_text,self.configuration)




if __name__ == "__main__":
    import doctest
    doctest.testmod()
