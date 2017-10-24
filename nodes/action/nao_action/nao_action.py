#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

# Luis Enrique Coronado Zuniga

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.


# TODO: a fuente de error es que al adquirir un valor de  un dicionario esta es de type unicode cuando da esto error, debe ser convertido seimpre a string.
# ejemplo gesture = param['gesture'], esto da errror, sebe al ser pasado gesture a una funcion, por lo que gesture = str(gesture) soluciona el problema

from nep import*
from nep_nao import*
import time
import atexit


class nao_action():

    def __init__(self, status_publisher, nao_ip, nao_port, ip_action, robot_name):
        self.status_pub = status_publisher
        self.nao_robot_say = nao_say(nao_ip, nao_port)
        self.nao_robot_do = nao_do(nao_ip, nao_port)
        self.ip_action = ip_action

        self.pub = publisher("/action_execution")
        
        time.sleep(1)
        print " ******** Robot " + robot_name + " ready! ***********"
        self.action_to_do =  subscriber("/action_request")
        self.run()

    def send_response(self,state = "success"):
        message = {'robot_name': robot_name, 'execution_state': state}
        print ("robot ***" + robot_name + "*** send a response of: " + state)
        self.pub.send_info(message)





    def run(self):
        #TODO add signal handler or joint or read socket to exit

        status_message = {'node_type':"action_engine", 'node_status':"on", 'robot_name':robot_name, 'robot_type':'NAO', 'description':"conected"}
        print "status: on"
        self.status_pub.send_info(status_message)

        i = 0
        
        while(True):            
            success, params = self.action_to_do.listen_info()
            
            if(success):
                
                if params == "":
                    print "null value received"
                    self.send_response("error")
                else:
                    valid_action = False
                    
                    print ("new behavior execution")
                    action = params["action"]
                    #TODO: solve problem multiple robots
                    #name = params["robot"]
                    #if name == robot_name:

                    #TODO valid action and send_response succes can be improved?
                    if(action== "setVoice"):
                        valid_action = True
                        volum = float(params["volum"])
                        pitch = float(params["pitch"])
                        dVoice = float(params["doubleVoice"])
                        speed = float(params["speed"])

                        self.nao_robot_say.setVoice(speed,volum,pitch,dVoice)
                        self.send_response("success")

                    if (action == "imitation"):
                        valid_action = True
                        
                        gesture = str(params["gesture"])
                        sound = str(params["sound"])
                        type_sound = str(params["type_sound"])

                        self.nao_robot_do.imitation(gesture, type_sound, sound)
                        self.send_response("success")

                    
                    if (action == "posture_standInit"):
                        valid_action = True
                        self.nao_robot_do.posture_standInit()
                        self.send_response("success")

                    if (action == "posture_stand"):
                        valid_action = True
                        self.nao_robot_do.posture_stand()
                        self.send_response("success")
                        
                    if (action == "posture_rest"):
                        valid_action = True
                        self.nao_robot_do.posture_rest()
                        self.send_response("success")

                    if (action == "walk"):
                        valid_action = True
                        x = str(params["x"])
                        y = str(params["y"])
                        theta = 0.0
                        self.nao_robot_do.walk_to(x,y,theta)
                        self.send_response("success")
                        
                    if (action == "posture_sit"):
                        valid_action = True
                        self.nao_robot_do.posture_sit()
                        self.send_response("success")
                        
                    #TODO add person ability
                    if (action == "say"):
                        valid_action = True
                        gesture = params["gesture"]

                        try:
                            print ("Robot will say: "  +  str(params["text"]))
                        except:
                            pass
                        
                        if (gesture == "no_gesture"):
                            text = params["text"] # text to say (string)
                            language =  str(params['language'])
                            self.nao_robot_say.without_moving(text.encode("utf-8"), language)
                            self.send_response("success")

                        else:
                            try:
                                text = params["text"] # text to say (string)
                                gesture = params["gesture"] # type of gesture to do (string)
                                language =  str(params['language'])
                                self.nao_robot_say.with_gesture(text.encode("utf-8"),str(gesture),language)
                                self.send_response("success")
                            except:
                                print ("Error: Inavlid parameter passed in the socket")
                                self.send_response("Error")

                    print ("Behavior **"  + action + "** finished...")
                    if valid_action == False:
                        self.send_response("error")


def goodbye():

        status_pub = publisher("/node_status", False)
        status_message = {'node_type':"action_engine", 'node_status':"off", 'robot_name':robot_name, 'robot_type':'NAO', 'description':"closed"}
        status_pub.send_info(status_message)

    

def main(nao_ip,nao_port,ip_action,robot_name):



    status_pub = publisher("/node_status", False)
    status_message = {'node_type':"action_engine", 'node_status':"starting", 'robot_name':robot_name, 'robot_type':'NAO', 'description':"busy"}
    status_pub.send_info(status_message)
    atexit.register(goodbye)
        
    print "****** NAO Robot IP: " + nao_ip
    nao = nao_action(status_pub,nao_ip, nao_port, ip_action, robot_name )


    




if __name__ == "__main__":

    
    nao_port = 9559
    ip_action = '127.0.0.1'

    try:
        nao_ip = sys.argv[1]
        robot_name = sys.argv[2]
        print ("Robot IP to connect:" + str(nao_ip))
        print ("Robot name:" + str(robot_name))
        
    except:
        nao_ip = '127.0.0.1'
        robot_name = "nao"

    main(nao_ip,nao_port,ip_action,robot_name)
            
            
        
            
