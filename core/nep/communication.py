# coding = utf-8
#!/usr/bin/env python

# ------------------------ Communication module --------------------------------
# Description: Set of classes used for simplify the use of ZeroMQ in publisher/subscriber communication pattern.
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


import time
import os
import zmq
import simplejson
import sys
import socket
import signal

##try:
##    import nanomsg
##except ImportError:
##    print ("Nanomsg not installed")



class node:

    def signal_handler(self, signal, frame):
        """Signal handler used to close the app"""
        print('Signal Handler, you pressed Ctrl+C! to close the node')
        time.sleep(1)
        sys.exit(0)
    
    def __init__(self, node_name, transport = "ZMQ"):
        """
        Class used to define a node and publisher-subscriber patterns

        Parameters
        ----------

        node_name : string 
            Name of the node
        
        transport : string
            Define the trasport layer of the node, can be 'ROS', 'ZMQ' or 'NN' to use ROS, ZeroMQ and and nanomsg respectively

        """
        signal.signal(signal.SIGINT, self.signal_handler)
        self.node_name = node_name
        self.transport  = transport 
        print ("New NEP node: " + self.node_name)
        
        if self.transport  == 'ROS':
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


    def conf_pub(self, msg_type = "dict", transport = "ZMQ" , network = "P2P", port = "9000", ip = "127.0.0.1", mode = "one2many" ):
        """

        The configuration of publishers are defined using python dictionaries with a specific format. This function can be used to
        define the configuration of a publisher. By default "ZMQ" (ZeroMQ) in a "P2P" network in "one2many" mode it is used.

        Parameters
        ----------
        msg_type : string 
            Type of data to send (recomended to allows ROS geometric messages compatibility)

        transport : string 
            Transport layer used to communicate, it can be:"ZMQ" to use ZeroMQ, "ROS" to use ROS, and "NN" to use Nanomsg

        network : string 
            Type of network architecture, it can be "direct" and "P2P" (only for ZeroMQ and Nanomsg)

        port : string 
            Value of the port to perform the socket connection (only for ZeroMQ and Nanomsg in a "direct" network)

        ip : string 
            Value of the ip to perform the socket connection (only for ZeroMQ and Nanomsg in a "direct" network)

        mode : string
            Only for ZeroMQ and Nanomsg. It can be "one2many" (one publisher and many subscribers in a topic), "many2one" (one publisher and many subscribers in a topic), "many2many" (many publishers and many subscribers in a topic).    

        Returns
        ----------

        conf: dictionary
            Dictionary with the specifications of the publisher

        Example
        ----------

        Creates a default publisher using ZeroMQ

        .. code-block:: python

            import nep
            new_node = nep.node("dummy_node")
            configuration = new_node.config_pub()
            pub = new_node.new_pub("dummy_topic", configuration)
        

        Creates a ROS publisher

        .. code-block:: python

            import nep
            new_node = nep.node("dummy_node", "ROS")
            configuration = new_node.config_pub()
            pub = new_node.new_pub("dummy_topic", configuration)
        
        """

        
        conf = { 'msg_type': msg_type, 'transport': transport, 'network': network, 'port': port, 'ip': ip, 'mode':mode}
        return conf

    def conf_sub(self, msg_type = "dict", transport = "ZMQ", network = "P2P", port = "9000", ip = "127.0.0.1", mode = "one2many" ):
        
        """
        The configuration of subscribers are defined using python dictionaries with a specific format. This function can be used to
        define the configuration of a subscriber. By default "ZMQ" (ZeroMQ) in a "P2P" network in "one2many" mode it is used.

        Parameters
        ----------
        msg_type : string 
            Type of data to send (recomended to allows ROS geometric messages compatibility)

        transport : string 
            Transport layer used to communicate, it can be "ZMQ" to use ZeroMQ, "ROS" to use ROS, and "NANO" to use Nanomsg

        network : string 
            Type of network architecture, it can be "direct" and "P2P" (only for ZeroMQ and Nanomsg)

        port : string 
            Value of the port to perform the socket connection (only for ZeroMQ and Nanomsg in a "direct" network)

        ip : string 
            Value of the ip to perform the socket connection (only for ZeroMQ and Nanomsg in a "direct" network)

        mode : string
            Only for ZeroMQ and Nanomsg. It can be "one2many" (one publisher and many subscribers in a topic), "many2one" (one publisher and many subscribers in a topic), "many2many" (many publishers and many subscribers in a topic).    

        Returns
        ----------

        conf: dictionary
            Dictionary with the specifications of the subscriber

        Example
        ----------

        Creates a default subscriber

        .. code-block:: python

            import nep
            new_node = nep.node("dummy_node")
            configuration = new_node.config_sub() 
            sub = new_node.new_sub("dummy_topic", configuration)
        
        Creates a ROS subscriber

        .. code-block:: python

            import nep
            new_node = nep.node("dummy_node", "ROS")
            configuration = new_node.config_sub()
            pub = new_node.new_sub("dummy_topic", configuration)
        
        """

        conf = { 'msg_type': msg_type, 'transport': transport, 'network': network, 'port': port, 'ip': ip, 'mode':mode}
        return conf

    def new_pub(self,topic, configuration =  {'transport': "ZMQ", 'network': "P2P", 'mode':"one2many", 'ip': '127.0.0.1', 'msg_type' : 'dict' }):
        """
        Function used to generate a new publisher in the current node

        Parameters
        ----------
        topic : string 
            Name of the topic

        configuration : dictionary 
            Configuration of the publisher


        Returns
        ----------

        pub : publisher
            publisher instance


        Example
        ----------

        Creates a default publisher

        .. code-block:: python

            import nep
            new_node = nep.node("dummy_node")
            configuration = new_node.config_pub() 
            pub = new_node.new_sub("dummy_topic", configuration)

        """
        
        #TODO: launch error if you dont put msg_type or conf
        pub = publisher(topic, self.node_name, configuration)
        return pub

    def new_sub(self,topic, configuration =  {'transport': "ZMQ", 'network': "P2P", 'mode':"one2many", 'ip': '127.0.0.1', 'msg_type' : 'dict' }):

        """
        Function used to generate a new subscriber in the current node

        Parameters
        ----------
        topic : string 
            Name of the topic

        configuration : dictionary  
            Configuration of the subscriber

        Returns
        ----------

        sub : subscriber 
            subscriber instance


        Creates a default subscriber

        .. code-block:: python

            import nep
            new_node = nep.node("dummy_node")
            configuration = new_node.config_sub() 
            sub = new_node.new_sub("dummy_topic", configuration)

        """

        sub = subscriber(topic, self.node_name, configuration)
        return sub



class publisher:
    """ Publisher class used for inter-process comunication between nodes. Supports ZeroMQ, nanomsg and ROS publishers. 
        Parameters
        ----------
        topic : string 
            Topic name to publish the messages

        node_name : string
            Name of the node 

        conf : dictionary
            Configuration of the publisher. The ease way to define this parameter is to use the conf_pub function of the node class

    """

    def __init__(self, topic, node_name = "default", conf =  {'transport': "ZMQ", 'network': "P2P", 'mode':"one2many", 'ip' : '127.0.0.1', 'msg_type' : 'dict' }):

        self.conf = conf
        self.network = self.conf['network']
        self.transport =  self.conf['transport']
        self.node_name = node_name
        self.topic = topic
        self.msg_type =  self.conf['msg_type']

        if self.transport ==  "ZMQ": #Use ZeroMQ
            print ("New publisher using ZMQ")
            try:
                self.mode = self.conf['mode']
            except:
                print ("WARNING: publisher mode parameter not defined, 'one2many' mode is set by default")
                self.mode = "one2many"
            self.__create_ZMQ_publisher()

        elif self.transport ==  "ROS": #Use ROS
            print ("New publisher using ROS")
            self.__create_ROS_publisher()
            
        elif self.transport ==  "NN": #Use nanmsg
            print ("New publisher using nanomsg")
            try:
                self.mode = self.conf['mode']
                self.__create_NN_publisher()
            except:
                print ("WARNING: publisher mode parameter not defined, 'one2many' mode is set by default")
                self.mode = "one2many"
                self.__create_NN_publisher()
        else:
            msg = "ERROR: Transport parameter " + self.transport + "is not supported, use instead 'ROS', 'ZMQ' (for ZeroMQ) or 'NN' (for nanomsg). "
            raise ValueError(msg)


    #TODO:also define queue_size
    def __create_ROS_publisher(self):
        """Function used to create a ROS publisher"""
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

            from geometry_msgs.msg import Vector3
            self.ros_pub = rospy.Publisher(self.topic, Vector3, queue_size=10)

        elif self.msg_type == "pose":

            from geometry_msgs.msg import Pose
            self.ros_pub = rospy.Publisher(self.topic, Pose, queue_size=10)
        

    def __create_ZMQ_publisher(self):
        """Function used to create a ZeroMQ publisher"""

        if self.network == "direct":
            self.port = self.conf['port']
            # Set the port selected by the user
            port = self.port
        elif self.network == "P2P":
            # Register the topic in the NEP Master and get the port
            print ("Advertising topic (" + self.topic + ") to NEP Master ....")
            port = self.__advertising_nep(self.node_name, self.topic, master_ip = '127.0.0.1', master_port = 7000, mode = self.mode )
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
                print ("publisher " + endpoint +  " bind")
                self.sock.bind(endpoint)
            elif self.mode == "many2one":
                # This allows two use more that one publisher ate the same endpoint
                print ("publisher " + endpoint +  " connect")
                self.sock.connect(endpoint)
            elif  self.mode == "many2many":
                print ("many2many mode")
                self.sock.connect(endpoint)
                print ("publisher " + endpoint +  " connect")
            else:
                print ("WARNING: mode selected as:" + str(self.mode) + "it can be only: 'many2one' or  'one2many'")
                print ("Mode set as 'one2many'")
                print ("publisher " + endpoint +  " bind")
                self.sock.bind(endpoint)

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
            elif  self.mode == "many2many":
                print ("many2many mode")
                self.sock.connect(endpoint)
                print ("publisher " + endpoint +  " connect")
            else:
                print ("WARNING: mode selected as:" + str(self.mode) + "it can be only: 'many2one' or  'one2many'")
                print ("Mode set as 'one2many'")
                print ("publisher " + endpoint +  " bind")
                self.sock.bind(endpoint)

        time.sleep(1)
        #TODO: why this problem?
        #This next lines are used to start the comunication, and avoid some errors presented with zeromq
        #message = {'actions': [{'action':'none', 'inputs':'none'}]}
        #self.send_info(message)

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

    def __create_NN_publisher(self):
        """Function used to create a NN publisher"""

        if self.network == "direct":
            self.port = self.conf['port']
            # Set the port selected by the user
            port = self.port
        elif self.network == "P2P":
            # Register the topic in the NEP Master and get the port
            print ("Advertising topic: '" + self.topic + "' to NEP Master ....")
            port = self.__advertising_nep(self.node_name, self.topic, master_ip = '127.0.0.1', master_port = 7000, mode = self.mode )
            print ("Topic registered by the NEP Master")

        ip = self.conf['ip']

        # Create a new ZeroMQ context and a publisher socket
        try:
            self.sock = nanomsg.Socket(nanomsg.PUB)
            
            if self.mode == "one2many":
                # This allows only use one publisher connected at the same endpoint
                if ip == '127.0.0.1':
                    ip = "*"
                endpoint = "tcp://" + ip + ":" + str(port)
                print ("publisher " + endpoint +  " bind")
                self.sock.bind(endpoint)
            elif self.mode == "many2one":
                # This allows two use more that one publisher ate the same endpoint
                if ip == '127.0.0.1':
                    ip = "localhost"
                endpoint = "tcp://" + ip + ":" + str(port)
                print ("publisher " + endpoint +  " connect")
                self.sock.connect(endpoint)
            elif  self.mode == "many2many":
                if ip == '127.0.0.1':
                    ip = "localhost"
                endpoint = "tcp://" + ip + ":" + str(port)
                print ("many2many mode")
                self.sock.connect(endpoint)
                print ("publisher " + endpoint +  " connect")
            else:
                if ip == '127.0.0.1':
                    ip = "*"
                endpoint = "tcp://" + ip + ":" + str(port)
                print ("WARNING: mode selected as:" + str(self.mode) + "it can be only: 'many2one' or  'one2many'")
                print ("Mode set as 'one2many'")
                print ("publisher " + endpoint +  " bind")
                self.sock.bind(endpoint)
            time.sleep(1)
        except:
            print ("Socket in use")
            #TODO: restart connection
        
 
    def __advertising_nep(self, node_name, topic, master_ip = '127.0.0.1', master_port = 7000, mode = "one2many"):
        
        """Function used to register a publisher in P2P connections
                
        Parameters
        ----------
        node_name : string 
            Name of the node

        topic : string
            Topic to register

        master_ip : string 
            ip of the master node service

        master_port : int
            port of the master node service

        Returns
        ----------
        port : string
            Port used to connect the socket
        
        """

        c = client( master_ip, master_port, transport = "ZMQ")
        c.send_info({'node_name':node_name, 'topic':topic, 'mode':mode })
        response = c.listen_info()
        
        topic_id = response['topic']
        if(topic_id == topic):
            port = response['port']
        return port

    def _dumps(self,o, **kwargs):
        """Serialize object to JSON bytes (utf-8).
        
        See jsonapi.jsonmod.dumps for details on kwargs.
        """
        
        if 'separators' not in kwargs:
            kwargs['separators'] = (',', ':')
        
        s = simplejson.dumps(o, **kwargs)
        
        if isinstance(s, unicode):
            s = s.encode('utf8')
        
        return s


    #Status: OK
    def _serialization(self, message, topic = None):
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
            return self.topic + ' ' + self._dumps(message)
        else:
            return topic + ' ' + self._dumps(message)
            
    
    
    def send_string(self,message, topic = None):
        """ Publish a string value. If a topic is not specified, then the messages will be published in the topic specified in the parameter topic_name when a object in this class is created.
            Otherwise it is published in the topic specified in the second parameter of this function. If the topic is not specified it send the message in the default topic.
            
            Parameters
            ----------
            message : string 
                String to be sended

            topic : string
                name of the topic to send the message

            Example
            ----------

            Send a string in a default publisher

            .. code-block:: python

                import nep
                new_node = nep.node("dummy_node")
                configuration = new_node.config_sub() 
                pub = new_node.new_pub("dummy_topic", configuration)
                pub.send_string("hello")  
        """

        if self.transport ==  "ZMQ":
            if topic is None:
                self.sock.send_string(self.topic + ' ' + message)
            else:
                self.sock.send_string(topic + ' ' + message)
        
        if self.transport ==  "NN":
            if topic is None:
                self.sock.send(self.topic + ' ' + message)
            else:
                self.sock.send(topic + ' ' + message)

        if self.transport == "ROS":
            self.ros_pub.publish(message)
            

    #Status: OK
    def send_info(self, message, topic = None, debug = False):
        """ Function used to publish a python dictionary. The message is first serialized using json format and then published by the socket
            
            Parameters
            ----------
            message : dictionary 
                Python dictionary to be send
            topic : string
                name of the topic to send the message
            debug : bool
                if == True, then it print the message to send

            Examples
            ----------

            Send a dictionary in a default publisher:


            .. code-block:: python

                import nep
                new_node = nep.node("dummy_node")
                configuration = new_node.config_sub()) 
                pub = new_node.new_pub("dummy_topic", configuration)
                pub.send_info({'message':"hello"}) 


            Send a nep_msg in a default publisher:

            .. code-block:: python

                import nep
                import nep.nep_msg
                new_node = nep.node("dummy_node")
                configuration = new_node.config_sub(msg_type = "vector") # nep_msg definition
                pub = new_node.new_pub("dummy_topic", configuration)
                vector = nep.vector(0,0,1)
                pub.send_info(vector)
            
            Send a nep_msg in ROS publisher:

            .. code-block:: python

                import nep
                import nep.nep_msg
                new_node = nep.node("dummy_node", useROS=True)
                # ROS Vector3 definition
                configuration = new_node.config_sub(msg_type = "vector", transport = "ROS")
                pub = new_node.new_pub("dummy_topic", configuration)
                vector = nep.vector(0,0,1) 
                pub.send_info(vector) 

        """

        if self.transport ==  "ZMQ" or self.transport ==  "NN":
            # TODO: if data es diferente a la definida poner un warning
            if topic is None:
                info = self._serialization(message)
            else:
                info =  self._serialization(message, topic)

            if debug:
                try:
                    print (info)
                except:
                    pass
            self.sock.send(info)

        
        if self.transport == "ROS":
        #TODO add try and except fot error of data

            if self.msg_type == "string":
                pub.publish(message)
            
            elif self.msg_type == "velocity":
                from geometry_msgs.msg import Twist
                twist = Twist()
                twist.linear.x = message.data['linear']['x']
                twist.linear.y = message.data['linear']['y']
                twist.linear.z = message.data['linear']['z']
                twist.angular.x = message.data['angular']['x']
                twist.angular.y = message.data['angular']['y']
                twist.angular.z = message.data['angular']['z']
                self.ros_pub.publish(twist)

            elif self.msg_type == "point":
                from geometry_msgs.msg import Point
                point = Point()
                point.x = message.data['x']
                point.y = message.data['y']
                point.z = message.data['z']
                self.ros_pub.publish(point)

            elif self.msg_type == "wrench":
                from geometry_msgs.msg import Wrench
                wrench = Wrench()
                wrench.force.x = message.data['force']['x']
                wrench.force.y = message.data['force']['y']
                wrench.force.z = message.data['force']['z']
                wrench.torque.x = message.data['torque']['x']
                wrench.torque.y = message.data['torque']['y']
                wrench.torque.z = message.data['torque']['z']
                self.ros_pub.publish(wrench)
                

            elif self.msg_type == "accel":
                from geometry_msgs.msg import Accel
                accel = Accel()
                accel.linear.x = message.data['linear']['x']
                accel.linear.y = message.data['linear']['y']
                accel.linear.z = message.data['linear']['z']
                accel.angular.x = message.data['angular']['x']
                accel.angular.y = message.data['angular']['y']
                accel.angular.z = message.data['angular']['z']
                self.ros_pub.publish(accel)

            elif self.msg_type == "quaternion":
                from geometry_msgs.msg import Quaternion
                quaternion = Quaternion()
                quaternion.x = message.data['x']
                quaternion.y = message.data['y']
                quaternion.z = message.data['z']
                quaternion.w = message.data['w']
                self.ros_pub.publish(quaternion)
                pass

            elif self.msg_type == "vector":
                from geometry_msgs.msg import Vector3
                vector = Vector3()
                vector.x = message.data['x']
                vector.y = message.data['y']
                vector.z = message.data['z']
                self.ros_pub.publish(vector)

            elif self.msg_type == "pose":
                from geometry_msgs.msg import Pose
                pose = Pose()
                pose.position.x = message.data['position']['x']
                pose.position.y = message.data['position']['y']
                pose.position.z = message.data['position']['z']
                pose.orientation.x = message.data['orientation']['x']
                pose.orientation.y = message.data['orientation']['y']
                pose.orientation.z = message.data['orientation']['z']
                pose.orientation.w = message.data['orientation']['w']
                self.ros_pub.publish(pose)
        


    
#Status: OK
class subscriber:
    """ Subscriber class used for inter-process comunication between nodes. 

        Parameters
        ----------
        topic : string 
            topic name to publish the messages

        node_name : string
            Name of the node 

        conf: dictionary
            Configuration of the subscriber

    """
    def __init__(self, topic, node_name = "default", conf =  {'transport': "ZMQ", 'network': "P2P", 'mode':"one2many", 'ip' : '127.0.0.1', 'type':'dict' }):
    
        self.conf = conf
        self.network = self.conf['network']
        self.transport =  self.conf['transport']
        self.node_name = node_name
        self.topic = topic
        self.delimiter = " "

        if self.transport ==  "ZMQ":
            try:
                self.mode = self.conf['mode']
                self.__create_ZMQ_subscriber()
            except:
                print ("WARNING: publisher mode nod defined, 'one2many' mode is set by default")
                self.mode = "one2many"
                self.__create_ZMQ_subscriber()

        elif self.transport ==  "NN": #Use nanmsg
            print ("New subscriber using nanomsg")
            try:
                self.mode = self.conf['mode']
                self.__create_NN_subscriber()
            except:
                print ("WARNING: subscriber mode parameter not defined, 'many2one' mode is set by default")
                self.mode = "many2one"
                self.__create_NN_subscriber()

        
        elif self.transport ==  "ROS":
            self.__create_ROS_subscriber()



    def __create_ZMQ_subscriber(self):
        """Function used to create a ZeroMQ publisher"""
        if self.network == "direct":
            # Set the port selected by the user
            self.port = self.conf["port"]
            port = self.port
        elif self.network == "P2P":
            # Register the topic in the NEP Master and get the port
            print ("Advertising topic (" + self.topic + ") to NEP Master ....")
            port = self.__advertising_nep(self.node_name, self.topic, master_ip = '127.0.0.1', master_port = 7000, mode = self.mode)
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
                print ("Multiple subscribers: OFF")
                self.sock.bind(endpoint)
                print ("subcriber " + endpoint +  " bind")
            elif self.mode == "one2many":
                # This allows two use more that one publisher ate the same endpoint
                print ("Multiple subscribers: ON")
                self.sock.connect(endpoint)
                print ("subcriber " + endpoint +  " connect")

            elif  self.mode == "many2many":
                endpoint = "tcp://" + ip + ":" + str(port+1)
                print ("many2many mode")
                self.sock.connect(endpoint)
                print ("subcriber " + endpoint +  " connect")

            else:
                print ("WARNING: mode selected as:" + str(self.mode) + "it can be only: 'many2one' or  'one2many'")
                print ("Mode set as 'one2many'")
                print ("subcriber " + endpoint +  " bind")
                self.sock.connect(endpoint)


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
                print ("Multiple subscribers: OFF")
                print ("subcriber " + endpoint +  " bind")
                self.sock.bind(endpoint)
                # This allows two use more that one publisher ate the same endpoint
            elif self.mode == "one2many":
                print ("Multiple subscribers: ON")
                print ("subcriber " + endpoint +  " connect")
                self.sock.connect(endpoint)
            elif  self.mode == "many2many":
                endpoint = "tcp://" + ip + ":" + str(port+1)
                print ("many2many mode")
                self.sock.connect(endpoint)
                print ("subcriber " + endpoint +  " connect")
            else:
                print ("WARNING: mode selected as:" + str(self.mode) + "it can be only: 'many2one' or  'one2many'")
                print ("Mode set as 'one2many'")
                print ("subcriber " + endpoint +  " bind")
                self.sock.connect(endpoint)

        print ("ZMQ subscriber started in " +  endpoint)


    def __create_NN_subscriber(self):
        """Function used to create a NN publisher"""
        import nanomsg

        if self.network == "direct":
            self.port = self.conf['port']
            # Set the port selected by the user
            port = self.port
        elif self.network == "P2P":
            # Register the topic in the NEP Master and get the port
            print ("Advertising topic: '" + self.topic + "' to NEP Master ....")
            port = self.__advertising_nep(self.node_name, self.topic, master_ip = '127.0.0.1', master_port = 7000, mode = self.mode )
            print ("Topic registered by the NEP Master")

        ip = self.conf['ip']

        # Create a new NN socket
        try:
            self.sock = nanomsg.Socket(nanomsg.SUB)
            self.sock.set_string_option(nanomsg.SUB, nanomsg.SUB_SUBSCRIBE, self.topic)

                       
            if self.mode == "many2one":
                # This allows only use one publisher connected at the same endpoint
                if ip == '127.0.0.1':
                    ip = "*"
                endpoint = "tcp://" + ip + ":" + str(port)
                print ("Multiple subscribers: OFF")
                self.sock.bind(endpoint)
                print ("subscriber " + endpoint +  " bind")
            elif self.mode == "one2many":
                # This allows two use more that one publisher ate the same endpoint
                if ip == '127.0.0.1':
                    ip = "localhost"
                endpoint = "tcp://" + ip + ":" + str(port)
                print ("Multiple subscribers: ON")
                self.sock.connect(endpoint)
                print ("subscriber " + endpoint +  " connect")

            elif  self.mode == "many2many":
                if ip == '127.0.0.1':
                    ip = "localhost"
                endpoint = "tcp://" + ip + ":" + str(port)
                endpoint = "tcp://" + ip + ":" + str(port+1)
                print ("many2many mode")
                self.sock.connect(endpoint)
                print ("subscriber " + endpoint +  " connect")

            else:
                if ip == '127.0.0.1':
                    ip = "*"
                endpoint = "tcp://" + ip + ":" + str(port)
                print ("WARNING: mode selected as:" + str(self.mode) + "it can be only: 'many2one' or  'one2many'")
                print ("Mode set as 'one2many'")
                print ("subcriber " + endpoint +  " bind")
                self.sock.connect(endpoint)

        except:
            print ("Socket in use")
            #TODO: restart connection


    #TODO: close for nanomsg
    def close_ZMQ_subscriber(self):
        """ This function closes the socket"""
        print "close listener"
        self.sock.close()
        self.context.destroy()
        time.sleep(1)




    def __advertising_nep(self, node_name, topic, master_ip = '127.0.0.1', master_port = 7000, mode = "one2many"):
        
        """Function used to register a publisher in P2P connections
                
        Parameters
        ----------
        node_name : string 
            Name of the node

        topic : string
            Topic to register

        master_ip : string 
            ip of the master node service

        master_port : int
            port of the master node service

        Returns
        ----------
        port : string
            Port used to connect the socket
        
        """

        c = client( master_ip, master_port, transport = "ZMQ")
        c.send_info({'node_name':node_name, 'topic':topic, 'mode':mode })
        response = c.listen_info()
        
        topic_id = response['topic']
        if(topic_id == topic):
            port = response['port']
        return port


    def _loads(self, s, **kwargs):
        """Load object from JSON bytes (utf-8).
        
        See jsonapi.jsonmod.loads for details on kwargs.
        """
        
        if str is unicode and isinstance(s, bytes):
            s = s.decode('utf8')
        
        return simplejson.loads(s, **kwargs)

    
    #Status: OK
    def _deserialization(self, info):
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
            msg = self._loads(info[json0:])
            success = True
        except:
            msg = ""
            success = False
        return msg


    def listen_string(self, block_mode = False):
        
        """ Function used to read string data from the sokect. The operation is by default in non blocking mode

            Parameters
            ----------
            block_mode : bool
                If True, the socket will set in blocking mode, otherwise the socket will be in non blocking mode
                
            Returns
            -------
            success : bool
                If True the information was obtained inside the timeline in non blocking mode  

            message : string 
                String received in the socket.      
        """

        if self.transport ==  "ZMQ" or self.transport ==  "NN" :
            message = ""
            try:
                #Blocking mode
                if block_mode:
                    # Get the message
                    info = self.sock.recv()
                    # Split the message

                    index = info.find(' ')
                    topic = info[0:index].strip()
                    message = info[index:]
                    success = True
                #Non blocking mode
                else:
                    if self.transport ==  "ZMQ":
                        info = self.sock.recv(flags = zmq.NOBLOCK)
                    elif self.transport ==  "NN":
                        info = self.sock.recv(flags=nanomsg.DONTWAIT)
                        
                    # Split the message
                    index = info.find(' ')
                    topic = info[0:index].strip()
                    message = info[index:]

                    success = True
            #Exeption for non blocking mode timeout
            except zmq.Again as e:
                #Nothing to read
                success = False
                pass

            #Exeption for non blocking mode timeout
            except nanomsg.NanoMsgAPIError:
                #Nothing to read
                success = False
                pass

            return  success, message
        
            


    #Status: OK
    def listen_info(self,block_mode =  False):
        """ Listen for a json message that define the human state or robot action. The operation is by default in non blocking mode
            
            Parameters
            ----------

            block_mode : bool
                If True, the socket will set in blocking mode, otherwise the socket will be in non blocking mode
                
            Returns
            -------

            success : bool
                If True the information was obtained inside the timeline in non blocking mode  

            info : dictionary
                Message obtained
        """
        if self.transport ==  "ZMQ" or self.transport == "NN":    
            success = False
            info = {}
            try:
                #Blocking mode
                if block_mode:
                    info = self._deserialization(self.sock.recv())
                    time.sleep(.001)
                    success = True
                #Non blocking mode
                else:
                    if self.transport ==  "ZMQ":
                        info = self._deserialization(self.sock.recv(flags = zmq.NOBLOCK))
                    elif self.transport ==  "NN":
                        info = self._deserialization(self.sock.recv(flags=nanomsg.DONTWAIT))

                    time.sleep(.001)
                    success = True
            #Exeption for non blocking mode timeout
            except zmq.Again as e:
                #Nothing to read
                success = False
                pass

            #Exeption for non blocking mode timeout
            except nanomsg.NanoMsgAPIError:
                #Nothing to read
                success = False
                pass

            return  success, info



class broker():
    def __init__(self, IP, PORT_XPUB, PORT_XSUB):
        context = zmq.Context()
        frontend = context.socket(zmq.XSUB)
        frontend.bind("tcp://" + IP + ":" + str(PORT_XSUB))
        backend = context.socket(zmq.XPUB)
        backend.bind("tcp://" + IP + ":" + str(PORT_XPUB))
        zmq.proxy(frontend, backend)
        frontend.close()
        backend.close()
        context.term()

#TODO: sock.close() and context.destroy() must be allway when a process ends
#In some cases socket handles won't be freed until you destroy the context.
#When you exit the program, close your sockets and then call zmq_ctx_destroy(). This destroys the context.
# In a language with automatic object destruction, sockets and contexts 
# will be destroyed as you leave the scope. If you use exceptions you'll have to
#  do the clean-up in something like a "final" block, the same as for any resource.


class server:
    def __init__(self, IP, port, transport = "ZMQ"):
        self.transport = transport

        if transport == "ZMQ":
            # ZMQ sockets
            context = zmq.Context()
            # Define the socket using the "Context"
            self.sock = context.socket(zmq.REP)
            self.sock.bind("tcp://" + IP + ":" + str(port))
        
        elif transport == "normal": 
            # Normal sockets
            try:
                #create an AF_INET, STREAM socket (TCP)
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #self.s.setblocking(0)
                self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            except socket.error, msg:
                print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
                sys.exit();
                
            print 'Socket Created'

            try:
                if IP == "localhost":
                #Same computer
                        IP = socket.gethostbyname( IP )
                        print ("local host in :", IP)
                
            except socket.gaierror:
                #could not resolve
                print 'Hostname could not be resolved. Exiting'
                sys.exit()
            #Connect to remote server
            self.s.bind(('' , port))
            self.s.listen(5)
            print 'Socket connected on ip ' + IP

            while True:
                # Wait for a connection
                print >>sys.stderr, 'waiting for a connection'
                connection, client_address = self.s.accept()

                try:
                    print >>sys.stderr, 'connection from', client_address

                    # Receive the data in small chunks and retransmit it
                    while True:
                        data = connection.recv(16)
                        print >>sys.stderr, 'received "%s"' % data
                        if data:
                            print >>sys.stderr, 'sending data back to the client'
                            connection.sendall(data)
                        else:
                            print >>sys.stderr, 'no more data from', client_address
                            break
            
                finally:
                    # Clean up the connection
                    connection.close()


    def _loads(self, s, **kwargs):
        """Load object from JSON bytes (utf-8).
        
        See jsonapi.jsonmod.loads for details on kwargs.
        """
        
        if str is unicode and isinstance(s, bytes):
            s = s.decode('utf8')
        
        return simplejson.loads(s, **kwargs)

    
    #Status: OK
    def _deserialization(self, info):
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
            msg = self._loads(info[json0:])
            success = True
        except:
            msg = ""
            success = False
        return msg

    def _dumps(self,o, **kwargs):
        """Serialize object to JSON bytes (utf-8).
    
            See jsonapi.jsonmod.dumps for details on kwargs.
        """
        
        if 'separators' not in kwargs:
            kwargs['separators'] = (',', ':')
        
        s = simplejson.dumps(o, **kwargs)
        
        if isinstance(s, unicode):
            s = s.encode('utf8')
        
        return s


    #Status: OK
    def _serialization(self, message):
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
        return self._dumps(message)

    def listen_info(self):

        if self.transport == "ZMQ":
            #response = self.sock.recv_json()
            #return response
            request = self.sock.recv()
            return self._deserialization(request)
            
        else:
            request = self.s.recv(1024)
            return request

    def send_info(self,response):
        
        if self.transport == "ZMQ":
            #self.sock.send_json(request)
            self.sock.send(self._serialization(response))
        else:
            try:
               self.s.sendall(response)
            except socket.error:
                #Send failed
                print 'Send failed'
                sys.exit()


class client:
    def __init__(self, IP, port, transport = "ZMQ"):
        
        self.transport = transport
        if self.transport == "ZMQ":
            context = zmq.Context()
            # Define the socket using the "Context"
            self.sock = context.socket(zmq.REQ)
            self.sock.connect("tcp://" + IP + ":" + str(port))

        elif transport == "normal":

            # Normal sockets
            try:
                #create an AF_INET, STREAM socket (TCP)
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error, msg:
                print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
                sys.exit();
                
            print 'Socket Created'

            try:
                if IP == "localhost":
                #Same computer
                        IP = socket.gethostbyname( IP )
                        print ("local host in :", IP)
                
            except socket.gaierror:
                #could not resolve
                print 'Hostname could not be resolved. Exiting'
                sys.exit()
            #Connect to remote server
            self.s.connect((IP , port))
            print 'Socket connected on ip ' + IP


    def _loads(self, s, **kwargs):
        """Load object from JSON bytes (utf-8).
        
        See jsonapi.jsonmod.loads for details on kwargs.
        """
        
        if str is unicode and isinstance(s, bytes):
            s = s.decode('utf8')
        
        return simplejson.loads(s, **kwargs)

    
    #Status: OK
    def _deserialization(self, info):
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
            msg = self._loads(info[json0:])
            success = True
        except:
            msg = ""
            success = False
        return msg

    def _dumps(self,o, **kwargs):
        """Serialize object to JSON bytes (utf-8).
        
        See jsonapi.jsonmod.dumps for details on kwargs.
        """
        
        if 'separators' not in kwargs:
            kwargs['separators'] = (',', ':')
        
        s = simplejson.dumps(o, **kwargs)
        
        if isinstance(s, unicode):
            s = s.encode('utf8')
        
        return s


    #Status: OK
    def _serialization(self, message):
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
        return self._dumps(message)



    def listen_info(self):
        
        if self.transport == "ZMQ":
            #response = self.sock.recv_json()
            #return response
            response = self.sock.recv()
            return self._deserialization(response)
            
        else:
          response = self.s.recv(1024)
          return response
            

    def send_info(self,request):
        if self.transport == "ZMQ":
            #self.sock.send_json(request)
            self.sock.send(self._serialization(request))
        else:
            try:
               self.s.sendall(request)
            except socket.error:
                #Send failed
                print 'Send failed'
                sys.exit()


if __name__ == "__main__":
    import doctest
    doctest.testmod()

# Which is better?
#From ZeroMQ v3.x, filtering happens at the publisher side when using a
#  connected protocol (tcp:// or ipc://). Using the epgm:// protocol,
#  filtering happens at the subscriber side.
#  In ZeroMQ v2.x, all filtering happened at the subscriber side.
