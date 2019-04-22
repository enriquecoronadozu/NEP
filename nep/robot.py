import nep
import threading
import time
import signal
import sys, os

class robot:
    
    def __init__(self, robot_name, pattern = "survey"):
        """ Define a new robot

            Parameters
            ----------

            robot_name : string
                Node or robot name which identify the robot

            pattern : string
                - If selected "survey" or "surveyor", then "nanomsg" will be used as middleware
                - If selected "actionlib", then "ROS" will be used as middleware
                - If selected "client-server", then "ZeroMQ" will be used as middleware
                - If selected "pub-sub", then  "ZeroMQ" will be used as middleware
        """

        self.middleware = pattern
        self.robot_name = robot_name
        self.deadline = 60 # cancel action that last more that 60 seconds
        self.action = {"state":"success"}
        self.currentActionID = "0"
        self.node = nep.node(robot_name, "ZMQ", True)

        conf_pub = self.node.broker()
        self.sharo = self.node.new_pub("/sharo", "json", conf_pub)

        # Use survey pattern
        if self.middleware == "nanomsg":
            print ("ROBOT NODE using: survey pattern")
            self.resp = self.node.new_respondent("action_survey") # Respondent subscribes to /manager topic 
        
        elif self.middleware == "ZMQ":
            print ("ROBOT NODE using: client-server pattern")
            self.server = self.node.new_server("action_server") # Respondent subscribes to /manager topic 

        elif self.middleware == "ROS":
            print ("ROBOT NODE using: ROS 1.0 actionlib")
            pass

        elif self.middleware == "ROS2":
            print ("ROBOT NODE using: ROS 2.0 actionlib")
            pass

        time.sleep(1)
    
        self.state = "idle" # idle can only be idle, busy or wait
        self.result = "inactive" # result can only be success or failure.
        self.action2do = {"status":"0", "action":{}}

        # Give feedback to the rize interface
        self.robot_actions = {}
        self.robot_cancel_actions = {}

        self.isCanceled = False
        self.inActionExecution = False
        self.running = True

        # ------------------------- Action thread ------------------------------------
        self.action_thread = threading.Thread(target = self.onActionLoop)
        self.action_thread.start()
        
        # ------------------------- Stop thread ------------------------------------
        self.cancel_thread = threading.Thread(target = self.onCancelLoop)
        self.cancel_thread.start()

    def onActionLoop(self):

        while self.running:    
            if self.action["state"] == "active" or self.action["state"] == "pending":
                self.inActionExecution = True #TODO: lock
                self.run_action(self.action)
                self.sharo.publish(self.action)
                print (self.action["id"] + " finished")
                self.inActionExecution = False #TODO: lock
                self.action["state"] = "success"
            time.sleep(.001)

    def onCancelLoop(self):
        while self.running:
           
            if self.isCanceled:
                print ("CANCEL" + str(self.action))
                self.run_action(self.action, cancel = True)
                self.isCanceled = False 
                print ("CANCELLLLLLL ---------------------------")
            else:
                time.sleep(0.05)


    def setRobotActions(self,robot_actions):
        """ Set a python dictionary with all the functions which the node can execute
            Parameters
            ----------

            robot_actions : dictionary
                Dictionary of functions
            
        """
        try:
            self.robot_actions = robot_actions
        except Exception as e: 
            print(e)
            print ("Error setting actions")
            self.node.failure()
            time.sleep(1)


    def setCancelActions(self,actions):
        """ Set a python dictionary with all the functions which the node can execute
            Parameters
            ----------

            robot_actions : dictionary
                Dictionary of functions
            
        """
        try:
            self.robot_cancel_actions = actions
        except Exception as e: 
            print(e)
            print ("Error setting cancel actions")
            self.node.failure()
            time.sleep(1)
        

                      
    def __listen_request(self):
        """ Listen and wait for the robot actions
        """
        success =  False
        action_request = {}
        if self.middleware == "nanomsg":
            success, action_request = self.resp.listen_json(block_mode=False)
            #if success:
                #print (action_request)
        elif self.middleware == "ZMQ":
            success =  True
            action_request = self.server.listen_info()

        if success:
            #print (action_request)
            if action_request["node"] == "cancel":
                return  True, action_request
            
            if self.robot_name in action_request['robots']: 
                return  True, action_request
            else:
                return  False, action_request

        return success, action_request


    def __send_response(self,msg):
        """ Send the response to the survey/cognitive node
        """
        #print 
        #print ("Response:")
        #print (msg)
        if self.middleware == "nanomsg":
            self.resp.send_json(msg)
        elif self.middleware == "ZMQ":
            self.server.send_info(msg)

    
        
       
    def run(self):
        while self.running:

            success, action_request =  self.__listen_request()

            if success:
                
                if action_request["node"] == "cancel":
                    self.isCanceled = True
                    msg = {"node":"canceled", "robot":self.robot_name}
                    self.__send_response(msg)
                else: 
                    
                    listPrimitives = []
                    primitives = action_request["primitives"]
                    for p in primitives:
                        listPrimitives.append(p["primitive"])

                    #print ("ACTION: --" +  action_request["id"] + "-- primitives: " + str(listPrimitives) )  

                    # If an action is in execution
                    if self.inActionExecution: 
                        
                        # Check if the action request is new or the same
                        new_action = self.checkIfNew(action_request)
                        #print ("returned new action" + str(new_action))
                        
                        # If is a new action, the cancel current action and return pending
                        if new_action:
                            #print ("new action - cancel")
                            self.isCanceled = True #TODO lock
                            self.execution_state = "pending"
                        # Else return running, action still not finished
                        else:
                            self.execution_state = "running"

                    # If robot idle
                    else:
                        new_action = self.checkIfNew(action_request)
                        #print ("returned new action " + str(new_action))
                        if new_action:
                            #print ("new action  - run")
                            #print ("running " + action_request["id"])
                            self.resetActionTime() #Reset time counter for actions
                            self.setAction(action_request) #Set new action to execute
                            self.execution_state = "running"
                        else:
                            self.execution_state = "success"

                    msg = {"node":self.execution_state, "robot":self.robot_name}
                    if self.execution_state == "success":
                        print ("Action -- " + action_request["id"] + " -- success")
                    #print (msg)

                    self.__send_response(msg)
                
                
            if self.inActionExecution:
                action_time = self.getActionTime()
                if action_time > self.deadline: # Cancel if is in a posible deadlock
                    self.isCanceled = True #TODO lock
            time.sleep(0.01)

                

    def resetActionTime(self):
        self.initActionTime =  time.time()

    def setAction(self,action_request):
        self.currentActionID = action_request["id"]
        self.action = action_request

    def getActionTime(self):
        return time.time() - self.initActionTime 


    def checkIfNew(self,action_request):
        id_ = action_request["id"]

        #print (self.currentActionID)
        if id_ != self.currentActionID:
            return True
        else:
            return False
            
        

    def run_action(self, message, cancel = False):
        """ Run an action
            
            Parameters
            ----------

            action : dictionary
                Action description

        """
            
        action = message["primitives"] # Get list of concatenated primitives
        n_primitives = len(action)
        in_parallel = True
                
        # Perform all the actions in parallel
        for i in range(n_primitives):
                    
            # Except the last one
            if (i == n_primitives-1):
                in_parallel = False
                
            primitive = action[i]
            primitive_name = primitive["primitive"] #Name of the primitive
            input_ = primitive["input"]
            options = primitive["options"]

            if primitive_name in self.robot_actions:
                # Execute function
                if cancel:
                    try:
                        self.robot_cancel_actions[primitive_name]()
                        print (primitive_name, " I am cancelling")
                    except:
                        pass
                else:
                    self.robot_actions[primitive_name](input_, options, in_parallel)
                    #print (primitive_name, " was executed")
                    
            else:
                print (primitive_name, "is not a valid primitive")