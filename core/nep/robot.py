#!/usr/bin/env python

# ------------------------ Communication module ---------------------------
# Description: Set of classes used for simplify the use of ZeroMQ
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


from nep import*
import time
import random
import threading
# -*- coding: utf-8 -*-

#delete
from speech_to_text import*

#TODO set languaje of the robot

#robot dictionaries, topic, ip and port definitions for the action engine.

class robot():
    """Robot independent social primitives orchestration class. This class works as a bridge between the social behaviors specified by the user/programmer, in a high level control script, and the robot behavior execution engines.
    
    First, the user must create the high level  control script using the Google Blockly based Web Interface (which generate a Python script) or using a Python script.
    
    This class will request for the execution of a specific behavior to the execution engines of the robot selected. The behavior to be executed are encoded in python dictionary and then sended to the execution engine using the ``run_action()`` function. After a execution request, the program will block until the execution of the requested action is performed. This is done using the ``wait_for_execution()`` function.
    
    """
    def __init__(self):
        
        print "Starting new robot instance ..."
        
        self.robot_ip = '127.0.0.1' # We are considering that the robots controler always connect with the action engine in local host
        self.robot_request_port =  '2020' # The port to talk with the robot engine is always 2020, to use multiple robots we change the name of the topic
        self.execution_response_port = '2021' # The port to listen the robot engine is always 2021, to use multiple robots we change the name of the topic

        try:
            #New thread that can de used to stop the program
            self.exit = threading.Thread(target = self.wait_kill)
            self.exit_sub =  subscriber("/program_execution", False)
            #Used to finish the background thread when the main thread finish
            self.exit.daemon = True
            self.exit.start()

            #Publisher for all the robots
            self.pub = publisher("/action_request")
            # Subcribe to robot responses
            self.sub = subscriber("/action_execution", False)
            self.with_robots = ["NAO"]
        except:
            print "Another main execution node have been launched"
            
            status_pub = publisher("/node_status", False)
            status_message = {'node_type':"main_code", 'node_status':"error", 'description':"busy"}
            print status_message
            status_pub.send_info(status_message)
            import sys
            sys.exit()


    def wait_kill(self):
        """Listen for kill signal of the program"""
        data = self.exit_sub.listen_string()
        import os
        pid = os.getpid()
        print pid
        import subprocess as s
        s.Popen('taskkill /F /PID {0}'.format(pid), shell=True)

    def setRobots(self,robots):
        self.with_robots = robots

    # Robot actions -------------------------
    def run_action(self,message):
        """  Function that send the request of a robot action execution. This request send a python dictionary with the description of such action. 
            Parameters
            ----------
            message : dictionary
                Robot action description.
            Returns
            -------
            result : string
                Execution result, such as "success" or "error".
                
            Example
            -------
            >>> # Here the an action of text to speech  is specified. 
            >>> message = {'action': 'say', 'text': 'hello', 'gesture': 'no_gesture', 'to_person': 'no_person' }
            >>> run_action(message)
        """
        success = False

        # Request and action execution
        print
        print ("Request of execution to ***" + str(self.with_robots) + "*** robot")

        if type(self.with_robots) == str:
            self.pub.send_info(message, debug=True)
            # Wait until execution finished and get the result

            try:
                print ("Waiting for response of " + str(self.with_robots))
                result = ""

                while True:
                    success, state = self.sub.listen_info(False)
                    if success:
                        robot = str(state["robot_name"]) 
                        result = str(state["execution_state"])
                        if robot == self.with_robots:
                            print ("Execution performed by " + robot + " with:" + result)
                            return result
            except:
                print "Error receiving response"
                return "error"

        if type(self.with_robots) == list:
            for robot in self.with_robots:
                self.pub.send_info(message, debug = True)
            self.wait_response(self.with_robots)


    def wait_response(self, robots):
            new_robot_list = robots[:]

            try:
                print ("Waiting for response of " + str(new_robot_list))
                while len(new_robot_list) > 0:
                    success, state = self.sub.listen_info(False)
                    if success:
                        robot = str(state["robot_name"]) 
                        result = str(state["execution_state"])
                        print ("Execution performed by " + robot + " with:" + result)

                        if robot in new_robot_list:
                            new_robot_list.remove(robot)
                            
                return True
            except:
                print "Error receiving response"
                return False

        
    def say(self,text,gesture,to_person,language):
        """  Robot text to speech action definition. This function create the python dictionary to be send to the execution engines.

            Parameters
            ----------
                text : string 
                    Text to be said for the robot.

                gesture : string 
                    Type of gesture that will be performed when the robot speaks. 
                
                to_person : string
                    Specify an action of gaze to an speficic person. TODO: define the persons.
                    
                language: string
                    Set the languge that the robot can speak

                
            Returns
            -------
            result :string
                Execution result, can be "success" or "error".
        """
        message = {'action': 'say', 'text': text, 'gesture': gesture, 'to_person': to_person, 'language':language }
        return self.run_action(message)

    
    def setVoice(self, speed , volum , pitch , doubleVoice ):
        message = {'action': 'setVoice', 'speed':speed, 'volum':volum, 'pitch':pitch, 'doubleVoice':doubleVoice }
        return self.run_action(message)


    def do(self,action):
        """ This function create a python dictionaty with the description of the action to be performed by the robot. This function is to define simple actions that does not needs the especification of some parameters. Can be used for example for send to the robot to the initial position or to end and interaction.

            Parameters
            ----------
            action : string 
                Simple action to do

            
            Returns
            -------
            result : string
                Execution result, can be "success" or "error".

        """
        message = {'action': action}
        return self.run_action(message)

    def do_gesture(self, gesture_name):
        """ This function create a python dictionaty with the description of the gesture to be performed by the robot.

            Parameters
            ----------
            
            gesture_name : string
                Name of the gesture to be performed

            with_robot: string
                Name of the robot that will execute the requested behavior. This name represent the name of the topic to be used.
            
            Returns
            -------
            
            result : string
                Execution result, such as "success" or "error".
        """
        message = {'action': "gesture", 'animation': gesture_name }
        return self.run_action(message)


    def doImitation(self, imitation_name, with_sound = "default"):
        """ This function create a python dictionaty with the description of the animation and sound to be performed by the robot.

            Parameters
            ----------
            
            thing2imitate : string
                Name of the imitation to perform

            Returns
            -------
            
            result : string
                Execution result, such as "success" or "error".
        """

        if(imitation_name) == "final":
             with_movement = "final"
             with_sound = "final"
             type_imitation = "final"

        if(imitation_name) == "preparation":
             with_movement = "preparation"
             with_sound = "preparation"
             type_imitation = "preparation"

        if(imitation_name) == "bored":
             with_movement = "bored"
             with_sound = "bored"
             type_imitation = "animals"

        if(imitation_name) == "wait":
             with_movement  = "wait"
             with_sound = "wait"
             type_imitation = "animals"

        if(imitation_name == "elephant"):
            with_movement = "elephant"
            with_sound = "elephant"
            type_imitation = "animals"

        if(imitation_name == "monkey"):
            with_movement = "monkey"
            with_sound = "monkey"
            type_imitation = "animals"

        if(imitation_name == "kenshiro"):
            with_movement = "kenshiro"
            with_sound = "hokuto"
            type_imitation = "animals"

        if(imitation_name== "cat"):
            with_movement = "cat"
            with_sound = "nya"
            type_imitation = "animals"

        if(imitation_name == "crow"):
            with_movement = "crow"
            with_sound = "crow"
            type_imitation = "animals"

        if(imitation_name == "disco"):
            with_movement = "disco"
            with_sound = "disco"
            type_imitation = "music"

        if(imitation_name == "guitar"):
            with_movement = "guitar"
            with_sound = "guitar"
            type_imitation = "music"

        if(imitation_name == "saxophone"):
            with_movement = "saxophone"
            with_sound = "saxophone"
            type_imitation = "music"

        if(imitation_name == "karate"):
            with_movement = "karate"
            with_sound = "karate"
            type_imitation = "music"

        if(imitation_name == "hand_up"):
            with_movement = "hand_up"
            with_sound = "hand_up"
            type_imitation = "music"


        if(imitation_name == "bow"):
            with_movement = "bow"
            with_sound = "bow"
            type_imitation = "music"

            
                
        message = {'action': "imitation", 'animation': imitation_name, 'sound': with_sound}
        return self.run_action(message)
     

# In testing phase ...................................................................................................................  

    def count (self,number,gesture,to_person = "no_person", language = "English"):
        """ Robot count definition (text to speech of the time that an action have been performed).

            Parameters
            ----------
            
            gesture : string
                Type of gesture that will be performed when the robot speaks. 
            
            number : int
                Specify the number to count

            Returns
            -------
            result : string
                Execution result, can be "success" or "error".
        
        """
        m = memory()
        text = m.select_message_for_count(number,'en')
        message = {'action': 'say', 'text': text, 'gesture': gesture, 'to_person': to_person, 'language':language}
        return self.run_action(message)


    def walk_to(self,x,y,theta):
        message = {'action': 'walk', 'x': x, 'y': y, 'theta': theta}
        return self.run_action(message)
        


    #TODO, data base 
    
    

    # Robot perception -----------------------
    # TODO: Improve or delete, documentation
    def listen (self, type_action, language = "en-US"):
        # listen and recognize response
        node = listen_node()
        text = node.recognize_speech(language)
        print text
        list_words = text.split(" ")
        meaning_response = "unknown"
        for word in list_words:
          if (word == "si"):
            meaning_response = "yes"
            return meaning_response
          if (word == "no"):
            meaning_response = "no"
            return meaning_response
        return meaning_response
    
class memory():
    """  Robot simple memory class. It is used for simple task such as count
    """
      
    def increase_counter(self,human_action,count_actions):
        """ Increase the value of a couter  

        Parameters
        ----------
        human_action : string
            Name of the input human action to count 

        count_actions : dictionary
            Dictionary of possible human actions to count 
          
        Returns
        -------
        
        count_actions : dictionary
            Update of the dictionary of human actions

        times : int
            Times that the specific human action was performed.
        
        """

        # If the input human action is in the dictionary of actions
        if human_action in count_actions:
              #Increase the counter of the input human action
            count_actions[human_action] = count_actions[human_action] + 1  
        else:
              #If the input action is a new action to count, then add this action to the dictionary of actions.
            count_actions[human_action] = 1
            
        return count_actions, count_actions[human_action]

    #TODO: more specific, count maybe times, objects, apples, ...
    def select_message_for_count(self, counter_value, language = 'en'):
        """ This function create a sentence for a count action. You need to specify a number to count and the lenguaje.

        Parameters
        ----------
        counter_value : int
            Number to be counted

        lenguage : string 
            Select "en" to select english, ``es`` for spanish, ``jp`` for japanesse, ``it`` for italian, ``fr`` for french
          
        Returns
        -------

        text_to_say : string 
            Complete text to be saud for the robot
        """
        #TODO: we need to create something in which the user can define this phrases or we can read this phrases from a file
        starting_phases = ["you complete the excersice", "nice, you complete the excersice" , "good, ", "you are doing well, "]
        text_to_say = ''
        start = random.choice(starting_phases)
        if language == 'en':
            if counter_value == 1:
                text_to_say = str(counter_value)
            else:
                text_to_say = str(counter_value)
        

        return text_to_say

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    

