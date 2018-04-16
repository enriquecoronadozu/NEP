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

class turtlebot():
        def __init__(self, status_publisher, ip, port, robot_name):

                # Node status publisher
                self.status_pub = status_publisher

                print "****** TurtleBot Robot IP: " + ip

                robot_conf = node.conf_pub(network = "direct", ip = "192.168.11.4", port = "9090")
                self.robot_pub = node.new_pub("test", robot_conf)


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
        
                status_message = {'node_type':"action", 'node_status':"connection_ready", 'robot_name':robot_name, 'robot_type':'turtlebot'}
                self.status_pub.send_info(status_message)
        
                print """=================================================="""
                print "Waiting for request ... "
                print

         

                x = 0
                y = 0
                z = 0
                a = 0
                b = 0
                c = 0

                while(True):
                        success, message = self.sub.listen_info(block_mode=False)
                        time.sleep(.001)
                        if(success):
                                action = message["action"]
                                print message
                                x = action[0]['options']['x']
                                y = action[0]['options']['y']
                                c = action[0]['options']['theta']
                                msg = {"linear":[x,y,z], "angular":[a,b,c]}
                                
                                print "send"
                                self.robot_pub.send_info(msg)
                                self.send_response("success")
                                        
##                    action = message["action"]
##                    msg = {"linear":[x,y,z], "angular":[a,b,c]}
##                    pub.send_info(msg)
    

    
    
def main(nao_ip,nao_port,robot_name):


    conf_pub = node.conf_pub(mode='many2one')
    status_pub = node.new_pub("/node_status",conf_pub)
    status_message = {'node_type':"action", 'node_status':"connection_starting", 'robot_name':robot_name, 'robot_type':'NAO'}
    status_pub.send_info(status_message)
    atexit.register(goodbye)

    turtle = turtlebot(status_pub,nao_ip, nao_port, robot_name )
        


if __name__ == "__main__":

        port = "9090"
        robot_name = "turtle"
        ip = '127.0.0.1'

        try:
                robot_name = sys.argv[1]
        except:
                pass
        try:
                ip = sys.argv[2]
        except:
                pass
        try:
                port = sys.argv[3]
        except:
                pass
    

        print ("Robot IP to connect:" + str(ip))
        print ("Robot PORT to connect:" + str(port))
        print ("Robot name:" + str(robot_name))
        main(ip,int(port),robot_name)



            




