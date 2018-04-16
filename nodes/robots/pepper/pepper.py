#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

# Luis Enrique Coronado Zuniga

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.


# TODO: cambiar a nueva nimevlaturea ---- action por primitive, 

import nep
import nep_nao
import time
import atexit
import sys
import signal


node = nep.node("NAO")

def signal_handler(signal, frame):
    """Signal handler used to close the app"""
    print('Signal Handler, you pressed Ctrl+C!')
    time.sleep(1)
    sys.exit(0)


class nao_action():

    def __init__(self, status_publisher, nao_ip, nao_port, robot_name):
        
        # Node status publisher
        self.status_pub = status_publisher

        # New nao instance
        self.robot = nep_nao.nao(nao_ip, nao_port)
        self.language = "English"
        
        # Robot funtions 

        self.switch={
            'say':self.robot.say,
            'rest':self.robot.rest,
            'say_contextual': self.robot.say_contextual,
            'wake_up': self.robot.wake_up,
            'animation': self.robot.animation,
            'imitation': self.robot.imitation,
            'stop_behaviors':self.robot.stop_behaviors,
            'posture':self.robot.posture,
            'play_sound':self.robot.play_sound,
            'open_hand': self.robot.open_hand,
            'close_hand': self.robot.close_hand,
            'close_hand': self.robot.close_hand,
            'move_to_position':self.robot.move_to_position,
            'change_joint_value':self.robot.change_joint_value,
            'move':self.robot.move,
            }

        # New pub/sub to cognitive nodes
        conf_pub = node.conf_pub(mode='many2many')
        self.pub= node.new_pub("/action_response",conf_pub)
        conf_sub = node.conf_sub(mode='many2many')
        self.sub = node.new_sub("/action_request",conf_sub)
        time.sleep(.2)

        
        print " ******** Robot " + robot_name + " ready! ***********"
        self.run()
        
        


    #TODO send response as a nep class
    def send_response(self,state = "success"):
        message = {'robot_name': robot_name, 'execution_state': state}
        print ("robot ***" + robot_name + "*** send a response of: " + state)
        self.pub.send_info(message)

    def set_language(self,language):
        self.language = language


    def run(self):
        

        
        #TODO add signal handler or joint or read socket to exit
        status_message = {'node_type':"action", 'node_status':"connection_ready", 'robot_name':robot_name, 'robot_type':'NAO'}
        self.status_pub.send_info(status_message)
        
        print """=================================================="""
        print "Waiting for request ... "
        print

        switch  = self.switch

        while(True):            
            success, message = self.sub.listen_info(block_mode=False)
            time.sleep(.001)

            if(success):
                if robot_name in message['robots']: 
                    action = message["action"]
                    print
                    print
                    print "----------------- REQUEST: ------------------ "
                    print message

                    n_primitives = len(action)

                    """if n_actions  == 1:
                        action = actions[0]
                        print action
                        action_name = action["action"]
                        print action_name
                        input_ = action["input"]

                        if action_name in switch:

                            if  input_ == "none":
                                switch[action_name]()
                            else:
                                switch[action_name](input_)

                            print action_name, "is a valid action"
                            self.send_response("success")
                        else:
                            
                            print action_name, "is not valid action"
                            self.send_response("none")
                    
                    if n_actions  == 2:"""
                        
                    positive_response = True
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

                        print "PRIMITIVE*   "  + str(primitive_name)  +  ": " +  str(input_)

                        if primitive_name in switch:

                            self.runAction(primitive_name, input_, parameters, in_parallel )
                            print primitive_name, "is a valid primitive"
                            
                        else:
                            print primitive_name, "is not valid primitive"
                            positive_response = False

                    if positive_response:
                        self.send_response("success")
                    else: 
                        self.send_response("none")


                    

    def runAction(self,primitive_name, input_, parameters, in_parallel = False):
        # ------------------------------- none is important --------------------------------
        if  input_ == "none":
            self.switch[primitive_name](parameters, in_parallel)
        else:
            self.switch[primitive_name](input_, parameters, in_parallel)

    


def connection_error():
    
        conf_pub = node.conf_pub(mode='many2one')
        status_pub = node.new_pub("/node_status",conf_pub)
        status_message = {'node_type':"action", 'node_status':"connection_error", 'robot_name':robot_name}
        status_pub.send_info(status_message)            

                    
def goodbye():

        conf_pub = node.conf_pub(mode='many2one')
        status_pub = node.new_pub("/node_status",conf_pub)
        status_message = {'node_type':"action", 'node_status':"connection_closed", 'robot_name':robot_name, 'robot_type':'NAO'}
        print ("Closing node..")
        status_pub.send_info(status_message)

    
def main(nao_ip,nao_port,robot_name):

    signal.signal(signal.SIGINT, signal_handler)
    conf_pub = node.conf_pub(mode='many2one')
    status_pub = node.new_pub("/node_status",conf_pub)
    status_message = {'node_type':"action", 'node_status':"connection_starting", 'robot_name':robot_name, 'robot_type':'NAO'}
    status_pub.send_info(status_message)
    atexit.register(goodbye)
        
    print "****** NAO Robot IP: " + nao_ip
    nao = nao_action(status_pub,nao_ip, nao_port, robot_name )


if __name__ == "__main__":

    nao_port = "9559"
    robot_name = "nao"
    nao_ip = '127.0.0.1'


    try:
        robot_name = sys.argv[1]
    except:
        pass
    try:
        nao_ip = sys.argv[2]
    except:
        pass
    try:
        nao_port = sys.argv[3]
    except:
        pass
    
    try:
        print ("Robot IP to connect:" + str(nao_ip))
        print ("Robot PORT to connect:" + str(nao_port))
        print ("Robot name:" + str(robot_name))
        main(nao_ip,int(nao_port),robot_name)
    except:
        connection_error()


            
