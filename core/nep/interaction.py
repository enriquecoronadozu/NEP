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
import nepki
            
class interaction():

    def __init__(self):

        """
        Class used to execute the robot behaviors in base the human and environment states.

        """

        # ------------------------- Connect all the needed nodes -----------------------
        success = False        
        try:
            
            self.node = nep.node("/robot_interaction")

            # ----------------------- Action request publisher -----------------------------
            # We uses one2many, therefore only one program can be runned at the same time
            # In this way we can also detect when a program is already running
            conf = self.node.conf_pub(mode= "one2many") 
            self.pub = self.node.new_pub("/action_request", conf)

            # ---------------------- Action response subscriber ----------------------------
            # Responses from several robots can be read only for this node 
            conf = self.node.conf_sub(mode= "many2one")
            self.sub = self.node.new_sub("/action_response", conf)
            success = True

        except:
            
            print "WARNING: Another cognitive node have been launched, please stop the execution of that node first"
            time.sleep(2)
            pub_config = self.node.conf_pub(mode = "many2one")
            self.status_pub = self.node.new_pub("/node_status", pub_config) 
            # Send message to the node supervisor, node already open
            status_message = {"node":"action", "state":"running"}
            self.status_pub.send_info(status_message)
            import sys
            sys.exit()

        if success:
            
            # ---------------------- Program stop execution ----------------------------
            # Only the Python server can stop a program
            conf = self.node.conf_sub(mode= "one2many") 
            self.exit_sub  = self.node.new_sub("/program_execution", conf)
        
            # ------------------------- Working memory client -----------------------------------
            # TODO: simplify this.
            print "Connect to memory server"
            self.working_memory_port = "7100"
            self.working_memory_client = nep.client("127.0.0.1", self.working_memory_port, transport = "ZMQ")
            self.execute = True

            # --------------------------- Actions Surveyor  -----------------------------
            # TODO: simplify this.
            deadline = 2000
            self.sur = nep.surveyor('127.0.0.1',"9080",deadline)
            time.sleep(1)

            # ------------------------- Kill thread ------------------------------------
            #Thread that can de used to stop the program
            #self.exit = threading.Thread(target = self.__wait_kill)
            # Used to finish the background thread when the main thread finish
            #self.exit.daemon = True
            # Start new thread 
            #self.exit.start()
        

    # TODO:delete        
    # ----------------------- Kill thread ------------------------------
    # Used to kill the current program
    def __wait_kill(self):
        """Listen for kill signal of the program"""
        s, data = self.exit_sub.listen_info(True) # Operation in blocking mode
        if s == True:
            print "************* Signal to stop program **************"
            print data
            import os
            pid = os.getpid()
            print pid
            import subprocess as s
            s.Popen('taskkill /F /PID {0}'.format(pid), shell=True)

    # ----------------------- Check condition ------------------------------
    def check_condition(self,condition):
        """
        Ask to the shared blackboard (SHARO) about the state of some condition. This function returns "success" if the condition is True, otherwise the function returns "failure".

        Parameters
        ----------
        condition : dictionary
            Condition to be cheked. Use the format {"node":"condition","primitive":<primitive>, "input":<state>}


        Returns
        ----------

        result : string
            Returns "success" if the condition is True, otherwise returns "failure".

        """
        
        type_state = condition["primitive"] 
        state  =  condition["input"]
        self.working_memory_client.send_info({'type_state':type_state, 'state':state })
        response = self.working_memory_client.listen_info()
        if response['detected']  == True:
            return "success"
        else:
            return "failure"

    # ------------- New action -----------------
    def new_action(self, primitives, robots):
        """
        Create a new action node


        Parameters
        ----------
        primitives : dictionary
            primitive or list of primitives that creates a composite action

        robot : list 
            robot name of list of robot names to execute the action
            
        Returns
        ----------
        action : dictionary
            Action description

        """
        list_of_actions = []
        action =  ""

        if not bool(primitives) and not bool(robots):
            print ("Primitives or robot not filled")
        else:
            action = nepki.action(primitives, robots)
            if self.execute == True:
                self.run(action)
        return action

    # ------------- Send request -----------------
    def research(self,action):
        """
        Send a request of execution or research of an action using the survey pattern

        Parameters
        ----------
        action : dictionary
            action node to be executed

            
        Returns
        ----------
        response : string
            State of the action execution

        """
        self.sur.send_info(action)
        s, msg = self.sur.listen_info()
        if s:
            response = msg["node"]
            return response
        else:
            print "ERROR: not response from robot"
            return "error"
                    



    def reaction(self,primitive,list_actions):
        new_reaction = {"condition":primitive, "actions":list_actions}
        return new_reaction


    def reactive(self,reactions,repeat = "one"):
        if repeat == "one":
            for reaction in reactions:
                    time.sleep(.01)
                    response = check_condition (reaction["condition"])
                    if detected == "success":
                         actions = reaction["actions"]
                         for action in actions:
                             self.run(action)
                         break
            pass
        
        elif repeat == "forever":
            run_next = True
            while run_next:
                for reaction in reactions:
                    time.sleep(.01)
                    type_state = reaction["condition"]["primitive"] 
                    state  =  reaction["condition"]["input"]
                    detected = self.is_detected(type_state,state)
                    print detected
                    print "request sended"
                    if detected == True:
                         actions = reaction["actions"]
                         for action in actions:
                             self.run(action)
                         break
        pass

 
  

    def run(self, message):
        """
        Execute an action using pub/sub

        Parameters
        ----------
        action : dictionary
            action node to be executed

        """
        print "ACTION execution:"
        print action
        self.pub.send_info(action)
        robots =  []
        if type(action['robots']) is list:
            robots = robots + action['robots']
        else:
            robots = robots + [action['robots']]
        self.wait_response(robots) 



        

    def wait_response(self, robots): # Improve blocking mode
        """
        Wait until get response from all robots

        Parameters
        ----------
        robots : list
            list of robot names (nodes)

        """

        new_robot_list = robots[:]

        print ("Waiting for response of " + str(new_robot_list))
        while len(new_robot_list) > 0:
            success, state = self.sub.listen_info(False)
            if success:
                robot = str(state["robot"]) 
                result = str(state["node"])
                print ("Action performed by " + robot + " with: " + result + " ")
                if robot in new_robot_list:
                    new_robot_list.remove(robot)
                    if new_robot_list != []:
                        print ("Robots left: " + str(new_robot_list) )
            time.sleep(.001)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

                                
