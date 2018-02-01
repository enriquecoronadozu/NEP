#!/usr/bin/env python

# ------------------------ Behavior class --------------------------------
# Description: Main behavioral class
# --------------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga
import nep
import time
import threading
            
class interaction():

    def __init__(self):
        
        
        self.node = nep.node("executor")
        conf = self.node.conf_pub(mode= "many2many")
        self.pub = self.node.new_pub("/action_request", conf)
        conf = self.node.conf_sub(mode= "many2many")
        self.sub = self.node.new_sub("/action_response", conf)
        conf = self.node.conf_sub(mode= "one2many") 
        self.exit_sub  = self.node.new_sub("/program_execution", conf)
            
        #New thread that can de used to stop the program
        self.exit = threading.Thread(target = self._wait_kill)
        # Used to finish the background thread when the main thread finish
        self.exit.daemon = True
        # Start new thread 
        self.exit.start()
            
        """except:
            # TODO change to client-server maybe or SURVEY or simplify message in a helper function 
            print "WARNING: Another cognitive node have been launched, please stop the execution of that node first"
            time.sleep(2)
            self.node = nep.node(self.node_name)
            pub_config = self.node.conf_pub(mode = "many2one")
            self.status_pub = self.node.new_pub(self.topic_node_status, pub_config) 
            # Send message to the node supervisor, node already open
            status_message = {'node_type':self.node_name, 'node_status':"error", 'description':"already_open"}
            print status_message
            self.status_pub.send_info(status_message)
            import sys
            sys.exit()"""

    def _wait_kill(self):
        """Listen for kill signal of the program"""
        s, data = self.exit_sub.listen_info(True)
        if s == True:
            print "************* Signal to stop program **************"
            print data
            import os
            pid = os.getpid()
            print pid
            import subprocess as s
            s.Popen('taskkill /F /PID {0}'.format(pid), shell=True)



    """def do_action(self,action, robots, parameters = {}):
        action_ = action[0]
        input_ =  action[1]
        new_action = [{"action":action_, "input": input_, "parameters": parameters}]
        self.run(new_action,robots)"""

    #Final 
    def new_action(self, do_primitives, with_robot, run = True):
        list_of_actions = []
        action =  ""

        if not bool(do_primitives):
            print ("No primitives avaliable")
        else:
            action = self.create_action(do_primitives,with_robot)
            if run == True:
                self.run(action)
        print action
        return action 

    def create_action(self, primitives, robots):
        if type(primitives) is list:
            message = {"action":primitives, "robots":robots}
        else:
            message = {"action":[primitives], "robots":robots}
            
        return message

    def new_group(self, actions, type_ = "parallel", run = False):
        pass

    #Delete?
    def actions2message(self,actions,robots,parameters = {}):
        list_of_actions = []
        message = ""
        actions_description = ""
        if type(actions[0]) is list: # Set of actiosn in parallel
            for action in actions:
                action_ = action[0]
                input_ =  action[1]
                new_action = {"action":action_, "input": input_, "parameters": parameters}
                list_of_actions.append(new_action)
            actions_description = list_of_actions
        else:
            action_ = actions[0]
            input_ =  actions[1]
            actions_description = [{"action":action_, "input": input_, "parameters": parameters}]

        message = {"actions":actions_description, "robots":robots}
        return message

        

    """def do_parallel_actions(self,actions, robots, parameters = {}):
        list_of_actions = []

        if not bool(actions):
            print ("Null list")
            pass
        else:
            
            if type(actions[0]) is list: # Set of actiosn in parallel
                for action in actions:
                    action_ = action[0]
                    input_ =  action[1]
                    new_action = {"action":action_, "input": input_, "parameters": parameters}
                    list_of_actions.append(new_action)
                self.run(list_of_actions,robots)
            else: # Only one action
                self.do_action(actions, robots, parameters = {})"""


    def do_parallel_actions(self, actions,  parameters = {}, robots = "nao", run = True):
        list_of_actions = []
        message =  ""

        if not bool(actions):
            print ("Null list")
            pass
        else:
            message = self.actions2message(actions, robots, parameters)
            if run == True:
                self.run(message)
        return message   

    def run(self, message):
        print "ACTION execution:"
        #robot_actions = {"actions":actions, "robots":robots}
        print message
        self.pub.send_info(message)
        robots =  []
        if type(message['robots']) is list:
            robots = robots + message['robots']
        else:
            robots = robots + [message['robots']]
        self.wait_response(robots) 

    def run_sequence(self, actions):
        if type(actions) is list:
            for msg in actions:
                self.run(msg)
        elif type(actions) is dict:
                self.run(actions)
        print ("sequence fisheched")
               

    def at_same_time(self, list_actions_1, list_actions_2):
        
        #New thread for repeating actions
        self.t_actions1 = threading.Thread(target = self.run_sequence, args = (list_actions_1,))
        self.t_actions2 = threading.Thread(target = self.run_sequence, args = (list_actions_2,))
        # Used to finish the background thread when the main thread finish

        # Start new thread 
        self.t_actions1.start()
        self.t_actions2.start()
        # Wait until both are finished
        self.t_actions1.join()
        self.t_actions2.join()
        print("same finished")

    def repeat_actions(self,list_actions):
        while not self.exit_repeat:
            run_sequence(list_actions)
           
        
    """def repeat_until_action(self, message_continue, messages_repeat):
        robots = []
        self.exit_repeat = False

        #New thread for repeating actions
         self.t_actions1 = threading.Thread(target = self.run_sequence, args = (list_actions_1,))
        # Used to finish the background thread when the main thread finish
         self.t_actions1.daemon = True
        # Start new thread 
        self.t_actions1.start()

        for msg in message_continue:
            self.pub.send_info(msg)
            if type(msg['robots']) is list:
                robots = robots + msg['robots']
            else:
                robots = robots + [msg['robots']]
        self.wait_response(robots)
        self.exit_repeat = True
        #Wait until finished the anothe threads
        self.t_repeat.joint()"""

    def repeat_until_trigger(self, trigger, messages_repeat):
        robots = []
        self.exit_repeat = False

        #New thread for repeating actions
        self.t_repeat = threading.Thread(target = self._wait_kill, args = (messages_repeat,))
        # Used to finish the background thread when the main thread finish
        self.t_repeat.daemon = True
        # Start new thread 
        self.t_repeat.start()
        self.exit_repeat = False

        while not self.exit_repeat:
            s, msg = sub_human_state.listen_info()
            if s:
                if msg["human_state"] == trigger:
                    self.exit_repeat = True

        self.t_repeat.joint()
        

    def wait_response(self, robots):
        new_robot_list = robots[:]

        print ("Waiting for response of " + str(new_robot_list))
        while len(new_robot_list) > 0:
            success, state = self.sub.listen_info(False)
            if success:
                robot = str(state["robot_name"]) 
                result = str(state["execution_state"])
                print ("Action performed by " + robot + " with: " + result + " ")
                if robot in new_robot_list:
                    new_robot_list.remove(robot)
                    if new_robot_list != []:
                        print ("Robots left: " + str(new_robot_list) )
            time.sleep(.001)
                                
        return True


if __name__ == "__main__":
    import doctest
    doctest.testmod()

                                
