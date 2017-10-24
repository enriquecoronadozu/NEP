# coding = utf-8
#!/usr/bin/env python

# ------------------------ Communication module --------------------------------
# Description: Set of classes used to abtract the transport layer using ROS, ZeroMQ and nanomsg
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


import time
import os
import zmq
from nep import human
import json
import sys



class node:
    def __init__(self, node_name, useROS = False):
        """ Class used to create NEP nodes, also abtract the creation of ROS nodes

        Parameters
        ----------
        node_name : string 
            nome of the node

        useROS : bool
            bool varaible that indicates the use of Ubuntu creation of ROS nodes
        """

        self.node_name = node_name
        self.useROS = useROS
        print ("New NEP node: " + self.node_name)
        
        if self.useROS ==True:
            try:
                import rospy		
                rospy.init_node(node_name, anonymous=True)
                print ("ROS node started")
            except:
                print ("ERROR: rospy not found, possible causes:")
                print ("- Are you using Ubuntu?")
                print ("- Have you installed ROS in your PC?")
                print ("- Have you used roscore command to start the ROS Master")
                
                if sys.version_info < (3.0):
                    y = raw_input("Press ENTER to continue and exit")

                sys.exit(1)


    def config_pub(self, transport = "ZMQ", network = "P2P", port = 9000, ip = "127.0.0.1", mode = "one2many" ):
        """ Function used to define the configuration of a publisher.

            Parameters
            ----------
            transport : string 
                middleware used, values can be "ZMQ" to ZeroMQ, "ROS" to use ROS and "NANO" to use nanomsg

            network : string
                Type to network topology used, values can be "P2P" to use name service masters or "direct" to indicate a specific endpoint 

            port : int
                specific port used only when network is set to "direct", by default port = 9000

            ip : strint
                specific ip used only when network is set to "direct", by default ip = "127.0.0.1"

            mode : "string"
                publisher mode for ZeroMQ, used when transport is set to "ZMQ". It value can be "one2many" or many2one". TODO: explain mode this.
            
            return: dictionary
                dictionary whit the publisher specifications
        """

        conf = { 'transport': transport, 'network': network, 'port': str(port), 'ip': ip, 'mode':mode}
        return conf

    def config_sub(self, transport = "ZMQ", network = "P2P", port = "9000", ip = "127.0.0.1", mode = "one2many" ):
        
         """ Function used to define the configuration of a subscriber.

            Parameters
            ----------
            transport : string 
                middleware used, values can be "ZMQ" to ZeroMQ, "ROS" to use ROS and "NANO" to use nanomsg

            network : string
                Type to network topology used, values can be "P2P" to use name service masters or "direct" to indicate a specific endpoint 

            port : int
                specific port used only when network is set to "direct", by default port = 9000

            ip : strint
                specific ip used only when network is set to "direct", by default ip = "127.0.0.1"

            mode : "string"
                publisher mode for ZeroMQ, used when transport is set to "ZMQ". It value can be "one2many" or many2one". TODO: explain mode this.
            
            return: dictionary
                dictionary whit the publisher specifications
        """
        conf = { 'transport': transport, 'network': network, 'port': port, 'ip': ip, 'mode':mode}
        return conf

    def new_pub(self,topic, configuration =  {'transport': "ZMQ", 'network': "P2P", 'mode':"one2many", 'ip': '127.0.0.1' }):
        
        """ Function used to create a new publisher

            Parameters
            ----------
            topic : "string"
                Name of the topic to send the messages

            configuration : dictionary
                dictionary used to specify the configuration of the publisher

             return: publisher
                publisher object used to send the messages in the defined topic
        """

        pub = publisher(topic, self.node_name, configuration)
        return pub

    def new_sub(self,topic, configuration =  {'transport': "ZMQ", 'network': "P2P", 'mode':"one2many", 'ip': '127.0.0.1' }):
            """ Function used to create a new subscriber

            Parameters
            ----------
            topic : "string"
                Name of the topic to receive the messages

            configuration : dictionary
                dictionary used to specify the configuration of the subscriber

             return: subscriber
                susbcriber object used to send the messages in the defined topic
        """
        sub = subscriber(topic, self.node_name, configuration)
        return sub


#TODO: sock.close() and context.destroy() must be allway when a process ends
#In some cases socket handles won't be freed until you destroy the context.
#When you exit the program, close your sockets and then call zmq_ctx_destroy(). This destroys the context.
# In a language with automatic object destruction, sockets and contexts 
# will be destroyed as you leave the scope. If you use exceptions you'll have to
#  do the clean-up in something like a "final" block, the same as for any resource.

#TODO in documentation , see if the function send and receive objects or dictionaries in functions as send_info, problem of publisher already used.
class publisher:
    """ Publisher class used for inter-process comunication between nodes. 

        Parameters
        ----------
        topic : string 
            topic name to publish the messages

        node_name : string
            Name of the node

        msg_type : string
            Type of the message to be send. It support strings, python dictionaries and ROS geometric types. TODO: add reference page

        configuration : dictionary
            Configuration of the publisher

    """

    def __init__(self, topic, msg_type = "string", node_name = "default", configuration =  {'transport': "ZMQ", 'network': "P2P", 'mode':"one2many", 'ip' : '127.0.0.1' }):

        self.conf = configuration
        self.network = self.conf['network']
        self.transport =  self.conf['transport']
        self.node_name = node_name
        self.topic = topic
        self.msg_type = msg_type

        if self.transport ==  "ZMQ":
            try:
                self.mode = self.conf['mode']
            except:
                print ("WARNING: publisher mode nod defined, 'one2many' mode is set by default")
                self.mode = "one2many"
            self.create_ZMQ_publisher()
            
        if self.transport ==  "ROS":
            self.create_ROS_publisher()


    #TODO:also define queue_size
    def create_ROS_publisher(self):
        """ Function used to create and define a ROS publisher """
        
		import rospy

                if self.msg_type == "string":
                    from std_msgs.msg import String
                    self.ros_pub = rospy.Publisher(self.topic, String, queue_size=10)

                elif self.msg_type == "velocity":
                    from geometry_msgs.msg import Twist
                    self.ros_pub = rospy.Publisher(self.topic, Twist, queue_size=10)

                elif self.msg_type == "point":

                    from geometry_msgs.msg import Point
                    self.ros_pub = rospy.Publisher(self.topic, Point, queue_size=10)

                elif self.msg_type == "wrench":

                    from geometry_msgs.msg import Wrench
                    self.ros_pub = rospy.Publisher(self.topic, Wrench, queue_size=10)

                elif self.msg_type == "accel":

                    from geometry_msgs.msg import Accel
                    self.ros_pub = rospy.Publisher(self.topic, Accel, queue_size=10)

                elif self.msg_type == "quaternion":

                    from geometry_msgs.msg import Quaternion
                    self.ros_pub = rospy.Publisher(self.topic, Quaternion, queue_size=10)

                elif self.msg_type == "vector":

                    from geometry_msgs.msg import Vector
                    self.ros_pub = rospy.Publisher(self.topic, Vector, queue_size=10)

                elif self.msg_type == "pose:

                    from geometry_msgs.msg import Pose
                    self.ros_pub = rospy.Publisher(self.topic, Pose queue_size=10)
        

    def create_ZMQ_publisher(self):
        """ Function used to create and define a ZMQ publisher """
        if self.network == "direct":
            # Set the port selected by the user
            port = set_port
        elif self.network == "P2P":
            # Register the topic in the NEP Master and get the port
            print ("Advertising topic to NEP Master ....")
            port = self.advertising_zqm(self.node_name, self.topic, master_ip = '127.0.0.1', master_port = 7000)
            print ("Topic registered by the NEP Master")

        ip = self.conf['ip']
        endpoint = "tcp://" + ip + ":" + str(port)
        

        # Create a new ZeroMQ context and a publisher socket
        try:
            context = zmq.Context()
            # Define the socket using the "Context"
            self.sock = context.socket(zmq.PUB)
            #Set the topic of the publisher and the end_point
            
            if self.mode == "one2many":
                # This allows only use one publisher connected at the same endpoint
                self.sock.bind(endpoint)
                print ("publisher " + endpoint +  " bind")
            elif self.mode == "many2one":
                # This allows two use more that one publisher ate the same endpoint
                self.sock.connect(endpoint)
                print ("publisher " + endpoint +  " connect")

        except:
            print("Socket already in use, restarting")
            self.sock.close()
            context.destroy()
            time.sleep(.2)
            context = zmq.Context()
            self.sock = context.socket(zmq.PUB)
            if self.mode == "one2many":
                # This allows only use one publisher connected at the same endpoint
                self.sock.bind(endpoint)
                print ("publisher " + endpoint +  " bind")
            elif self.mode == "many2one":
                # This allows two use more that one publisher ate the same endpoint
                self.sock.connect(endpoint)
                print ("publisher " + endpoint +  " connect")

        #TODO: why this problem?
        #This next lines are used to start the comunication, and avoid some errors presented with zeromq
        message = {'action': 'none'}
        self.send_info(message)

        # ZeroMQ note:
        # There is one more important thing to know about PUB-SUB sockets: 
        # you do not know precisely when a subscriber starts to get messages.
        # Even if you start a subscriber, wait a while, and then start the publisher, 
        # the subscriber will always miss the first messages that the publisher sends. 


        # In Chapter 2 - Sockets and Patterns we'll explain how to synchronize a 
        # publisher and subscribers so that you don't start to publish data until 
        # the subscribers really are connected and ready. There is a simple and 
        # stupid way to delay the publisher, which is to sleep. Don't do this in a
        #  real application, though, because it is extremely fragile as well as
        #  inelegant and slow. Use sleeps to prove to yourself what's happening, 
        # and then wait for 
        # Chapter 2 - Sockets and Patterns to see how to do this right.

        #This delay in important, whithout them the comunication is not effective.

        time.sleep(1)
        print ("ZMQ publisher started in " +  endpoint)
        print
            

    def advertising_zqm(self, node_name, topic, master_ip = '127.0.0.1', master_port = 7000):
        """ Function used to register a ZMQ topic in the NEP master


        Parameters
        ----------

        node_name : string
            Name of the node

        topic : string 
            topic name to publish the messages

        master_ip : string
            IP adress of the master node, by default is set to '127.0.0.1'

        master_port : int
            port of the master node,  by default is set to '7000'
        """
        
        #Use client-server pattern to advertise and register a node and topic to the NEP Master
        context = zmq.Context()
        self.master_sock = context.socket(zmq.REQ)
        self.master_sock.connect("tcp://"+ master_ip + ":" + str(master_port))
        self.master_sock.send_json({'node_name':node_name, 'topic':topic})
        response = self.master_sock.recv_json()
        topic_id = response['topic']
        if(topic_id == topic):
            port = response['port']
        return port

    #Status: OK
    def serialization(self, message, topic = None):
        """ Function used to serialize a python dictionary using json. In this function the message to be send is attached to the topic. If the topic is not specified it send the message in the default topic.
            
            Parameters
            ----------
            message : dictionary
                Python dictionary to be send

             topic : string
                name of the topic to send the message
            
            Returns
            -------
            message : string
                Message to be send, topic + message 
        """
        if topic is None:
            return self.topic + ' ' + json.dumps(message)
        else:
            return topic + ' ' + json.dumps(message)
            
    
    
    def send_string(self,message, topic = None):
        """ Publish a string value. If a topic is not specified, then the messages will be published in the topic specified in the parameter topic_name when a object in this class is created.
            Otherwise it is published in the topic specified in the second parameter of this function. If the topic is not specified it send the message in the default topic.
            
            Parameters
            ----------
            message : string String to be sended

             topic : string
                name of the topic to send the message
                
        """
        if self.transport ==  "ZMQ":
            if topic is None:
                self.sock.send_string(self.topic + ' ' + message)
            else:
                self.sock.send_string(topic + ' ' + message)

	if self.transport == "ROS":
		self.ros_pub.publish(message)
            

    #Status: OK
    def send_info(self,message, topic = None, debug = False):
        """ Function used to publish a python dictionary. The message is first serialized using json format and then published by the socket
            
            Parameters
            ----------
            message : dictionary 
                Python dictionary to be send
            topic : string
                name of the topic to send the message
            debug : bool
                if == True, then it print the message to send
        """

        if self.transport ==  "ZMQ":
            # TODO: if data es diferente a la definida poner un warning
            if topic is None:
                info = self.serialization(message)
            else:
                info =  self.serialization(message, topic)

            if debug:
                try:
                    print (info)
                except:
                    pass
            self.sock.send(info)
        
        if self.transport == "ROS":
            #TODO add try and except fot error of data

            if self.msg_type == "string":
                   

                elif self.msg_type == "velocity":


                elif self.msg_type == "point":


                elif self.msg_type == "wrench":

                elif self.msg_type == "accel":


                elif self.msg_type == "quaternion":


                elif self.msg_type == "vector":


                elif self.msg_type == "pose:


            
            self.ros_pub.publish(message)
        

    #TODO: does not work, no manda mensajes
    def send(self,message, debug = False):
        if self.transport ==  "ZMQ":
            if type(message) == type(dict()):
                if debug:
                    try:
                        print (message)
                    except:
                        pass
                
                self.sock.send_json(message)
                
            else:
                print ("ERROR: message must to be a Python dictionary")
        




    
#Status: OK
class subscriber:
    """ Subscriber class used for inter-process comunication between nodes. 

        Parameters
        ----------
        topic : string 
            topic name to publish the messages

        node_name : string
            Name of the node 

        configuration : dictionary
            Configuration of the subscriber

    """
    def __init__(self, topic,node_name = "default", configuration =  {'transport': "ZMQ", 'network': "P2P", 'mode':"one2many", 'ip' : '127.0.0.1' }):
    
        self.conf = configuration
        self.network = self.conf['network']
        self.transport =  self.conf['transport']
        self.node_name = node_name
        self.topic = topic

        if self.transport ==  "ZMQ":
            try:
                self.mode = self.conf['mode']
            except:
                print ("WARNING: publisher mode nod defined, 'one2many' mode is set by default")
                self.mode = "one2many"

            self.create_ZMQ_subscriber()
        if self.transport ==  "ROS":
            self.create_ROS_subscriber()

    def create_ZMQ_subscriber(self):
        """ Function used to create and define a ZMQ publisher """
        
        if self.network == "direct":
            # Set the port selected by the user
            port = set_port
        elif self.network == "P2P":
            # Register the topic in the NEP Master and get the port
            print ("Advertising topic to NEP Master ....")
            port = self.advertising_zqm(self.node_name, self.topic, master_ip = '127.0.0.1', master_port = 7000)
            print ("Topic registered by the NEP Master")

        ip = self.conf['ip']
        endpoint = "tcp://" + ip + ":" + str(port)
        
            
        try:        
            # ZeroMQ Context
            self.context = zmq.Context()

            # Start a null social signal current state
            self.info = ""

            self.delimiter = " " #space delimiter for python, for C# is "\n"

            # Define the type of context, in this case a subcriber
            self.sock = self.context.socket(zmq.SUB)

            # Define subscription and the messages with prefix to accept.
            # setsockopt obtain the data which message starts with the second argument
            # Then we obtain data from the topic with that starts with topic_name value
            self.sock.setsockopt(zmq.SUBSCRIBE, self.topic)
           
            if self.mode == "many2one":
                # This allows only use one publisher connected at the same endpoint
                print ("Multiple subscribbers: ON")
                self.sock.bind(endpoint)
                print ("subcriber " + endpoint +  " bind")
            elif self.mode == "one2many":
                # This allows two use more that one publisher ate the same endpoint
                print ("Multiple subscribbers: OFF")
                self.sock.connect(endpoint)
                print ("subcriber " + endpoint +  " connect")


        except:
            
            print("Socket already in use, restarting")
            self.sock.close()
            self.context.destroy()
            time.sleep(.2)
            self.context = zmq.Context()
            self.sock = self.context.socket(zmq.SUB)
            self.sock.setsockopt(zmq.SUBSCRIBE, self.topic)

            if self.mode == "many2one":
                # This allows only use one publisher connected at the same endpoint
                print ("subcriber " + endpoint +  " bind")
                self.sock.bind(endpoint)
                # This allows two use more that one publisher ate the same endpoint
            elif self.mode == "one2many":
                print ("subcriber " + endpoint +  " connect")
                self.sock.connect(endpoint)

        print ("ZMQ subscriber started in " +  endpoint)




    def advertising_zqm(self, node_name, topic, master_ip = '127.0.0.1', master_port = 7000):
        
        """ Function used register a topic """

        context = zmq.Context()
        self.master_sock = context.socket(zmq.REQ)
        self.master_sock.connect("tcp://"+ master_ip + ":" + str(master_port))
        self.master_sock.send_json({'node_name':node_name, 'topic':topic})
        response = self.master_sock.recv_json()
        topic_id = response['topic']
        if(topic_id == topic):
            port = response['port']
        return port
    
    #Status: OK
    def deserialization(self, info):
        """ Separate the topic and the json message from the data received from the ZeroMQ socket. If the deserialization was successful and the message as a python dictionary
            
            Parameters
            ----------
            info : string
                topic + message received by the ZQM socket 

            Returns
            -------
            msg : string
                String message as a python dictionary
        """
        try:
            json0 = info.find('{')
            topic = info[0:json0].strip()
            msg = json.loads(info[json0:])
            success = True
        except:
            msg = ""
            success = False
        return msg


    def listen_string(self, block_mode = True):
        if self.transport ==  "ZMQ":
            """ Function used to read string data from the sokect. The read operation is in blocking mode
                
                Returns
                -------
                message : string 
                    String received in the socket.
                    
            """
            message = ""
            try:
                #Blocking mode
                if block_mode:
                    # Get the message
                    info = self.sock.recv()
                    # Split the message
                    list_message_splitted = info.split(self.delimiter)

                    message = list_message_splitted[1]
                    time.sleep(.001)
                    success = True
                #Non blocking mode
                else:
                    info = self.sock.recv(flags = zmq.NOBLOCK)
                    # Split the message
                    list_message_splitted = info.split(self.delimiter)

                    message = list_message_splitted[1]
                    time.sleep(.001)
                    success = True
            #Exeption for non blocking mode timeout
            except zmq.Again as e:
                #Nothing to read
                success = False
                pass
            return  success, message


    #Status: OK
    def listen_info(self,block_mode =  True):
        """ Listen for a json message that define the human state or robot action. 
            
            Parameters
            ----------

            block_mode : bool
                If == True, then the read operation is in blocking mode (the execution continue until there are something to read), otherwise in non blocking mode (if not data, then the execution of the program continues an exception is launched after a timeout).
            
            Returns
            -------

            success : bool
                Return true if the read operation was successfull

            info : dictionary
                Message
        """
        if self.transport ==  "ZMQ":    
            success = False
            info = {}
            try:
                #Blocking mode
                if block_mode:
                    info = self.deserialization(self.sock.recv())
                    time.sleep(.001)
                    success = True
                #Non blocking mode
                else:
                    info = self.deserialization(self.sock.recv(flags = zmq.NOBLOCK))
                    time.sleep(.001)
                    success = True
            #Exeption for non blocking mode timeout
            except zmq.Again as e:
                #Nothing to read
                success = False
                pass
            return  success, info

    #TODO: does not work, no recive mensajes desde send_json
    def listen(self,block_mode =  True):
        if self.transport ==  "ZMQ":
            success = False
            info = {}
            try:
                #Blocking mode
                if block_mode:
                    info = self.sock.recv_json()
                    print info
                    time.sleep(.001)
                    success = True
                #Non blocking mode
                else:
                    info = self.sock.recv_json(flags = zmq.NOBLOCK)
                    print info
                    time.sleep(.001)
                    success = True
            #Exeption for non blocking mode timeout
            except zmq.Again as e:
                #Nothing to read
                success = False
                pass

        return  success, info

# Experimental .....................................................................................

    #TODO: used? delete it?
    def listen_csharp(self, block_mode =  True, debug = False):   
        """ Function used to read data from a NetMQ socket (C# version of ZeroMQ). 
            The ZQM wrapper in C# (NetMQ) works different that ZMQ. Instead of send a message as ``topic + space + message`` where ``topic`` and ``message`` are strings, NetMQ send a message as ``topic + enter + message``. 
            Therefore, this function read first the topic part and then the message part and only returns the message part obtained.

            Parameters
            ----------

            block_mode : bool
                Select blocking (True) or non blocking mode (False).

            debug :bool 
                If True the message is printed in the console

            Returns
            -------
            message : string
                part from a NetQM socket message
        """
        try:
            # If blocking mode
            if block_mode:
                # Get the message in non blocking mode
                topic= self.sock.recv()
                if topic == self.topic:
                    message = self.sock.recv()            
                    if debug:
                        print (topic)
                        print (message)
                    return message
            else:

                # Get the topic in blocking mode
                topic= self.sock.recv(flags = zmq.NOBLOCK)
                if topic == self.topic:
                    # The next message is the message
                    message = self.sock.recv()
                    # Print the state value if is in debug mode
                    if debug:
                        print (topic)
                        print (message)
                    return message

        except zmq.Again as e:
            time.sleep(.05)
            return  'none'


            

class decode_message():
    """ This class is used to decode the sensory messages from devices such as Kinect.
        
        Parameters
        ----------
        delimiter : string
            This parameter indicate the delimiter between the info received. By default is ``,``.
    """

    def __init__(self,delimiter = ','):
        self.delimiter = delimiter

    def decode_smartwatch_imu(self,line,start = 2):
        """3 axis info decodification

        Parameters
        ----------
        line : string 
            Sample of 3 axis information
            
        start : int 
            Starting line of the 3 axis information

        Returns
        -------
        success: bool
            True if the string has the correct format

        option: int 
            if option == 0 then is aceleration data, if option = 1 then is gyroscope data, if option = 2 then angle axis representation

        value1: float 
            x value

        value2: float 
            y value

        value3: float 
            z value

        Example
        -------

        An example of a format used for a wearAmi program is:

        - <indicator>;number;x_value;y_value:z_value
        
        where <indicator> can be a (acceleration), y (gyroscope), e (euler angles)

        """
        line_list = line.split(self.delimiter)
        if(line_list[0] == 'a'):
                if(len(line_list)==start+3 and line_list[start+2] != ''):
                        x = line_list[start ]
                        y = line_list[start +1]
                        z = line_list[start +2]
                        return True,0,x,y,z
        if(line_list[0] == 'y'):
                if(len(line_list)==start+3 and line_list[start+2] != ''):
                        x = line_list[start ]
                        y = line_list[start +1]
                        z = line_list[start +2]
                        return True,1,x,y,z
        if(line_list[0] == 'r'):
                if(len(line_list)==start+3 and line_list[start+2] != ''):
                        pitch = line_list[start ]
                        yaw = line_list[start +1]
                        roll = line_list[start +2]
                        return True,2,yaw,pitch,roll
        print "error decoding data"
        return False,0,0,0,0


    def decode_3axis_info(self,line):
        #TODO: improve and add try catch
        """3 axis info decodification

        Parameters
        ----------
        line : string 
            Sample of 3 axis information

        Returns
        -------
        success: bool
            True if the string has the correct format

        value1: float 
            x value

        value2: float 
            y value

        value3: float 
            z ValueError
        """
        line_list = line.split(self.delimiter)
        if(len(line_list)==3):
            x = line_list[0]
            y = line_list[1]
            z = line_list[2]
            return True,x,y,z
       
        print "error decoding data"
        return False,0,0,0

        
if __name__ == "__main__":
    import doctest
    doctest.testmod()

# Which is better?
#From ZeroMQ v3.x, filtering happens at the publisher side when using a
#  connected protocol (tcp:// or ipc://). Using the epgm:// protocol,
#  filtering happens at the subscriber side.
#  In ZeroMQ v2.x, all filtering happened at the subscriber side.
