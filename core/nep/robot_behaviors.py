#!/usr/bin/env python

# ------------------------ Robot behavior class --------------------------------
# Description: Robot complex behaviors class
# --------------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga




import nep
import time
import threading

            
#TODO documentation
class robot_behaviors:
    """ Class used to execute the robot behaviors. 

        Parameters
        ----------
         type_behavior : string
            Type of behavior, in this momento only "reactive"
        perception_description : dictionary
            Description of the perceptual module to react.

        Example
        ------- 
        It is necessary to specify the port, ip and topic of the perceptual module to react. This must be done using a python dictionary as the example bellow:

        
        >>> # React to arm gestures
        >>> perceptual_description = perception = {'ip': '127.0.0.1', 'port': '5002', 'topic': '/arm_gesture'}
        >>> behavior = robot_behaviors("reactive", perceptual_description) 
        

    
    """
    def __init__(self, type_behavior):
        self.exit = False
        self.human_action = 'none'
        self.success = False

        # IF the type of behavior is reactive
        if type_behavior == 'reactive':
            self.perception_topic = "/human_state"

            self.node = nep.node("robot_behavior")
            sub_config = self.node.conf_sub(mode = "many2many")
            self.listener  =  self.node.new_sub("/human_state", sub_config)

            #TODO joint, close threads           




    def update_human_state(self):
        """  Read the data from the socket and update the human state
        """   
        while not self.exit:
            self.success, state = self.listener.listen_info(block_mode = False)
            if self.success:
                #Read the human action defined in the dictionary ``state``. To obtain this info we need to use the dictionary key ``human_action``.
                self.human_action = state['human_action']
            time.sleep(.01)


    #Delete?
    def increase_counter(self,human_action,count_actions):
        if human_action in count_actions:
            count_actions[human_action] = count_actions[human_action] + 1  
        else:
            count_actions[human_action] = 1
            
        return count_actions, count_actions[human_action]
        
        
    def run(self):
        """ Run the behavior. This is done in two threads, the first one reads the perceptual information. The second one is used to react to the human actions.
        """

        self.count_actions = {}
        human_state_thread = threading.Thread(target=self.update_human_state)
        human_state_thread.start()
            
        while not self.exit:
            if self.success:
                self.exit, self.count_actions = self.reactive_behavior_function(self.human_action, self.count_actions)
            time.sleep(.01)
            
            
                                    
if __name__ == "__main__":
    import doctest
    doctest.testmod()

                                
