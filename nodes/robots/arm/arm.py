import nep
import time
import atexit

node = nep.node("turtlebot")

def goodbye():

        conf_pub = node.conf_pub(mode='many2one')
        status_pub = node.new_pub("/node_status",conf_pub)
        status_message = {'node_type':"action", 'node_status':"connection_closed", 'robot_name':robot_name, 'robot_type':'NAO'}
        print ("Closing node..")
        status_pub.send_info(status_message)

class arm():
        def __init__(self, status_publisher, ip, port, robot_name):

                # Node status publisher
                self.status_pub = status_publisher
                self.robot_name = robot_name

                print "****** Arm Action IP: " + ip

        
                self.client = nep.client(ip, port,  transport = "normal") # Create a new client instance
                print "Server connected"
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

        def run(self):
        
                status_message = {'node_type':"action", 'node_status':"connection_ready", 'robot_name':self.robot_name, 'robot_type':'arm'}
                self.status_pub.send_info(status_message)
        
                print """=================================================="""
                print "Waiting for requests ... "
                print

                while(True):            
                    success, message = self.sub.listen_info(block_mode=False)
                    time.sleep(.001)

                    if(success):
                        if robot_name in message['robots']: 
                            action = message["action"]

                            print
                            print "----------------- REQUEST: ------------------ "
                            print message

                            positive_response = True
                            primitive = action[0]
                            primitive_name = primitive["primitive"]
                            input_ = primitive["input"]
                            parameters = primitive["options"]
                            print "PRIMITIVE*   "  + str(primitive_name)  +  ": " +  str(input_)
                            if primitive_name == "animation":
                                    print "Send to emotion server"
                                    self.client.send_info(input_)   # Send request
                                    response = self.client.listen_info() # Wait for server response
                                    print "Server response: ", response                                    

                            if positive_response:
                                self.send_response("success")
                            else: 
                                self.send_response("none")

    
    
def main(ip,port,name):


    conf_pub = node.conf_pub(mode='many2one')
    status_pub = node.new_pub("/node_status",conf_pub)
    status_message = {'node_type':"action", 'node_status':"connection_starting", 'robot_name':robot_name, 'robot_type':'arm'}
    status_pub.send_info(status_message)
    atexit.register(goodbye)

    arm_matlab = arm(status_pub,ip,port, robot_name )
        


if __name__ == "__main__":

        port = "30000"
        robot_name = "arm"
        ip = '192.168.11.31'

        try:
                robot_name = sys.argv[1]
        except:
                pass
        try:
                ip = sys.argv[2]
        except:
                pass
    

        print ("Robot IP to connect:" + str(ip))
        print ("Robot PORT to connect:" + str(port))
        print ("Robot name:" + str(robot_name))
        main(ip,int(port),robot_name)



            




