import nep
import threading
import time
import signal

class robot:
    
    def __init__(self, robot_name, pattern = "surveyor"):
        """ Define a new robot node using surveyor or publish/subscriber pattern

            Parameters
            ----------

            robot_name : string
                Node or robot name which identify the robot

            pattern : string
                Can take two values: "surveyor" or "pubsub" to use the surveyor or publish-subscribe communication pattern

        """
        
        ip = '127.0.0.1'
        port = "9080"

        self.pattern = pattern
        self.robot_name = robot_name
        self.resp = nep.respondent(ip,port)
    


        self.state = "idle" # idle can only be idle, busy or wait
        self.result = "inactive" # result can only be success or failure.
        self.action2do = {"action":"none"}
        self.node = nep.node(robot_name)
        self.fd = self.node.activate_feedback()
        self.fd.connection_starting()
        self.robot_actions={}

        # ---------------------- Program stop execution ----------------------------
        # Only the Python server can stop a program
        #conf = self.node.conf_sub(mode= "one2many") 
        #self.exit_sub  = self.node.new_sub("/program_execution", conf)


        # --------------- Publisher subscriber action nodes --------------------
        conf_pub = self.node.conf_pub(mode='many2one')
        self.pub=  self.node.new_pub("/action_response",conf_pub)
        conf_sub =  self.node.conf_sub(mode='one2many')
        self.sub =  self.node.new_sub("/action_request",conf_sub)
        time.sleep(.2)

        # ------------------------- Update thread ------------------------------------
        self.action_response = threading.Thread(target = self.__onUpdateStatus)
        self.action_response.daemon = True
        self.action_response.start()

        # ------------------------- Kill thread ------------------------------------
        # thread that can de used to stop the program
        #self.exit = threading.Thread(target = self.__wait_kill)
        # Used to finish the background thread when the main thread finish
        #self.exit.daemon = True
        # start new thread 
        #self.exit.start()
        self.fd.connection_ready()

    def set_robot_actions(self,robot_actions):
        """ Set a python dictionary with all the functions which the node can execute
            Parameters
            ----------

            robot_actions : dictionary
                Dictionary of functions
            
        """
        self.robot_actions = robot_actions


    def __onUpdateStatus(self):
        """
        Update the state machine for action execution
        """
        while True:
            success, action_request =  self.listen_request()
            if success:
                if action_request["node"] == "action":
                    self.action2do =  action_request
                if self.state == "idle":
                    self.state = "busy"
                    msg = {"node":"running", "robot":self.robot_name}
                    if self.pattern == "surveyor": # TODO: improve?
                        self.__send_response(msg)
                elif self.state == "busy":
                    msg = {"node":"running", "robot":self.robot_name}
                    if self.pattern == "surveyor": # TODO: improve?
                        self.__send_response(msg)
                elif self.state == "wait":
                    self.state = "idle"
                    msg = {"node":"success", "robot":self.robot_name}
                    print (msg)
                    self.__send_response(msg)
            elif self.state == "wait" and self.pattern == "pubsub":  # TODO: improve?
                    self.state = "idle"
                    msg = {"node":"success", "robot":self.robot_name}
                    print (msg)
                    self.__send_response(msg)
                

    def __listen_request(self):
        """ Listen and wait for the robot actions
        """
        success =  True
        if self.pattern == "surveyor":
            action_request = self.resp.listen_info()
        elif self.pattern == "pubsub":
            success, action_request = self.sub.listen_info(block_mode=False)

        if success:
            if self.robot_name in action_request['robots']: 
                success = True
            else:
                success = False

        return success, action_request
        

    def __send_response(self,msg):
        """ Send the response to the surveyor/cognitive node
        """
        if self.pattern == "surveyor":
            self.resp.send_info(msg)
        elif self.pattern == "pubsub":
            self.pub.send_info(msg)

    def run(self):
        """ Run the action node
        """
        while True:
            if self.state == "busy":
                self.run_action(self.action2do)
                self.state = "wait"
            else:
                time.sleep(.001)


    def run_action(self, message):
        """ Run an action
            
            Parameters
            ----------

            action : dictionary
                Action description

        """
            
        action = message["primitives"]
        n_primitives = len(action)
        in_parallel = True
                
        # Perform all the actions in parallel
        for i in range(n_primitives):
                    
            # Except the last one
            if (i == n_primitives-1):
                in_parallel = False
                
            primitive = action[i]
            primitive_name = primitive["primitive"]
            input_ = primitive["input"]
            parameters = primitive["options"]

            if primitive_name in self.robot_actions:
                # Execute function
                self.robot_actions[primitive_name](input_, parameters, in_parallel)
                print (primitive_name, " was executed")
                    
            else:
                print (primitive_name, "is not a valid primitive")



